"""Tests for the domain error hierarchy."""

from sigma.domain.errors import DomainValidationError


def test_domain_validation_error_is_value_error() -> None:
    assert issubclass(DomainValidationError, ValueError)


def test_domain_validation_error_can_be_caught_as_value_error() -> None:
    try:
        raise DomainValidationError("some domain rule violated")
    except ValueError as exc:
        assert str(exc) == "some domain rule violated"
