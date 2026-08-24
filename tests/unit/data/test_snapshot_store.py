"""Tests for snapshot persistence: Parquet + YAML sidecar round-trip."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from sigma.data.errors import DataValidationError
from sigma.data.snapshot import SnapshotMeta, load_snapshot, save_snapshot
from sigma.domain import MarketObservation


def make_meta(**overrides) -> SnapshotMeta:
    defaults = {
        "universe": "research-universe-v1",
        "provider": "yfinance",
        "symbols": ["AAPL"],
        "frequency": "1d",
        "calendar": "NYSE",
        "timezone": "America/New_York",
        "retrieved_at": datetime(2026, 8, 24, 15, 30, tzinfo=UTC),
        "rows": 2,
        "dropped_rows": 0,
    }
    defaults.update(overrides)
    return SnapshotMeta.model_validate(defaults)


def make_observations() -> list[MarketObservation]:
    def obs(day: int) -> MarketObservation:
        return MarketObservation.model_validate(
            {
                "asset_id": "equity-aapl-us",
                "timestamp": datetime(2026, 8, day, tzinfo=UTC),
                "open": "229.50",
                "high": "231.20",
                "low": "228.80",
                "close": "230.10",
                "adjusted_close": "229.85",
                "volume": "54000000" if day == 17 else None,
                "dataset_id": "research-universe-v1__t0",
            }
        )

    return [obs(17), obs(18)]


def test_round_trip_preserves_observations_and_metadata(tmp_path) -> None:
    paths = save_snapshot(make_observations(), meta=make_meta(), out_dir=tmp_path)
    loaded_obs, loaded_meta = load_snapshot(paths.prices)

    assert loaded_obs == make_observations()
    assert loaded_meta == make_meta()
    assert loaded_obs[1].volume is None


def test_decimal_values_survive_exactly(tmp_path) -> None:
    exact = Decimal("230.101010101")
    observations = [
        MarketObservation.model_validate(
            {
                "asset_id": "equity-aapl-us",
                "timestamp": datetime(2026, 8, 17, tzinfo=UTC),
                "open": exact,
                "high": exact,
                "low": exact,
                "close": exact,
                "adjusted_close": exact,
                "volume": None,
                "dataset_id": "ds",
            }
        )
    ]
    paths = save_snapshot(observations, meta=make_meta(rows=1), out_dir=tmp_path)
    loaded, _ = load_snapshot(paths.prices)
    assert loaded[0].close == exact


def test_sidecar_contains_checksum_matching_parquet_bytes(tmp_path) -> None:
    import hashlib

    import yaml

    paths = save_snapshot(make_observations(), meta=make_meta(), out_dir=tmp_path)
    sidecar_text = paths.meta.read_text(encoding="utf-8").lower()
    actual = hashlib.sha256(paths.prices.read_bytes()).hexdigest()

    assert f"checksum_sha256: {actual}" in sidecar_text
    assert yaml.safe_load(paths.meta.read_text(encoding="utf-8"))["rows"] == 2


def test_load_detects_tampered_parquet(tmp_path) -> None:
    paths = save_snapshot(make_observations(), meta=make_meta(), out_dir=tmp_path)
    raw = bytearray(paths.prices.read_bytes())
    raw[-1] ^= 0xFF
    paths.prices.write_bytes(bytes(raw))

    with pytest.raises(DataValidationError, match="checksum"):
        load_snapshot(paths.prices)


def test_rejects_naive_retrieved_at(tmp_path) -> None:
    naive = datetime(2026, 8, 24, 15, 30)  # noqa: DTZ001 — intentionally naive
    with pytest.raises(Exception):  # noqa: B017 — pydantic wraps the ValueError
        make_meta(retrieved_at=naive)
