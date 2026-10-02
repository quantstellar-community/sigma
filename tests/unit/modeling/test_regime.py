"""Tests for HMM regime layer (WP-4b, ADR-0009).

Synthetic series with KNOWN regime structure are the ground truth:
if the HMM cannot recover a structure we built by hand, it is wrong.
"""

import numpy as np
import pytest

from sigma.modeling.errors import ModelingError
from sigma.modeling.regime import (
    characterize_regimes,
    fit_regime_model,
    label_regimes,
    select_k,
)

DATASET_ID = "test-snapshot__t0"


def make_two_regime_series(
    n_calm: int = 400, n_crisis: int = 200, seed: int = 7
) -> np.ndarray:
    """Calm block (Gaussian, vol 0.005) followed by crisis block
    (Student-t df=3, scale 0.02 — genuinely fat-tailed, as crisis regimes are)."""
    rng = np.random.default_rng(seed)
    calm = rng.normal(0.0, 0.005, n_calm)
    crisis = rng.standard_t(df=3, size=n_crisis) * 0.02
    return np.concatenate([calm, crisis])


def make_three_regime_series(seed: int = 11) -> np.ndarray:
    """Calm (Gaussian, vol 0.003) → Volatile (Gaussian, vol 0.015)
    → Crisis (Student-t df=3, scale 0.02). Long blocks keep all three
    states identifiable to the Gaussian HMM."""
    rng = np.random.default_rng(seed)
    blocks = [
        rng.normal(0.0002, 0.003, 600),
        rng.normal(-0.0001, 0.015, 600),
        rng.standard_t(df=3, size=400) * 0.02,
    ]
    return np.concatenate(blocks)


# ---------------------------------------------------------------- fit


def test_fit_two_regimes_recovers_known_structure() -> None:
    returns = make_two_regime_series()
    fit = fit_regime_model(returns, k=2, dataset_id=DATASET_ID)

    assert fit.k == 2
    assert fit.dataset_id == DATASET_ID
    assert len(fit.most_likely_states) == len(returns)

    # The calm block must be dominated by ONE state and the crisis block
    # dominated by the OTHER state (HMM does not know the block boundary,
    # so we assert dominance, not perfect separation).
    first_half = fit.most_likely_states[:400]
    second_half = fit.most_likely_states[400:]
    dominant_first = np.bincount(first_half).argmax()
    dominant_second = np.bincount(second_half).argmax()
    assert np.mean(first_half == dominant_first) > 0.9
    assert np.mean(second_half == dominant_second) > 0.9
    assert dominant_first != dominant_second


def test_fit_is_deterministic_with_fixed_seed() -> None:
    returns = make_two_regime_series()
    a = fit_regime_model(returns, k=2, dataset_id=DATASET_ID)
    b = fit_regime_model(returns, k=2, dataset_id=DATASET_ID)
    assert np.array_equal(a.most_likely_states, b.most_likely_states)


def test_fit_produces_valid_transition_matrix() -> None:
    fit = fit_regime_model(make_two_regime_series(), k=2, dataset_id=DATASET_ID)
    assert fit.transition_matrix.shape == (2, 2)
    assert np.all(fit.transition_matrix >= 0)
    assert np.allclose(fit.transition_matrix.sum(axis=1), 1.0)
    # diagonal dominance => regimes persist (stylized fact)
    assert np.all(np.diag(fit.transition_matrix) > 0.5)


def test_fit_rejects_short_series() -> None:
    with pytest.raises(ModelingError):
        fit_regime_model(np.zeros(5), k=2, dataset_id=DATASET_ID)


def test_fit_rejects_invalid_k() -> None:
    with pytest.raises(ModelingError):
        fit_regime_model(make_two_regime_series(), k=0, dataset_id=DATASET_ID)


# ------------------------------------------------------- characterization


def test_characterization_orders_volatility_correctly() -> None:
    fit = fit_regime_model(make_two_regime_series(), k=2, dataset_id=DATASET_ID)
    char = characterize_regimes(fit, returns=make_two_regime_series())

    vols = {state: char.annualized_vol[state] for state in char.annualized_vol}
    sorted_by_vol = sorted(vols.items(), key=lambda item: item[1])
    assert sorted_by_vol[0][1] < sorted_by_vol[1][1]  # calm < crisis

    # durations from transition matrix must be positive and > 1 day
    assert all(char.duration[state] > 1.0 for state in char.duration)


def test_characterization_fat_tail_in_crisis_state() -> None:
    """Crisis state must show heavier tail than calm (measured, not assumed)."""
    fit = fit_regime_model(make_two_regime_series(), k=2, dataset_id=DATASET_ID)
    char = characterize_regimes(fit, returns=make_two_regime_series())

    calm_state = min(char.active_states, key=lambda s: char.annualized_vol[s])
    crisis_state = max(char.active_states, key=lambda s: char.annualized_vol[s])
    assert char.kurtosis[crisis_state] > char.kurtosis[calm_state]


# ------------------------------------------------------------------ labels


def test_labeling_assigns_meaningful_names() -> None:
    fit = fit_regime_model(make_two_regime_series(), k=2, dataset_id=DATASET_ID)
    char = characterize_regimes(fit, returns=make_two_regime_series())
    labels = label_regimes(char)

    assert set(labels.values()) == {"Calm", "Crisis"}
    assert len(set(labels.values())) == 2  # every state gets a distinct label


def test_labeling_three_regimes() -> None:
    returns = make_three_regime_series()
    fit = fit_regime_model(returns, k=3, dataset_id=DATASET_ID)
    char = characterize_regimes(fit, returns=returns)
    labels = label_regimes(char)

    # All three states must be active (not swallowed) and labeled.
    assert set(labels.values()) == {"Calm", "Volatile", "Crisis"}
    # vol ordering must map to label ordering
    vol_by_label = {labels[s]: char.annualized_vol[s] for s in labels}
    assert vol_by_label["Calm"] < vol_by_label["Volatile"] < vol_by_label["Crisis"]


# ------------------------------------------------------------- select_k


def test_select_k_prefers_two_for_two_regime_data() -> None:
    returns = make_two_regime_series()
    selection = select_k(returns, candidates=(2, 3), dataset_id=DATASET_ID)
    assert selection.best_k == 2
    assert set(selection.bic_by_k) == {2, 3}


def test_select_k_prefers_three_for_three_regime_data() -> None:
    returns = make_three_regime_series()
    selection = select_k(returns, candidates=(2, 3), dataset_id=DATASET_ID)
    assert selection.best_k == 3
