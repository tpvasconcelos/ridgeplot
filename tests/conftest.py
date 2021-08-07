from pytest import Session


def _patch_plotly_show() -> None:
    """Monkey patch ``plotly.io.show`` as to not perform any rendering and,
    instead, simply call ``plotly.io._utils.validate_coerce_fig_to_dict``"""
    import plotly.io

    # noinspection PyProtectedMember
    from plotly.io._utils import validate_coerce_fig_to_dict

    def wrapped(fig, renderer=None, validate=True, **kwargs):
        validate_coerce_fig_to_dict(fig, validate)

    plotly.io.show = wrapped


def pytest_sessionstart(session: Session) -> None:
    """Called after the ``Session`` object has been created and before
    performing collection and entering the run test loop.

    :param pytest.Session session: The pytest session object.

    References
    ----------
      * https://docs.pytest.org/en/6.2.x/reference.html#initialization-hooks
    """
    _patch_plotly_show()
