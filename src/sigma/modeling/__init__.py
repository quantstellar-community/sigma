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

__all__ = [
    "AlignmentReport",
    "ModelingError",
    "ReturnMatrix",
    "price_to_float",
    "simple_returns",
    "to_log",
]
