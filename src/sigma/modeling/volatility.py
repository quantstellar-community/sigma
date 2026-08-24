"""Conditional volatility estimation (WP-4a, ADR-0006).

Five candidates share one contract: given a return history, forecast the
next day's volatility as ``sigma_daily: float``. GARCH is never trusted
until it beats the naive baselines out-of-sample (ADR-0006 D2/D8).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from importlib import import_module

import numpy as np

from sigma.modeling.errors import ModelingError

__all__ = [
    "ArchDiagnostics",
    "VolatilityState",
    "check_arch_effects",
    "constant_sigma",
    "ewma_sigma",
    "garch_sigma",
    "rolling_sigma",
]

_RISKMETRICS_LAMBDA = 0.94
_TRADING_DAYS = 252
_MIN_GARCH_OBS = 100
_GARCH_DISTS = ("normal", "t")


@dataclass(frozen=True)
class VolatilityState:
    """One volatility estimate with provenance (SCHEMA.md §8.2)."""

    asset_id: str
    timestamp: datetime
    sigma_daily: float
    method: str
    dataset_id: str

    @property
    def annualized(self) -> float:
        return self.sigma_daily * math.sqrt(_TRADING_DAYS)


@dataclass(frozen=True)
class ArchDiagnostics:
    """Pre-fit evidence that returns actually carry ARCH effects (D7)."""

    adf_pvalue: float
    arch_lm_pvalue: float
    has_arch_effects: bool


def _as_returns(returns: np.ndarray, minimum: int) -> np.ndarray:
    values = np.asarray(returns, dtype=float)
    if values.ndim != 1 or len(values) < minimum:
        msg = f"need a 1-D return series with at least {minimum} observations"
        raise ModelingError(msg)
    if not np.all(np.isfinite(values)):
        msg = "return series contains non-finite values"
        raise ModelingError(msg)
    return values


def constant_sigma(returns: np.ndarray) -> float:
    """Baseline 0: sample std of the whole history."""
    values = _as_returns(returns, minimum=2)
    return float(np.std(values, ddof=1))


def rolling_sigma(returns: np.ndarray, window: int = 60) -> float:
    """Baseline 1: sample std of the most recent ``window`` observations."""
    if window < 2:
        msg = "rolling window must be at least 2"
        raise ModelingError(msg)
    values = _as_returns(returns, minimum=window)
    return float(np.std(values[-window:], ddof=1))


def ewma_sigma(returns: np.ndarray, lam: float = _RISKMETRICS_LAMBDA) -> float:
    """Baseline 2: RiskMetrics EWMA recursion.

    Variance is initialised to the full-sample variance and updated once per
    observation; the updated variance is the one-step-ahead forecast.
    """
    if not 0.0 < lam < 1.0:
        msg = f"lambda must be in (0, 1), got {lam}"
        raise ModelingError(msg)
    values = _as_returns(returns, minimum=2)

    variance = float(np.var(values))
    for observation in values:
        variance = lam * variance + (1.0 - lam) * observation * observation
    return math.sqrt(variance)


def garch_sigma(
    returns: np.ndarray,
    dist: str = "t",
) -> float:
    """GARCH(1,1) one-step-ahead volatility forecast via the ``arch`` package.

    Fits on percent-scaled returns for numerical stability and converts back.
    Maximum likelihood is deterministic, so repeated fits are reproducible.
    Invalid ``dist`` values are rejected at runtime.
    """
    if dist not in _GARCH_DISTS:
        msg = f"unsupported dist {dist!r}; expected one of {_GARCH_DISTS}"
        raise ModelingError(msg)
    values = _as_returns(returns, minimum=_MIN_GARCH_OBS)

    arch = import_module("arch")
    percent = values * 100.0
    model = arch.arch_model(percent, mean="Constant", vol="GARCH", p=1, q=1, dist=dist)
    result = model.fit(disp="off", show_warning=False)
    forecast_variance = float(
        result.forecast(horizon=1, reindex=False).variance.values[-1, 0]
    )
    return math.sqrt(forecast_variance) / 100.0


def check_arch_effects(returns: np.ndarray) -> ArchDiagnostics:
    """ADF stationarity + ARCH-LM heteroskedasticity tests (statsmodels)."""
    values = _as_returns(returns, minimum=50)

    statsmodels_tsa = import_module("statsmodels.tsa.stattools")
    statsmodels_diag = import_module("statsmodels.stats.diagnostic")

    adf_pvalue = float(statsmodels_tsa.adfuller(values)[1])
    arch_lm_pvalue = float(statsmodels_diag.het_arch(values)[1])
    return ArchDiagnostics(
        adf_pvalue=adf_pvalue,
        arch_lm_pvalue=arch_lm_pvalue,
        has_arch_effects=bool(arch_lm_pvalue < 0.05),
    )
