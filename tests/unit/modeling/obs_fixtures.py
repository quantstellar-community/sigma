"""Deterministic MarketObservation fixtures for returns tests."""

from datetime import UTC, datetime

from sigma.domain import MarketObservation

DATASET_ID = "test-snapshot__t0"

_BASE_PRICES: dict[str, str] = {}


def make_obs(
    asset_id: str,
    day: int,
    adjusted_close: str,
    *,
    dataset_id: str = DATASET_ID,
) -> MarketObservation:
    """Build one observation; adjusted_close drives everything (raw = +1%)."""
    adj = adjusted_close
    raw = str(round(float(adj) * 1.01, 4))
    high = str(float(adj) * 1.02)
    low = str(float(adj) * 0.98)
    opn = str(float(low) + 0.5)
    return MarketObservation.model_validate(
        {
            "asset_id": asset_id,
            "timestamp": datetime(2026, 8, day, tzinfo=UTC),
            "open": opn,
            "high": high,
            "low": low,
            "close": raw,
            "adjusted_close": adj,
            "volume": "1000000",
            "dataset_id": dataset_id,
        }
    )
