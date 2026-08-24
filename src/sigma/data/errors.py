"""Data layer exceptions."""

__all__ = ["DataValidationError"]


class DataValidationError(ValueError):
    """Raised when market data fails the validation gate (WORKFLOW §4.2).

    The risk engine must never receive data that failed validation.
    """
