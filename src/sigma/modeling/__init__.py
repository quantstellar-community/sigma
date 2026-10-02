"""Sigma modeling layer: statistical and financial computations.

Public API. Import from here, not from submodules.
"""

from sigma.modeling.errors import ModelingError
from sigma.modeling.regime import (
    KSelection,
    RegimeCharacterization,
    RegimeFit,
    characterize_regimes,
    fit_regime_model,
    label_regimes,
    select_k,
)
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
    "KSelection",
    "ModelingError",
    "RegimeCharacterization",
    "RegimeFit",
    "ReturnMatrix",
    "VolatilityState",
    "characterize_regimes",
    "check_arch_effects",
    "constant_sigma",
    "ewma_sigma",
    "fit_regime_model",
    "garch_sigma",
    "label_regimes",
    "price_to_float",
    "rolling_sigma",
    "select_k",
    "simple_returns",
    "to_log",
]
