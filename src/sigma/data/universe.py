"""Universe configuration model and loader (ADR-0003 D1).

A universe declares which assets Sigma knows about. It lives in
``configs/*.yaml`` — adding an asset never requires code changes.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

from sigma.domain import AssetId, AssetType, CurrencyCode

__all__ = ["AssetSpec", "Universe", "load_universe"]

_KEBAB_CASE = r"^[a-z0-9]+(-[a-z0-9]+)*$"


class AssetSpec(BaseModel):
    """One asset entry inside a universe file."""

    model_config = ConfigDict(frozen=True)

    asset_id: AssetId
    symbol: str = Field(min_length=1)
    asset_type: AssetType
    currency: CurrencyCode


class Universe(BaseModel):
    """The set of assets a download/risk analysis operates on."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(pattern=_KEBAB_CASE)
    frequency: str = Field(min_length=1)
    calendar: str = Field(min_length=1)
    timezone: str = Field(min_length=1)
    period_start: date
    assets: list[AssetSpec] = Field(min_length=1)

    @field_validator("assets")
    @classmethod
    def _no_duplicate_asset_ids(cls, value: list[AssetSpec]) -> list[AssetSpec]:
        ids = [asset.asset_id for asset in value]
        if len(ids) != len(set(ids)):
            msg = f"duplicate asset_id in universe: {ids}"
            raise ValueError(msg)
        return value

    def symbol_to_asset_id(self) -> dict[str, str]:
        return {asset.symbol: asset.asset_id for asset in self.assets}


def load_universe(path: Path) -> Universe:
    """Parse and validate a ``configs/universe.yaml`` file."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    spec = dict(raw["universe"])
    spec["period_start"] = spec.pop("period")["start"]
    spec["assets"] = raw["assets"]
    return Universe.model_validate(spec)
