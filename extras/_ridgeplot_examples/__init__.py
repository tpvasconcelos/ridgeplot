from __future__ import annotations

from typing import Callable

import plotly.graph_objects as go


def normalize(fig: go.Figure) -> go.Figure:
    # Reduce the figure's margins to more tightly fit the chart
    # (only if the user hasn't already customized the margins!)
    if fig.layout.margin == go.layout.Margin():
        t = None if fig.layout.title.text else 40
        fig = fig.update_layout(margin=dict(l=0, r=0, t=t, b=40))

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
