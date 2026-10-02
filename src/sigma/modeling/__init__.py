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
from sigma.modeling.regime_garch import (
    GARCHParams,
    RegimeGARCHFit,
    RegimeVolForecast,
    fit_regime_garch,
    forecast_regime_vol,
    simulate_regime_paths,
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
    rolling_sigma,
)

__all__ = [
    "AlignmentReport",
    "ArchDiagnostics",
    "GARCHParams",
    "KSelection",
    "ModelingError",
    "RegimeCharacterization",
    "RegimeFit",
    "RegimeGARCHFit",
    "RegimeVolForecast",
    "ReturnMatrix",
    "VolatilityState",
    "characterize_regimes",
    "check_arch_effects",
    "constant_sigma",
    "ewma_sigma",
    "fit_regime_garch",
    "fit_regime_model",
    "forecast_regime_vol",
    "label_regimes",
    "price_to_float",
    "rolling_sigma",
    "select_k",
    "simple_returns",
    "simulate_regime_paths",
    "to_log",
]
