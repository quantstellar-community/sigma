"""yfinance adapter (ADR-0003 D5).

The only module allowed to import yfinance. Converts provider output into
frozen canonical ``MarketObservation`` entities per the Sigma Data Contract
(ADR-0001): float -> Decimal via ``str``, timestamps localized to UTC,
symbols mapped through the universe config.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from datetime import date
from typing import Any

import pandas as pd
import yfinance as yf
from pydantic import BaseModel, ConfigDict, ValidationError

from sigma.data.errors import DataValidationError
from sigma.data.universe import Universe
from sigma.domain import MarketObservation

__all__ = ["ParseResult", "fetch_raw", "parse_observations"]

_PRICE_FIELDS = ("Open", "High", "Low", "Close", "Adj Close")
_REQUIRED_COLUMNS = (*_PRICE_FIELDS, "Volume")


def fetch_raw(universe: Universe, end: date | None = None) -> pd.DataFrame:
    """Download raw daily bars from Yahoo Finance (the network boundary).

    ``auto_adjust=False`` keeps raw Close and adds Adj Close separately —
    required by the canonical schema (SCHEMA.md §7.2).
    """
    frame = yf.download(
        tickers=[asset.symbol for asset in universe.assets],
        start=universe.period_start,
        end=end,
        auto_adjust=False,
        progress=False,
    )
    if frame is None:
        msg = "yfinance download returned None"
        raise DataValidationError(msg)
    return frame


class ParseResult(BaseModel):
    """Canonical observations plus honest accounting of what was dropped."""

    model_config = ConfigDict(frozen=True)

    observations: list[MarketObservation]
    dropped_rows: int


def parse_observations(
    frame: pd.DataFrame,
    *,
    universe: Universe,
    dataset_id: str,
) -> ParseResult:
    """Convert a provider DataFrame into canonical MarketObservations."""
    if frame.empty:
        msg = "provider returned no data"
        raise DataValidationError(msg)

    available_symbols = set(frame.columns.get_level_values(-1))
    unknown = available_symbols - set(universe.symbol_to_asset_id())
    if unknown:
        msg = f"symbols not declared in universe: {sorted(unknown)}"
        raise DataValidationError(msg)

    observations: list[MarketObservation] = []
    dropped_rows = 0

    for asset in universe.assets:
        if asset.symbol not in available_symbols:
            continue
        bars = frame.xs(asset.symbol, axis=1, level=-1)
        _require_columns(bars, asset.symbol)

        for index, row in bars.iterrows():
            values = {name: row[name] for name in _REQUIRED_COLUMNS}
            if any(_is_missing(values[name]) for name in _PRICE_FIELDS):
                dropped_rows += 1
                continue

            observations.append(
                _to_observation(
                    asset_id=asset.asset_id,
                    timestamp=index,
                    values=values,
                    dataset_id=dataset_id,
                )
            )

    return ParseResult(observations=observations, dropped_rows=dropped_rows)


def _require_columns(bars: pd.DataFrame, symbol: str) -> None:
    missing = [column for column in _REQUIRED_COLUMNS if column not in bars.columns]
    if missing:
        msg = f"missing columns {missing} for symbol {symbol}"
        raise DataValidationError(msg)


def _is_missing(value: object) -> bool:
    # numpy floats subclass Python float, so this catches NaN from pandas too.
    return value is None or (isinstance(value, float) and math.isnan(value))


def _to_observation(
    *,
    asset_id: str,
    timestamp: Any,
    values: Mapping[str, object],
    dataset_id: str,
) -> MarketObservation:
    ts = pd.Timestamp(timestamp).tz_localize("UTC").to_pydatetime()
    payload = {
        "asset_id": asset_id,
        "timestamp": ts,
        "open": values["Open"],
        "high": values["High"],
        "low": values["Low"],
        "close": values["Close"],
        "adjusted_close": values["Adj Close"],
        "volume": None if _is_missing(values["Volume"]) else values["Volume"],
        "dataset_id": dataset_id,
    }
    try:
        return MarketObservation.model_validate(payload)
    except ValidationError as exc:
        msg = f"invalid observation for {asset_id} at {timestamp}"
        raise DataValidationError(msg) from exc
