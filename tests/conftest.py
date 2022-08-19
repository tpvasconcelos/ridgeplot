from typing import Any, Dict

from pytest import Session


def _patch_plotly_show() -> None:
    """Monkey patch ``plotly.io.show`` as to not perform any rendering and,
    instead, simply call ``plotly.io._utils.validate_coerce_fig_to_dict``"""
    from typing import Union

    import plotly.io
    from plotly.graph_objs import Figure
    from plotly.io._utils import validate_coerce_fig_to_dict  # noqa

    def wrapped(
        fig: Union[Figure, dict],
        renderer: str = None,
        validate: bool = True,
        **kwargs: Dict[str, Any],
    ) -> None:
        validate_coerce_fig_to_dict(fig, validate)

    plotly.io.show = wrapped


def pytest_sessionstart(session: Session) -> None:
    """Called after the :py:class:`pytest.Session` object has been created and
    before performing collection and entering the run test loop.

    Args:
        session
            The pytest :py:class:`~pytest.Session` object.

    References:
    - https://docs.pytest.org/en/6.2.x/reference.html#initialization-hooks
    """
    _patch_plotly_show()
