def pytest_sessionstart() -> None:
    import plotly.io

    # noinspection PyProtectedMember
    from plotly.io._utils import validate_coerce_fig_to_dict

    def wrapped(fig, renderer=None, validate=True, **kwargs):
        validate_coerce_fig_to_dict(fig, validate)

    plotly.io.show = wrapped
