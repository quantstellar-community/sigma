"""Tests for the yfinance adapter: fetch_raw + parse_observations."""

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import pandas as pd
import pytest
from yf_fixtures import make_yf_frame

from sigma.data import yfinance_loader as yfl
from sigma.data.errors import DataValidationError
from sigma.data.universe import Universe
from sigma.domain import MarketObservation

UNIVERSE_YAML = """
universe:
  name: research-universe-v1
  frequency: 1d
  calendar: NYSE
  timezone: America/New_York
  period:
    start: 2026-08-01
assets:
  - { asset_id: equity-aapl-us, symbol: AAPL, asset_type: EQUITY, currency: USD }
  - { asset_id: etf-gld-us, symbol: GLD, asset_type: ETF, currency: USD }
"""


def make_universe(tmp_path) -> Universe:
    path = tmp_path / "universe.yaml"
    path.write_text(UNIVERSE_YAML, encoding="utf-8")
    from sigma.data.universe import load_universe

    return load_universe(path)


def test_fetch_raw_requests_adjusted_and_raw_prices(monkeypatch, tmp_path) -> None:
    captured: dict = {}

    def fake_download(**kwargs):
        captured.update(kwargs)
        return make_yf_frame(["AAPL", "GLD"])

    monkeypatch.setattr(yfl.yf, "download", fake_download)
    yfl.fetch_raw(make_universe(tmp_path))

    assert captured["auto_adjust"] is False
    assert set(captured["tickers"]) == {"AAPL", "GLD"}
    assert captured["start"] == date(2026, 8, 1)


def test_parse_maps_symbols_to_asset_ids(tmp_path) -> None:
    result = yfl.parse_observations(
        make_yf_frame(["AAPL", "GLD"]),
        universe=make_universe(tmp_path),
        dataset_id="research-universe-v1__t0",
    )
    ids = {obs.asset_id for obs in result.observations}
    assert ids == {"equity-aapl-us", "etf-gld-us"}


def test_parse_produces_frozen_domain_observations(tmp_path) -> None:
    result = yfl.parse_observations(
        make_yf_frame(["AAPL"]), universe=make_universe(tmp_path), dataset_id="ds"
    )
    obs = result.observations[0]
    assert isinstance(obs, MarketObservation)
    assert obs.dataset_id == "ds"


def test_parse_converts_float_via_str_not_binary(tmp_path) -> None:
    universe = make_universe(tmp_path)
    frame = make_yf_frame(["AAPL"])
    result = yfl.parse_observations(frame, universe=universe, dataset_id="ds")

    first_close = frame[("Close", "AAPL")].iloc[0]
    assert Decimal(str(first_close)) in {obs.close for obs in result.observations}


def test_parse_drops_nan_rows_and_reports_count(tmp_path) -> None:
    universe = make_universe(tmp_path)
    frame = make_yf_frame(["AAPL"])
    frame.iloc[-1, frame.columns.get_loc(("Close", "AAPL"))] = float("nan")

    result = yfl.parse_observations(frame, universe=universe, dataset_id="ds")
    assert result.dropped_rows == 1
    assert len(result.observations) == 4


def test_parse_raises_on_symbol_missing_from_universe(tmp_path) -> None:
    frame = make_yf_frame(["AAPL", "TSLA"])
    with pytest.raises(DataValidationError, match="TSLA"):
        yfl.parse_observations(frame, universe=make_universe(tmp_path), dataset_id="ds")


def test_parse_raises_on_empty_frame(tmp_path) -> None:
    empty = pd.DataFrame(
        columns=pd.MultiIndex.from_tuples(
            [
                ("Close", "AAPL"),
                ("Adj Close", "AAPL"),
                ("High", "AAPL"),
                ("Low", "AAPL"),
                ("Open", "AAPL"),
                ("Volume", "AAPL"),
            ]
        )
    )
    with pytest.raises(DataValidationError):
        yfl.parse_observations(empty, universe=make_universe(tmp_path), dataset_id="ds")


def test_timestamps_are_utc_midnight_of_trading_day(tmp_path) -> None:
    result = yfl.parse_observations(
        make_yf_frame(["AAPL"]), universe=make_universe(tmp_path), dataset_id="ds"
    )
    ts = result.observations[0].timestamp
    assert ts.utcoffset() == timedelta(0)
    assert ts == datetime(2026, 8, 17, tzinfo=UTC)
