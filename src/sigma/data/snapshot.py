"""Snapshot persistence: Parquet + YAML metadata sidecar (ADR-0003 D3).

A snapshot is an immutable pair ``{universe}__{stamp}.parquet`` +
``{universe}__{stamp}.parquet.meta.yaml``. The sidecar carries full
provenance plus a SHA-256 checksum of the Parquet bytes; loading verifies
the pair was never tampered with.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from typing import Annotated, Any

import pandas as pd
import yaml
from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from sigma.data.errors import DataValidationError
from sigma.domain import MarketObservation

__all__ = ["SnapshotMeta", "SnapshotPaths", "load_snapshot", "save_snapshot"]

_PRICE_COLUMNS = ("open", "high", "low", "close", "adjusted_close")
_FRAME_COLUMNS: tuple[str, ...] = (
    "asset_id",
    "timestamp",
    *_PRICE_COLUMNS,
    "volume",
    "dataset_id",
)


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        msg = "retrieved_at must be timezone-aware"
        raise ValueError(msg)
    if value.utcoffset() != timedelta(0):
        msg = "retrieved_at must be UTC"
        raise ValueError(msg)
    return value


class SnapshotMeta(BaseModel):
    """Provenance metadata stored beside every snapshot (SCHEMA.md §7.1)."""

    model_config = ConfigDict(frozen=True)

    schema_version: str = "1"
    universe: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    symbols: list[str] = Field(min_length=1)
    frequency: str = Field(min_length=1)
    calendar: str = Field(min_length=1)
    timezone: str = Field(min_length=1)
    retrieved_at: Annotated[datetime, AfterValidator(_require_utc)]
    period_start: date | None = None
    period_end: date | None = None
    rows: int = Field(ge=0)
    dropped_rows: int = Field(default=0, ge=0)


@dataclass(frozen=True)
class SnapshotPaths:
    prices: Path
    meta: Path


def save_snapshot(
    observations: list[MarketObservation],
    *,
    meta: SnapshotMeta,
    out_dir: Path,
) -> SnapshotPaths:
    """Write the immutable prices+metadata pair and return both paths."""
    stamp = meta.retrieved_at.strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    prices_path = out_dir / f"{meta.universe}__{stamp}.parquet"
    _to_frame(observations).to_parquet(prices_path, index=False)

    checksum = sha256(prices_path.read_bytes()).hexdigest()
    meta_path = Path(f"{prices_path}.meta.yaml")
    payload = {**meta.model_dump(mode="json"), "checksum_sha256": checksum}
    meta_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    return SnapshotPaths(prices=prices_path, meta=meta_path)


def load_snapshot(prices_path: Path) -> tuple[list[MarketObservation], SnapshotMeta]:
    """Read a snapshot back, verifying its checksum first."""
    prices_path = Path(prices_path)
    meta_path = Path(f"{prices_path}.meta.yaml")

    payload: dict[str, Any] = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    expected_checksum = payload.pop("checksum_sha256", "")
    actual_checksum = sha256(prices_path.read_bytes()).hexdigest()
    if actual_checksum != expected_checksum:
        msg = (
            f"snapshot integrity failure: checksum mismatch for {prices_path.name}"
            f"(expected {expected_checksum}, got {actual_checksum})"
        )
        raise DataValidationError(msg)

    meta = SnapshotMeta.model_validate(payload)
    frame = pd.read_parquet(prices_path)
    return [_row_to_observation(row) for row in frame.itertuples(index=False)], meta


def _to_frame(observations: list[MarketObservation]) -> pd.DataFrame:
    records = [
        {
            "asset_id": observation.asset_id,
            "timestamp": pd.Timestamp(observation.timestamp),
            **{column: str(getattr(observation, column)) for column in _PRICE_COLUMNS},
            "volume": None if observation.volume is None else str(observation.volume),
            "dataset_id": observation.dataset_id,
        }
        for observation in observations
    ]
    # dict insertion order already matches _FRAME_COLUMNS
    return pd.DataFrame(records)


def _row_to_observation(row: Any) -> MarketObservation:
    def as_decimal_str_or_none(value: Any) -> str | None:
        if value is None or pd.isna(value):
            return None
        return str(value)  # pydantic parses str -> Decimal

    payload = {
        "asset_id": row.asset_id,
        "timestamp": row.timestamp.to_pydatetime(),
        **{
            column: as_decimal_str_or_none(getattr(row, column))
            for column in _PRICE_COLUMNS
        },
        "volume": as_decimal_str_or_none(row.volume),
        "dataset_id": row.dataset_id,
    }
    return MarketObservation.model_validate(payload)
