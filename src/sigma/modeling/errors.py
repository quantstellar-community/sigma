"""Modeling layer exceptions (WORKFLOW §21 "Modeling Failure")."""

__all__ = ["ModelingError"]


class ModelingError(ValueError):
    """Raised when a modeling computation cannot produce a trustworthy result."""
