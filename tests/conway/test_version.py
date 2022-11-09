"""Conway version check."""

from src import conway


def test_version_info():
    """Euler version test."""
    assert conway.__version__ is not None
