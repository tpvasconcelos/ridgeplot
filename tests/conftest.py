from typing import Any, Dict, Optional

import pytest


def _patch_plotly_show() -> None:
    """Monkey patch ``plotly.io.show`` as to not perform any rendering and,
    instead, simply call ``plotly.io._utils.validate_coerce_fig_to_dict``"""
    from typing import Union

    import plotly.io
    from plotly.graph_objs import Figure
    from plotly.io._utils import validate_coerce_fig_to_dict  # noqa

    def wrapped(
        fig: Union[Figure, dict],
        renderer: Optional[str] = None,
        validate: bool = True,
        **kwargs: Dict[str, Any],
    ) -> None:
        validate_coerce_fig_to_dict(fig, validate)

    plotly.io.show = wrapped


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
    _patch_plotly_show()
