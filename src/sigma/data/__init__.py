"""Sigma data layer: providers, validation gate, snapshot persistence.

Public entry points:
- ``load_universe`` / ``Universe``      — configs/universe.yaml handling
- ``run_download`` / ``main``          — full pipeline entry point
- ``fetch_raw`` / ``parse_observations`` — yfinance adapter
- ``save_snapshot`` / ``load_snapshot``  — Parquet + sidecar persistence
- ``validate_observations``            — WORKFLOW §4.2 gate
"""

from sigma.data.errors import DataValidationError
from sigma.data.snapshot import (
    SnapshotMeta,
    SnapshotPaths,
    load_snapshot,
    save_snapshot,
)
from sigma.data.universe import AssetSpec, Universe, load_universe
from sigma.data.validation import validate_observations

__all__ = [
    "AssetSpec",
    "DataValidationError",
    "SnapshotMeta",
    "SnapshotPaths",
    "Universe",
    "load_snapshot",
    "load_universe",
    "save_snapshot",
    "validate_observations",
]
