from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.graph_objects as go

if TYPE_CHECKING:
    from collections.abc import Callable


def tighten_margins(fig: go.Figure, px: int = 0) -> go.Figure:
    """Tighten the margins of a Plotly figure."""
    if fig.layout.margin != go.layout.Margin():
        # If the Figure's margins are different from the default values,
        # we'll assume that the user has set these values intentionally
        return fig
    # If the Figure does not have a title, we'll leave 40px of space at the
    # top to account for the Plotly toolbar. If the Figure does include
    # a title, we'll leave the top margin with the default value.
    margin_top = None if fig.layout.title.text else max(40, px)
    return fig.update_layout(margin=dict(l=px, r=px, t=margin_top, b=px))


def load_basic() -> go.Figure:
    from ._basic import main

    return main()


def load_basic_hist() -> go.Figure:
    from ._basic_hist import main

    return main()


def load_lincoln_weather() -> go.Figure:
    from ._lincoln_weather import main

    return main()


def load_lincoln_weather_red_blue() -> go.Figure:
    from ._lincoln_weather_red_blue import main

    return main()


def load_probly() -> go.Figure:
    from ._probly import main

    return main()


ALL_EXAMPLES: list[tuple[str, Callable[[], go.Figure]]] = [
    ("basic", load_basic),
    ("basic_hist", load_basic_hist),
    ("lincoln_weather", load_lincoln_weather),
    ("lincoln_weather_red_blue", load_lincoln_weather_red_blue),
    ("probly", load_probly),
]
