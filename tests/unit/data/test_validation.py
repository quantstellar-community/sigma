"""Tests for the validation gate (WORKFLOW §4.2 subset, ADR-0003 D6)."""

from datetime import UTC, datetime

import pytest

from sigma.data.errors import DataValidationError
from sigma.data.validation import validate_observations
from sigma.domain import MarketObservation


def make_obs(asset_id: str = "equity-aapl-us", day: int = 17) -> MarketObservation:
    return MarketObservation.model_validate(
        {
            "asset_id": asset_id,
            "timestamp": datetime(2026, 8, day, tzinfo=UTC),
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
