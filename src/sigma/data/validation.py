"""Validation gate for canonical observations (WORKFLOW §4.2, ADR-0003 D6).

Data that fails here never reaches the risk engine. Checks:
duplicates, per-asset ordering, universe coverage, and NYSE
calendar completeness (no silently swallowed trading days).
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from importlib import import_module
from typing import TYPE_CHECKING

from sigma.data.errors import DataValidationError
from sigma.domain import MarketObservation

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = ["validate_observations"]

_CALENDAR_MODULE = "QuantLib"


def _nyse_calendar():
    ql = import_module(_CALENDAR_MODULE)
    return ql.UnitedStates(ql.UnitedStates.NYSE)


def _is_nyse_business_day(calendar, value: date) -> bool:
    ql = import_module(_CALENDAR_MODULE)
    return bool(calendar.isBusinessDay(ql.Date(value.day, value.month, value.year)))


def _unexpected_missing_trading_days(
    timestamps: Sequence[datetime],
) -> list[date]:
    """Return NYSE business days absent between first and last observation."""
    if len(timestamps) < 2:
        return []

    calendar = _nyse_calendar()
    present = {timestamp.date() for timestamp in timestamps}
    missing: list[date] = []

    current = timestamps[0].date()
    end = timestamps[-1].date()
    while current <= end:
        if current not in present and _is_nyse_business_day(calendar, current):
            missing.append(current)
        current += timedelta(days=1)
    return missing


def validate_observations(
    observations: list[MarketObservation],
    required_symbols: dict[str, str],
) -> None:
    """Check duplicates, ordering, coverage and calendar completeness.

    ``required_symbols`` maps provider symbol -> Sigma asset_id.
    Raises ``DataValidationError`` on any violation.
    """
    if not observations and required_symbols:
        msg = f"validation failed: no data for required symbols {sorted(required_symbols)}"
        raise DataValidationError(msg)

    seen_pairs: set[tuple[str, datetime]] = set()
    last_timestamp_by_asset: dict[str, datetime] = {}
    timestamps_by_asset: dict[str, list[datetime]] = {}

    for observation in observations:
        pair = (observation.asset_id, observation.timestamp)
        if pair in seen_pairs:
            msg = (
                "validation failed: duplicate observation "
                f"{observation.asset_id} @ {observation.timestamp}"
            )
            raise DataValidationError(msg)
        seen_pairs.add(pair)

        previous = last_timestamp_by_asset.get(observation.asset_id)
        if previous is not None and observation.timestamp <= previous:
            msg = (
                "validation failed: timestamp ordering violated for "
                f"{observation.asset_id} at {observation.timestamp}"
            )
            raise DataValidationError(msg)
        last_timestamp_by_asset[observation.asset_id] = observation.timestamp
        timestamps_by_asset.setdefault(observation.asset_id, []).append(
            observation.timestamp
        )

    covered_assets = set(timestamps_by_asset)
    missing_symbols = [
        symbol
        for symbol, asset_id in required_symbols.items()
        if asset_id not in covered_assets
    ]
    if missing_symbols:
        msg = f"validation failed: no data for symbols {missing_symbols}"
        raise DataValidationError(msg)

    for asset_id in sorted(timestamps_by_asset):
        holes = _unexpected_missing_trading_days(timestamps_by_asset[asset_id])
        if holes:
            preview = ", ".join(str(day) for day in holes[:3])
            msg = (
                f"validation failed: asset {asset_id} unexpectedly missing "
                f"{len(holes)} NYSE trading day(s), e.g. {preview}"
            )
            raise DataValidationError(msg)
