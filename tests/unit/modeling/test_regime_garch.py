"""Tests for regime-partitioned GARCH (WP-4b.5a, ADR-0011).

Synthetic series with KNOWN regime labels are the ground truth: we verify
that fitting GARCH per regime recovers distinct volatility structures.
"""


import numpy as np
import pytest

from sigma.modeling.errors import ModelingError
from sigma.modeling.regime_garch import (
    RegimeGARCHFit,
    fit_regime_garch,
    forecast_regime_vol,
    simulate_regime_paths,
)

DATASET_ID = "test-snapshot__t0"
_CALM_VOL, _CRISIS_VOL = 0.005, 0.03


def make_two_regime_with_labels(
    n_calm: int = 500, n_crisis: int = 300, seed: int = 13
) -> tuple[np.ndarray, np.ndarray]:
    """Calm block then crisis block; labels known: 0=calm, 1=crisis."""
    rng = np.random.default_rng(seed)
    calm = rng.normal(0.0, _CALM_VOL, n_calm)
    crisis = rng.standard_t(df=5, size=n_crisis) * _CRISIS_VOL
    returns = np.concatenate([calm, crisis])
    labels = np.concatenate([np.zeros(n_calm, dtype=int), np.ones(n_crisis, dtype=int)])
    return returns, labels


# ------------------------------------------------------------------- fit


def test_fit_two_regimes_produces_distinct_params() -> None:
    returns, labels = make_two_regime_with_labels()
    fit = fit_regime_garch(returns, labels, dataset_id=DATASET_ID)

    assert isinstance(fit, RegimeGARCHFit)
    assert set(fit.params_by_regime) == {0, 1}
    assert fit.dataset_id == DATASET_ID

    calm = fit.params_by_regime[0]
    crisis = fit.params_by_regime[1]
    # Crisis must have a higher long-run variance than calm
    assert crisis.long_run_variance > calm.long_run_variance
    # persistence in (0, 1) for both
    for params in fit.params_by_regime.values():
        assert 0.0 < params.persistence < 1.0


def test_fit_is_deterministic_with_fixed_seed() -> None:
    returns, labels = make_two_regime_with_labels()
    a = fit_regime_garch(returns, labels, dataset_id=DATASET_ID)
    b = fit_regime_garch(returns, labels, dataset_id=DATASET_ID)
    for state in a.params_by_regime:
        assert a.params_by_regime[state] == b.params_by_regime[state]


def test_fit_rejects_regime_with_too_few_observations() -> None:
    returns, labels = make_two_regime_with_labels(n_calm=500, n_crisis=30)
    with pytest.raises(ModelingError, match="observations"):
        fit_regime_garch(returns, labels, dataset_id=DATASET_ID)


def test_fit_rejects_length_mismatch() -> None:
    returns, labels = make_two_regime_with_labels()
    with pytest.raises(ModelingError, match="length"):
        fit_regime_garch(returns, labels[:-10], dataset_id=DATASET_ID)


# --------------------------------------------------------------- forecast


def test_forecast_reflects_current_regime_volatility() -> None:
    returns, labels = make_two_regime_with_labels()
    fit = fit_regime_garch(returns, labels, dataset_id=DATASET_ID)

    # last day is crisis -> forecast should be elevated
    crisis_forecast = forecast_regime_vol(
        fit, returns, labels, current_idx=len(returns) - 1
    )
    # first day of calm block -> forecast should be low
    calm_forecast = forecast_regime_vol(fit, returns, labels, current_idx=10)

    assert crisis_forecast.sigma_tomorrow > calm_forecast.sigma_tomorrow
    assert crisis_forecast.current_regime == 1
    assert calm_forecast.current_regime == 0
    assert crisis_forecast.dataset_id == DATASET_ID


def test_forecast_is_deterministic() -> None:
    returns, labels = make_two_regime_with_labels()
    fit = fit_regime_garch(returns, labels, dataset_id=DATASET_ID)
    a = forecast_regime_vol(fit, returns, labels, current_idx=100)
    b = forecast_regime_vol(fit, returns, labels, current_idx=100)
    assert a.sigma_tomorrow == b.sigma_tomorrow


# -------------------------------------------------------------- simulate


def test_simulate_produces_valid_paths() -> None:
    returns, labels = make_two_regime_with_labels()
    fit = fit_regime_garch(returns, labels, dataset_id=DATASET_ID)

    paths = simulate_regime_paths(fit, n_days=10, n_paths=100, seed=1)

    assert paths.shape == (100, 10)
    assert np.all(np.isfinite(paths))
    # daily returns in crisis regime should reach larger magnitudes
    assert np.abs(paths).max() > 0.01


def test_simulate_is_deterministic() -> None:
    returns, labels = make_two_regime_with_labels()
    fit = fit_regime_garch(returns, labels, dataset_id=DATASET_ID)
    a = simulate_regime_paths(fit, n_days=5, n_paths=10, seed=42)
    b = simulate_regime_paths(fit, n_days=5, n_paths=10, seed=42)
    assert np.array_equal(a, b)


def test_simulate_rejects_invalid_dims() -> None:
    returns, labels = make_two_regime_with_labels()
    fit = fit_regime_garch(returns, labels, dataset_id=DATASET_ID)
    with pytest.raises(ModelingError):
        simulate_regime_paths(fit, n_days=0, n_paths=10, seed=1)
