from __future__ import annotations

from typing import Callable

import plotly.graph_objects as go


def tighten_margins(fig: go.Figure) -> go.Figure:
    """Tighten the margins of a Plotly figure."""
    if fig.layout.margin != go.layout.Margin():
        # If the Figure's margins are different from the default values,
        # we'll assume that the user has set these values intentionally
        return fig
    # If the Figure has a title, we'll leave 40px of space at the top
    # None that this might not work well for all titles. E.g., if the
    # title has multiple lines, or if the font size is larger, etc.
    fig_has_title = fig.layout.title.text != ""
    margin_top = None if fig_has_title else 40
    fig = fig.update_layout(margin=dict(l=0, r=0, t=margin_top, b=40))
    return fig


def load_basic() -> go.Figure:
    from ._basic import main

    return main()


def load_lincoln_weather() -> go.Figure:
    from ._lincoln_weather import main

    return main()


def load_probly() -> go.Figure:
    from ._probly import main

    return main()


ALL_EXAMPLES: list[tuple[str, Callable[[], go.Figure]]] = [
    ("basic", load_basic),
    ("lincoln_weather", load_lincoln_weather),
    ("probly", load_probly),
]
