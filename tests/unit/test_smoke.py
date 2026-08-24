"""Smoke tests: verify the sigma package is installed and importable."""

import sigma


def test_sigma_package_is_importable() -> None:
    assert sigma.__name__ == "sigma"
