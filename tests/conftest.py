import pytest

from ridgeplot._testing import patch_plotly_show


def pytest_sessionstart(session: pytest.Session) -> None:
    """Called after the :class:`pytest.Session` object has been created and
    before performing collection and entering the run test loop.

    Parameters
    ----------
    session
        The pytest :class:`~pytest.Session` object.

    References
    ----------
    https://docs.pytest.org/en/stable/reference.html#initialization-hooks

    ..
        Ignore the following `flake8-docstrings` errors:
        # noqa: D401
    """
    patch_plotly_show()
