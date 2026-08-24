"""Integration: real snapshot -> canonical returns (skips without local data)."""

from pathlib import Path

import pandas as pd
import pytest

from sigma.data.snapshot import load_snapshot
from sigma.modeling import simple_returns, to_log

SNAPSHOT_DIR = Path("data/processed/prices")
_snapshots = sorted(SNAPSHOT_DIR.glob("research-universe-v1__*.parquet"))
LATEST_SNAPSHOT = _snapshots[-1] if _snapshots else None


@pytest.mark.skipif(
    LATEST_SNAPSHOT is None, reason="no local snapshot; run `make download`"
)
def test_real_snapshot_produces_clean_return_matrix() -> None:
    assert LATEST_SNAPSHOT is not None
    observations, snapshot_meta = load_snapshot(LATEST_SNAPSHOT)

    matrix = simple_returns(observations)
    values = matrix.values

    assert values.shape[1] == 12
    assert len(values) > 2000
    assert bool(values.isna().to_numpy().any()) is False
    assert isinstance(values.index, pd.DatetimeIndex)
    assert values.index.is_monotonic_increasing
    assert matrix.dataset_id.startswith(snapshot_meta.universe + "__")

    log_matrix = to_log(matrix)
    assert log_matrix.method == "LOG"
    assert log_matrix.values.shape == values.shape
