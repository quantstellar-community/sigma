"""Deterministic yfinance-like fixtures for offline loader tests.

Builds DataFrames shaped exactly like ``yf.download(..., auto_adjust=False)``
output: MultiIndex columns (price field level, ticker level) over a naive
daily DatetimeIndex.
"""

from __future__ import annotations

import pandas as pd

FIELDS = ["Adj Close", "Close", "High", "Low", "Open", "Volume"]

# Hand-written, deterministic base prices so tests never depend on the network.
_BASE_PRICES: dict[str, float] = {"AAPL": 230.0, "GLD": 245.0}

_DATES = pd.bdate_range("2026-08-17", periods=5)


def make_yf_frame(symbols: list[str]) -> pd.DataFrame:
    """Return a MultiIndex DataFrame mimicking yfinance daily download output."""
    columns: dict[tuple[str, str], list[float]] = {}
    for symbol in symbols:
        base = _BASE_PRICES.get(symbol)
        if base is None:
            base = 100.0
        day_drift = [0.0, 0.5, -0.4, 0.9, 0.2]
        adj = [round(base + d, 2) for d in day_drift]
        raw = [round(a + 0.15, 2) for a in adj]
        high = [round(r + 1.2, 2) for r in raw]
        low = [round(r - 1.3, 2) for r in raw]
        opn = [round(l + 0.6, 2) for l in low]
        vol = [54_000_000.0 + i * 1_000.0 for i in range(len(_DATES))]
        columns.update(
            {
                ("Adj Close", symbol): adj,
                ("Close", symbol): raw,
                ("High", symbol): high,
                ("Low", symbol): low,
                ("Open", symbol): opn,
                ("Volume", symbol): vol,
            }
        )

    multi_columns = pd.MultiIndex.from_tuples(
        sorted(columns.keys()), names=["Price", "Ticker"]
    )
    data = {key: columns[key] for key in multi_columns}
    return pd.DataFrame(data, index=_DATES, columns=multi_columns)
