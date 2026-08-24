"""Tests for CorporateAction entity."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from sigma.domain import CorporateAction

TS = datetime(2026, 8, 12, 0, 0, tzinfo=UTC)


def make_action(**overrides: object) -> CorporateAction:
    defaults: dict[str, object] = {
        "asset_id": "equity-aapl-us",
        "timestamp": TS,
        "action_type": "DIVIDEND",
        "amount": Decimal("0.26"),
        "dataset_id": "market-universe-v1",
    }
    defaults.update(overrides)
    return CorporateAction.model_validate(defaults)


def test_creates_valid_dividend_action() -> None:
    action = make_action()
    assert action.action_type == "DIVIDEND"
    assert action.amount == Decimal("0.26")


def test_creates_valid_split_action() -> None:
    action = make_action(action_type="SPLIT", amount=Decimal(4))
    assert action.action_type == "SPLIT"


def test_rejects_zero_amount() -> None:
    with pytest.raises(ValidationError):
        make_action(amount=Decimal(0))


def test_rejects_negative_amount() -> None:
    with pytest.raises(ValidationError):
        make_action(amount=Decimal("-1.5"))


def test_rejects_unknown_action_type() -> None:
    with pytest.raises(ValidationError):
        make_action(action_type="MERGER")


def test_rejects_naive_timestamp() -> None:
    naive = datetime(2026, 8, 12, 0, 0)  # noqa: DTZ001 — intentionally naive
    with pytest.raises(ValidationError):
        make_action(timestamp=naive)


def test_corporate_action_is_frozen() -> None:
    action = make_action()
    with pytest.raises(ValidationError):
        action.amount = Decimal(99)
