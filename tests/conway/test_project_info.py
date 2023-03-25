"""Conway project information check."""

from src import conway


def test_project_info():
    """Conway version test."""

    assert conway.__version__ is not None
    assert conway.PROGRAM_NAME == "conway"
