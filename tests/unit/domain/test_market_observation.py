"""Tests for MarketObservation entity."""

from datetime import UTC, datetime, timedelta, timezone
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError

from sigma.domain import MarketObservation

UTC_AWARE_TS = datetime(2026, 8, 21, 14, 30, tzinfo=UTC)


def make_observation(**overrides: object) -> MarketObservation:
    defaults: dict[str, object] = {
        "asset_id": "equity-aapl-us",
        "timestamp": UTC_AWARE_TS,
        "open": Decimal("229.50"),
        "high": Decimal("231.20"),
        "low": Decimal("228.80"),
        "close": Decimal("230.10"),
        "adjusted_close": Decimal("229.85"),
        "volume": Decimal(54_321_000),
        "dataset_id": "market-universe-v1",
    }
    defaults.update(overrides)
    return MarketObservation.model_validate(defaults)


def test_creates_valid_observation() -> None:
    obs = make_observation()
    assert obs.asset_id == "equity-aapl-us"
    assert obs.close == Decimal("230.10")
    assert obs.volume is not None


def test_volume_is_optional() -> None:
    obs = make_observation(volume=None)
    assert obs.volume is None


def test_prices_are_decimal_not_float() -> None:
    obs = make_observation(close=230.10)
    assert isinstance(obs.close, Decimal)
    assert obs.close == Decimal("230.10")


def test_rejects_naive_timestamp() -> None:
    naive = datetime(2026, 8, 21, 14, 30)  # noqa: DTZ001 — intentionally naive
    with pytest.raises(ValidationError):
        make_observation(timestamp=naive)


def test_rejects_non_utc_timezone() -> None:
    ny = datetime(2026, 8, 21, 10, 30, tzinfo=ZoneInfo("America/New_York"))
    with pytest.raises(ValidationError):
        make_observation(timestamp=ny)


@pytest.mark.parametrize(
    "field",
    ["open", "high", "low", "close", "adjusted_close"],
)
def test_rejects_negative_price(field: str) -> None:
    with pytest.raises(ValidationError):
        make_observation(**{field: Decimal("-0.01")})


def test_rejects_high_below_close() -> None:
    with pytest.raises(ValidationError):
        make_observation(high=Decimal("229.00"), close=Decimal("230.10"))


def test_rejects_low_above_open() -> None:
    with pytest.raises(ValidationError):
        make_observation(low=Decimal("230.00"), open=Decimal("229.50"))


def test_rejects_negative_volume() -> None:
    with pytest.raises(ValidationError):
        make_observation(volume=Decimal(-1))


def test_observation_is_frozen() -> None:
    obs = make_observation()
    with pytest.raises(ValidationError):
        obs.close = Decimal("999.00")


def test_equal_observations_with_same_values_compare_equal() -> None:
    a, b = make_observation(), make_observation()
    assert a == b


def test_accepts_boundary_ohlc_where_high_equals_close() -> None:
    obs = make_observation(
        open=Decimal(100),
        high=Decimal(110),
        low=Decimal(95),
        close=Decimal(110),
    )
    assert obs.high == Decimal(110)


def test_accepts_zero_offset_custom_timezone() -> None:
    ts = datetime(2026, 8, 21, 14, 30, tzinfo=timezone(timedelta(hours=0), "ANY"))
    assert make_observation(timestamp=ts).timestamp == ts
