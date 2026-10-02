"""Tests for volatility estimators (WP-4a, ADR-0006)."""

import math
from datetime import UTC, datetime

import numpy as np
import pytest

from sigma.modeling import ArchDiagnostics, VolatilityState
from sigma.modeling.errors import ModelingError
from sigma.modeling.volatility import (
    check_arch_effects,
    constant_sigma,
    ewma_sigma,
    rolling_sigma,
)

# ---------------------------------------------------------------- constant


def test_constant_sigma_hand_computed() -> None:
    sigma = constant_sigma(np.array([0.01, 0.03]))
    assert math.isclose(sigma, math.sqrt(0.0002))


def test_constant_sigma_requires_two_points() -> None:
    with pytest.raises(ModelingError):
        constant_sigma(np.array([0.01]))


# ---------------------------------------------------------------- rolling


def test_rolling_sigma_uses_last_window_only() -> None:
    returns = np.array([0.09, -0.09, 0.01, 0.02, 0.03])
    sigma = rolling_sigma(returns, window=3)
    assert math.isclose(sigma, 0.01)  # std(ddof=1) of [0.01, 0.02, 0.03]


def test_rolling_sigma_rejects_short_series() -> None:
    with pytest.raises(ModelingError):
        rolling_sigma(np.array([0.01, 0.02]), window=60)


# ------------------------------------------------------------------- ewma


def test_ewma_sigma_hand_computed_lambda_default() -> None:
    returns = np.array([0.01, -0.02])
    # init variance (population) = 0.000225
    # step 1: 0.94 * 0.000225 + 0.06 * 0.0001  = 0.00021750
    # step 2: 0.94 * 0.0002175 + 0.06 * 0.0004 = 0.00022845
    expected = math.sqrt(0.00022845)
    sigma = ewma_sigma(returns)
    assert math.isclose(sigma, expected, rel_tol=1e-12)


def test_ewma_sigma_respects_lambda_override() -> None:
    returns = np.array([0.01, -0.02, 0.03])
    assert ewma_sigma(returns, lam=0.5) != ewma_sigma(returns, lam=0.99)


def test_ewma_sigma_requires_two_points() -> None:
    with pytest.raises(ModelingError):
        ewma_sigma(np.array([0.01]))


# ------------------------------------------------------------ diagnostics


def test_diagnostics_report_no_arch_for_iid_noise() -> None:
    rng = np.random.default_rng(42)
    diagnostics = check_arch_effects(rng.normal(0.0, 0.01, size=500))
    assert isinstance(diagnostics, ArchDiagnostics)
    assert diagnostics.has_arch_effects is False


def test_diagnostics_detect_clustering() -> None:
    rng = np.random.default_rng(42)
    calm = rng.normal(0.0, 0.006, 400)
    wild = rng.normal(0.0, 0.025, 100)
    diagnostics = check_arch_effects(np.concatenate([calm, wild]))
    assert diagnostics.has_arch_effects is True


# --------------------------------------------------------------- entity


def test_volatility_state_annualizes_by_sqrt_252() -> None:
    state = VolatilityState(
        asset_id="equity-aapl-us",
        timestamp=datetime(2026, 8, 21, tzinfo=UTC),
        sigma_daily=0.01,
        method="garch-t",
        dataset_id="ds",
    )
    assert math.isclose(state.annualized, 0.01 * math.sqrt(252))
