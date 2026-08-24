"""Sigma modeling layer: statistical and financial computations.

Public API. Import from here, not from submodules.
"""

from sigma.modeling.errors import ModelingError
from sigma.modeling.returns import (
    AlignmentReport,
    ReturnMatrix,
    price_to_float,
    simple_returns,
    to_log,
)
from sigma.modeling.volatility import (
    ArchDiagnostics,
    VolatilityState,
    check_arch_effects,
    constant_sigma,
    ewma_sigma,
    garch_sigma,
    rolling_sigma,
)

__all__ = [
    "AlignmentReport",
    "ArchDiagnostics",
    "ModelingError",
    "ReturnMatrix",
    "VolatilityState",
    "check_arch_effects",
    "constant_sigma",
    "ewma_sigma",
    "garch_sigma",
    "price_to_float",
    "rolling_sigma",
    "simple_returns",
    "to_log",
]
