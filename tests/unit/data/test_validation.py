"""Tests for the validation gate (WORKFLOW §4.2 subset, ADR-0003 D6)."""

from datetime import UTC, datetime

import pytest

from sigma.data.errors import DataValidationError
from sigma.data.validation import validate_observations
from sigma.domain import MarketObservation


def make_obs(
    asset_id: str = "equity-aapl-us", day: int = 17, month: int = 8
) -> MarketObservation:
    return MarketObservation.model_validate(
        {
            "asset_id": asset_id,
            "timestamp": datetime(2026, month, day, tzinfo=UTC),
            "open": "100",
            "high": "110",
            "low": "95",
            "close": "105",
            "adjusted_close": "104",
            "volume": None,
            "dataset_id": "ds",
        }
    )


REQUIRED_SYMBOLS = {"AAPL": "equity-aapl-us"}


def test_valid_observations_pass() -> None:
    validate_observations([make_obs(day=17), make_obs(day=18)], REQUIRED_SYMBOLS)


def test_duplicate_asset_timestamp_raises() -> None:
    with pytest.raises(DataValidationError, match="duplicate"):
        validate_observations([make_obs(day=17), make_obs(day=17)], REQUIRED_SYMBOLS)


def test_unsorted_timestamps_raise() -> None:
    with pytest.raises(DataValidationError, match="ordering"):
        validate_observations([make_obs(day=18), make_obs(day=17)], REQUIRED_SYMBOLS)


def test_symbol_without_any_observation_raises() -> None:
    only_aapl = [make_obs(day=17), make_obs(day=18)]
    with pytest.raises(DataValidationError, match="GLD"):
        validate_observations(
            only_aapl, {"AAPL": "equity-aapl-us", "GLD": "etf-gld-us"}
        )


def test_empty_collection_raises_when_symbols_required() -> None:
    with pytest.raises(DataValidationError):
        validate_observations([], REQUIRED_SYMBOLS)


def test_unexpected_missing_trading_day_raises() -> None:
    # 2026-08-19 is a Wednesday — a regular NYSE business day.
    observations = [make_obs(day=17), make_obs(day=18), make_obs(day=20)]
    with pytest.raises(DataValidationError, match="missing"):
        validate_observations(observations, REQUIRED_SYMBOLS)


def test_weekend_gap_does_not_trigger() -> None:
    # Friday 2026-08-21 then Monday 2026-08-24: weekend in between is fine.
    observations = [make_obs(day=21), make_obs(day=24)]
    validate_observations(observations, REQUIRED_SYMBOLS)


def test_nyse_holiday_does_not_trigger() -> None:
    # Labor Day 2026 falls on Monday 2026-09-07; skipping it must be accepted.
    observations = [make_obs(day=4, month=9), make_obs(day=8, month=9)]
    validate_observations(observations, REQUIRED_SYMBOLS)
