"""Base exception for domain rule violations outside entity construction."""

__all__ = ["DomainValidationError"]


class DomainValidationError(ValueError):
    """Raised when a domain rule that spans multiple entities is violated.

    Construction-time field validation raises ``pydantic.ValidationError``.
    This hierarchy is reserved for rules checked across entities or during
    domain operations (e.g., portfolio weight sums).
    """
