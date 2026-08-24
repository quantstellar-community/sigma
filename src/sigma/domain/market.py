"""Market data domain entities.

Implements the "Dataset & Market Data" group of docs/SCHEMA.md §7:
Asset identity, MarketObservation, CorporateAction.

Conventions follow ADR-0002: frozen entities, Decimal money fields,
UTC-aware timestamps (SCHEMA.md §7.5).
"""

from datetime import datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

__all__ = [
    "Asset",
    "AssetId",
    "AssetType",
    "CorporateAction",
    "CorporateActionType",
    "CurrencyCode",
    "MarketObservation",
]

_KEBAB_CASE = r"^[a-z0-9]+(-[a-z0-9]+)*$"

AssetId = Annotated[str, StringConstraints(pattern=_KEBAB_CASE)]
"""Stable Sigma-managed identifier, e.g. ``equity-aapl-us`` (ADR-0002 D4).

Convention: ``<asset_type>-<symbol>-<market>``, lowercase kebab-case."""

CurrencyCode = Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}$")]

Price = Annotated[Decimal, Field(ge=0)]


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        msg = "timestamp must be timezone-aware"
        raise ValueError(msg)
    if value.utcoffset() != timedelta(0):
        msg = "timestamp must be UTC (zero offset)"
        raise ValueError(msg)
    return value


def _decimal_from_float(value: object) -> object:
    """Coerce float input via ``str`` so binary rounding artifacts never leak."""
    if isinstance(value, float):
        return Decimal(str(value))
    return value


UtcTimestamp = Annotated[datetime, AfterValidator(_require_utc)]


class AssetType(StrEnum):
    EQUITY = "EQUITY"
    ETF = "ETF"
    INDEX = "INDEX"
    COMMODITY = "COMMODITY"
    FX = "FX"
    MACRO = "MACRO"


class CorporateActionType(StrEnum):
    DIVIDEND = "DIVIDEND"
    SPLIT = "SPLIT"


class Asset(BaseModel):
    """A tradable or observable financial instrument (SCHEMA.md §6)."""

    model_config = ConfigDict(frozen=True)

    asset_id: AssetId
    symbol: str
    asset_type: AssetType
    currency: CurrencyCode

    @field_validator("symbol")
    @classmethod
    def _symbol_not_blank(cls, value: str) -> str:
        if not value.strip():
            msg = "symbol must not be blank"
            raise ValueError(msg)
        return value


class MarketObservation(BaseModel):
    """One OHLCV market bar for one asset at one timestamp (SCHEMA.md §7.2).

    ``close`` is the raw traded price; ``adjusted_close`` is split/dividend
    adjusted. Returns are always computed from ``adjusted_close``.
    """

    model_config = ConfigDict(frozen=True)

    asset_id: AssetId
    timestamp: UtcTimestamp
    open: Price
    high: Price
    low: Price
    close: Price
    adjusted_close: Price
    volume: Annotated[Decimal | None, Field(default=None, ge=0)]
    dataset_id: str = Field(min_length=1)

    @field_validator(
        "open", "high", "low", "close", "adjusted_close", "volume", mode="before"
    )
    @classmethod
    def _coerce_prices(cls, value: object) -> object:
        return _decimal_from_float(value)

    @model_validator(mode="after")
    def _check_ohlc_consistency(self) -> "MarketObservation":
        if self.high < self.open or self.high < self.close:
            msg = "high must be >= max(open, close)"
            raise ValueError(msg)
        if self.low > self.open or self.low > self.close:
            msg = "low must be <= min(open, close)"
            raise ValueError(msg)
        return self


class CorporateAction(BaseModel):
    """A dividend or split event stored separately from prices (SCHEMA.md §7.4)."""

    model_config = ConfigDict(frozen=True)

    asset_id: AssetId
    timestamp: UtcTimestamp
    action_type: CorporateActionType
    amount: Annotated[Decimal, Field(gt=0)]
    dataset_id: str = Field(min_length=1)

    @field_validator("amount", mode="before")
    @classmethod
    def _coerce_amount(cls, value: object) -> object:
        return _decimal_from_float(value)
