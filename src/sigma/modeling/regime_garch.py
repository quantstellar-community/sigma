"""Regime-partitioned GARCH (WP-4b.5a, ADR-0011).

Stage 2 of the Hybrid (ADR-0007): after HMM assigns regime labels, fit a
GARCH model per regime (pooled by label, ADR-0011 D1) and use carry-over
forecasting (D2). Decoupled: only consumes regime labels — never the HMM.

Roles:
- ``fit_regime_garch``: learn per-regime GARCH parameters (pooled).
- ``forecast_regime_vol``: 1-day-ahead sigma with carry-over state.
- ``simulate_regime_paths``: scenario paths for WP-5 scenario generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

import numpy as np

from sigma.modeling.errors import ModelingError

__all__ = [
    "GARCHParams",
    "RegimeGARCHFit",
    "RegimeVolForecast",
    "fit_regime_garch",
    "forecast_regime_vol",
    "simulate_regime_paths",
]

_MIN_REGIME_OBS = 100
_DEFAULT_SEED = 42


@dataclass(frozen=True)
class GARCHParams:
    """Estimated GARCH(1,1) parameters for one regime (pooled fit)."""

    omega: float
    alpha: float
    beta: float
    nu: float  # Student-t degrees of freedom

    @property
    def persistence(self) -> float:
        return self.alpha + self.beta

    @property
    def long_run_variance(self) -> float:
        return self.omega / (1.0 - self.persistence)


@dataclass(frozen=True)
class RegimeGARCHFit:
    """Per-regime GARCH parameters with provenance."""

    params_by_regime: dict[int, GARCHParams]
    dataset_id: str


@dataclass(frozen=True)
class RegimeVolForecast:
    """One-day-ahead volatility forecast conditioned on the current regime."""

    sigma_tomorrow: float
    current_regime: int
    dataset_id: str


def _validate(returns: np.ndarray, labels: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(returns, dtype=float)
    label_values = np.asarray(labels, dtype=int)
    if values.ndim != 1 or label_values.ndim != 1:
        msg = "returns and labels must both be 1-D"
        raise ModelingError(msg)
    if len(values) != len(label_values):
        msg = f"labels length {len(label_values)} does not match returns length {len(values)}"
        raise ModelingError(msg)
    if not np.all(np.isfinite(values)):
        msg = "return series contains non-finite values"
        raise ModelingError(msg)
    return values, label_values


def fit_regime_garch(
    returns: np.ndarray,
    labels: np.ndarray,
    *,
    dataset_id: str,
    dist: str = "t",
    seed: int = _DEFAULT_SEED,
) -> RegimeGARCHFit:
    """Fit GARCH(1,1) per regime on the pooled subsample of that regime (D1)."""
    values, label_values = _validate(returns, labels)

    params_by_regime: dict[int, GARCHParams] = {}
    for regime in np.unique(label_values):
        subsample = values[label_values == regime]
        if len(subsample) < _MIN_REGIME_OBS:
            msg = (
                f"regime {regime} has only {len(subsample)} pooled observations; "
                f"need at least {_MIN_REGIME_OBS} to fit GARCH reliably"
            )
            raise ModelingError(msg)
        params_by_regime[int(regime)] = _fit_single_garch(subsample, dist, seed)

    return RegimeGARCHFit(params_by_regime=params_by_regime, dataset_id=dataset_id)


def _fit_single_garch(subsample: np.ndarray, dist: str, seed: int) -> GARCHParams:
    arch = import_module("arch")
    percent = subsample * 100.0
    model = arch.arch_model(percent, mean="Constant", vol="GARCH", p=1, q=1, dist=dist)
    result = model.fit(disp="off", show_warning=False)
    params = result.params

    omega = float(params["omega"]) / 100.0**2  # percent -> decimal
    alpha = float(params["alpha[1]"])
    beta = float(params["beta[1]"])
    nu = float(params.get("nu", 100.0))  # large nu ~ Gaussian
    return GARCHParams(omega=omega, alpha=alpha, beta=beta, nu=nu)


def forecast_regime_vol(
    fit: RegimeGARCHFit,
    returns: np.ndarray,
    labels: np.ndarray,
    *,
    current_idx: int,
) -> RegimeVolForecast:
    """One-step-ahead sigma with carry-over variance state (ADR-0011 D2).

    Walks the series chronologically; on regime switch the parameters change
    but the variance state is carried over (no reset to long-run variance).
    """
    values, label_values = _validate(returns, labels)
    if current_idx < 1 or current_idx >= len(values):
        msg = (
            f"current_idx {current_idx} out of range for series of length {len(values)}"
        )
        raise ModelingError(msg)
    _require_all_regimes_fitted(fit, label_values)

    variance = _long_run_variance(fit, label_values[0])
    for t in range(1, current_idx + 1):
        params = fit.params_by_regime[int(label_values[t])]
        shock_sq = values[t - 1] ** 2
        variance = params.omega + params.alpha * shock_sq + params.beta * variance

    current_regime = int(label_values[current_idx])
    sigma_tomorrow = float(np.sqrt(variance))
    return RegimeVolForecast(
        sigma_tomorrow=sigma_tomorrow,
        current_regime=current_regime,
        dataset_id=fit.dataset_id,
    )


def simulate_regime_paths(
    fit: RegimeGARCHFit,
    *,
    n_days: int,
    n_paths: int,
    seed: int = _DEFAULT_SEED,
    start_regime: int | None = None,
    start_variance: float | None = None,
) -> np.ndarray:
    """Simulate ``n_paths`` sequences of ``n_days`` returns (D4).

    Each day: draw innovation from Student-t(nu[regime]), update variance
    with the regime's GARCH recursion, then move to the next regime using a
    uniform transition model (no learned transitions — labels are the
    conditioning, transitions come from HMM layer in WP-5).
    """
    if n_days < 1 or n_paths < 1:
        msg = "n_days and n_paths must both be >= 1"
        raise ModelingError(msg)
    if not fit.params_by_regime:
        msg = "fit has no regime parameters"
        raise ModelingError(msg)

    rng = np.random.default_rng(seed)
    regimes = sorted(fit.params_by_regime)
    paths = np.empty((n_paths, n_days))

    for path_idx in range(n_paths):
        regime = start_regime if start_regime is not None else regimes[0]
        variance = (
            start_variance
            if start_variance is not None
            else _long_run_variance(fit, regime)
        )
        for day in range(n_days):
            params = fit.params_by_regime[regime]
            innovation = float(rng.standard_t(df=max(params.nu, 2.1)))
            sigma = np.sqrt(variance)
            paths[path_idx, day] = sigma * innovation
            variance = (
                params.omega
                + params.alpha * (sigma * innovation) ** 2
                + params.beta * variance
            )
            # regime transition: uniform random pick among regimes (placeholder;
            # real transition matrix comes from HMM layer at WP-5)
            regime = int(rng.choice(regimes))

    return paths


def _require_all_regimes_fitted(fit: RegimeGARCHFit, labels: np.ndarray) -> None:
    missing = {int(r) for r in np.unique(labels)} - set(fit.params_by_regime)
    if missing:
        msg = f"fit has no parameters for regime(s) {sorted(missing)}"
        raise ModelingError(msg)


def _long_run_variance(fit: RegimeGARCHFit, regime: int) -> float:
    return fit.params_by_regime[int(regime)].long_run_variance
