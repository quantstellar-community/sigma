"""Tests for Asset entity and AssetType enum."""

import pytest
from pydantic import ValidationError

from sigma.domain import Asset, AssetType


def make_asset(**overrides: object) -> Asset:
    defaults: dict[str, object] = {
        "asset_id": "equity-aapl-us",
        "symbol": "AAPL",
        "asset_type": "EQUITY",
        "currency": "USD",
    }
    defaults.update(overrides)
    return Asset.model_validate(defaults)


def test_creates_valid_asset() -> None:
    asset = make_asset()
    assert asset.asset_id == "equity-aapl-us"
    assert asset.symbol == "AAPL"
    assert asset.currency == "USD"


def test_asset_type_enum_members() -> None:
    assert {member.value for member in AssetType} == {
        "EQUITY",
        "ETF",
        "INDEX",
        "COMMODITY",
        "FX",
        "MACRO",
    }


def test_rejects_empty_asset_id() -> None:
    with pytest.raises(ValidationError):
        make_asset(asset_id="")


def test_rejects_uppercase_asset_id() -> None:
    with pytest.raises(ValidationError):
        make_asset(asset_id="Equity-AAPL-US")


def test_rejects_asset_id_with_spaces() -> None:
    with pytest.raises(ValidationError):
        make_asset(asset_id="equity aapl us")


def test_accepts_kebab_case_asset_id_with_digits() -> None:
    assert make_asset(asset_id="etf-spy2-us").asset_id == "etf-spy2-us"


def test_rejects_lowercase_currency() -> None:
    with pytest.raises(ValidationError):
        make_asset(currency="usd")


def test_rejects_wrong_currency_length() -> None:
    with pytest.raises(ValidationError):
        make_asset(currency="USDD")


def test_rejects_empty_symbol() -> None:
    with pytest.raises(ValidationError):
        make_asset(symbol="")


def test_rejects_unknown_asset_type() -> None:
    with pytest.raises(ValidationError):
        make_asset(asset_type="CRYPTO")


def test_asset_is_frozen() -> None:
    asset = make_asset()
    with pytest.raises(ValidationError):
        asset.symbol = "MSFT"
