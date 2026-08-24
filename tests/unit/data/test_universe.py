"""Tests for universe config parsing (configs/universe.yaml)."""

import pytest
from pydantic import ValidationError

from sigma.data.universe import load_universe

VALID_YAML = """
universe:
  name: research-universe-v1
  frequency: 1d
  calendar: NYSE
  timezone: America/New_York
  period:
    start: 2015-01-01
assets:
  - { asset_id: equity-aapl-us, symbol: AAPL, asset_type: EQUITY, currency: USD }
  - { asset_id: etf-gld-us, symbol: GLD, asset_type: ETF, currency: USD }
"""


def write(tmp_path, text: str):
    path = tmp_path / "universe.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_loads_valid_universe(tmp_path) -> None:
    universe = load_universe(write(tmp_path, VALID_YAML))
    assert universe.name == "research-universe-v1"
    assert universe.period_start.isoformat() == "2015-01-01"
    assert len(universe.assets) == 2


def test_symbols_lookup_is_available(tmp_path) -> None:
    universe = load_universe(write(tmp_path, VALID_YAML))
    assert universe.symbol_to_asset_id() == {
        "AAPL": "equity-aapl-us",
        "GLD": "etf-gld-us",
    }


def test_rejects_duplicate_asset_ids(tmp_path) -> None:
    duplicated = VALID_YAML.replace(
        "{ asset_id: etf-gld-us,", "{ asset_id: equity-aapl-us,"
    )
    with pytest.raises(ValidationError, match="duplicate"):
        load_universe(write(tmp_path, duplicated))


def test_rejects_invalid_asset_id_format(tmp_path) -> None:
    bad = VALID_YAML.replace("equity-aapl-us", "Equity AAPL")
    with pytest.raises(ValidationError):
        load_universe(write(tmp_path, bad))


def test_rejects_empty_assets_list(tmp_path) -> None:
    bad = VALID_YAML.split("assets:")[0] + "assets: []\n"
    with pytest.raises(ValidationError):
        load_universe(write(tmp_path, bad))


def test_rejects_unknown_asset_type(tmp_path) -> None:
    bad = VALID_YAML.replace("asset_type: EQUITY", "asset_type: CRYPTO")
    with pytest.raises(ValidationError):
        load_universe(write(tmp_path, bad))
