"""Integration: real snapshot -> HMM regimes on a real asset (skips without data)."""

from pathlib import Path

import numpy as np
import pytest

from sigma.data.snapshot import load_snapshot
from sigma.modeling import (
    characterize_regimes,
    fit_regime_model,
    label_regimes,
    select_k,
    simple_returns,
    to_log,
)

SNAPSHOT_DIR = Path("data/processed/prices")
_snapshots = sorted(SNAPSHOT_DIR.glob("research-universe-v1__*.parquet"))
LATEST_SNAPSHOT = _snapshots[-1] if _snapshots else None


@pytest.mark.skipif(
    LATEST_SNAPSHOT is None, reason="no local snapshot; run `make download`"
)
def test_hmm_detects_regimes_on_real_spy_returns() -> None:
    assert LATEST_SNAPSHOT is not None
    observations, _ = load_snapshot(LATEST_SNAPSHOT)
    returns_matrix = simple_returns(observations)

    log_returns = to_log(returns_matrix)
    spy = log_returns.values["etf-spy-us"].to_numpy()

    fit = fit_regime_model(spy, k=2, dataset_id=returns_matrix.dataset_id)
    char = characterize_regimes(fit, returns=spy)
    labels = label_regimes(char)

    # structural sanity on real data
    assert set(labels.values()) == {"Calm", "Crisis"}
    assert len(fit.most_likely_states) == len(spy)
    assert np.all(np.isfinite(fit.state_probabilities))

    calm_state = next(s for s, label in labels.items() if label == "Calm")
    crisis_state = next(s for s, label in labels.items() if label == "Crisis")
    calm_vol = char.annualized_vol[calm_state]
    crisis_vol = char.annualized_vol[crisis_state]
    assert 0.05 < calm_vol < 0.40  # sane SPY annualized vols
    assert crisis_vol > calm_vol

    selection = select_k(spy, candidates=(2, 3), dataset_id=returns_matrix.dataset_id)
    assert selection.best_k in (2, 3)
    print(
        f"\nSPY regimes k=2: Calm vol={calm_vol:.1%}, Crisis vol={crisis_vol:.1%}\n"
        f"select_k -> {selection.recommendation}"
    )
