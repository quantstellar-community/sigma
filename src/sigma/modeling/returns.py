"""Asset returns computation (WP-3, ADR-0005).

First financial computation of Sigma: canonical simple returns derived from
``adjusted_close``, log returns as explicit derived representation.

Conventions (SCHEMA.md §18):
- SIMPLE is canonical: R_t = adjusted_close_t / adjusted_close_{t-1} - 1
- LOG is derived:      r_t = ln(1 + R_t), conversion always via ``to_log``
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal

import numpy as np
import pandas as pd

from sigma.domain import MarketObservation
from sigma.modeling.errors import ModelingError

__all__ = [
    "AlignmentReport",
    "ReturnMatrix",
    "price_to_float",
    "simple_returns",
    "to_log",
]


def price_to_float(value: Decimal) -> float:
    """The single Decimal -> float boundary of the modeling layer (ADR-0002 D3)."""
    return float(value)


@dataclass(frozen=True)
class AlignmentReport:
    """Mandatory accounting of every row that did not survive alignment."""

    asset_days: dict[str, int]
    aligned_price_days: int
    dropped_by_alignment: dict[str, int]
    return_days: int


@dataclass(frozen=True)
class ReturnMatrix:
    """Aligned return matrix with provenance back to its source snapshot."""

    values: pd.DataFrame
    method: Literal["SIMPLE", "LOG"]
    dataset_id: str
    meta: AlignmentReport


def simple_returns(observations: list[MarketObservation]) -> ReturnMatrix:
    """Compute canonical simple returns on the common trading-day grid.

    Prices are inner-aligned across assets first (SCHEMA.md §7.5); every
    dropped day is reported in :class:`AlignmentReport`.
    """
    if not observations:
        msg = "no observations provided"
        raise ModelingError(msg)

    dataset_ids = {observation.dataset_id for observation in observations}
    if len(dataset_ids) > 1:
        msg = f"observations mix multiple dataset_id values: {sorted(dataset_ids)}"
        raise ModelingError(msg)
    dataset_id = observations[0].dataset_id

    price_grid: dict[str, dict[datetime, float]] = {}
    for observation in observations:
        asset_series = price_grid.setdefault(observation.asset_id, {})
        asset_series[observation.timestamp] = price_to_float(observation.adjusted_close)

    asset_days = {asset_id: len(series) for asset_id, series in price_grid.items()}

    aligned = (
        pd.concat(
            [
                pd.Series(series, name=asset_id)
                for asset_id, series in sorted(price_grid.items())
            ],
            axis=1,
        )
        .sort_index()
        .dropna(axis=0, how="any")
    )

    _require_at_least_two_rows(aligned, asset_days)

    returns = aligned / aligned.shift(1) - 1
    values = returns.iloc[1:].astype(np.float64)

    report = AlignmentReport(
        asset_days=asset_days,
        aligned_price_days=len(aligned),
        dropped_by_alignment={
            asset_id: asset_days[asset_id] - len(aligned)
            for asset_id in aligned.columns
        },
        return_days=len(values),
    )
    return ReturnMatrix(
        values=values, method="SIMPLE", dataset_id=dataset_id, meta=report
    )


def to_log(matrix: ReturnMatrix) -> ReturnMatrix:
    """Explicit SIMPLE -> LOG conversion: r = ln(1 + R)."""
    log_values = pd.DataFrame(
        np.log1p(matrix.values.to_numpy()),
        index=matrix.values.index,
        columns=matrix.values.columns,
    )
    return ReturnMatrix(
        values=log_values,
        method="LOG",
        dataset_id=matrix.dataset_id,
        meta=matrix.meta,
    )


def _require_at_least_two_rows(
    aligned: pd.DataFrame, asset_days: dict[str, int]
) -> None:
    if len(aligned) >= 2:
        return
    detail = ", ".join(
        f"{asset_id}={asset_days[asset_id]}" for asset_id in sorted(asset_days)
    )
    msg = (
        f"alignment left only {len(aligned)} common trading day(s); "
        f"cannot compute returns; input days per asset: {detail}"
    )
    raise ModelingError(msg)
