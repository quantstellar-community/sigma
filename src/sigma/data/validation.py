"""Validation gate for canonical observations (WORKFLOW §4.2, ADR-0003 D6).

Data that fails here never reaches the risk engine.
"""

from __future__ import annotations

from datetime import datetime

from sigma.data.errors import DataValidationError
from sigma.domain import MarketObservation

__all__ = ["validate_observations"]


def validate_observations(
    observations: list[MarketObservation],
    required_symbols: dict[str, str],
) -> None:
    """Check duplicates, per-asset ordering, and universe coverage.

    ``required_symbols`` maps provider symbol -> Sigma asset_id.
    Raises ``DataValidationError`` on any violation.
    """
    if not observations and required_symbols:
        msg = f"validation failed: no data for required symbols {sorted(required_symbols)}"
        raise DataValidationError(msg)

    seen_pairs: set[tuple[str, datetime]] = set()
    last_timestamp_by_asset: dict[str, datetime] = {}

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

    covered_assets = {observation.asset_id for observation in observations}
    missing_symbols = [
        symbol
        for symbol, asset_id in required_symbols.items()
        if asset_id not in covered_assets
    ]
    if missing_symbols:
        msg = f"validation failed: no data for symbols {missing_symbols}"
        raise DataValidationError(msg)
