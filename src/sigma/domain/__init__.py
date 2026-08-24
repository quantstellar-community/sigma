"""Sigma domain layer: shared financial concepts (SCHEMA.md).

Public API of the domain package. Import entities from here, not from
submodules, so internal restructuring never breaks consumers.
"""

from sigma.domain.errors import DomainValidationError
from sigma.domain.market import (
    Asset,
    AssetId,
    AssetType,
    CorporateAction,
    CorporateActionType,
    CurrencyCode,
    MarketObservation,
)

__all__ = [
    "Asset",
    "AssetId",
    "AssetType",
    "CorporateAction",
    "CorporateActionType",
    "CurrencyCode",
    "DomainValidationError",
    "MarketObservation",
]
