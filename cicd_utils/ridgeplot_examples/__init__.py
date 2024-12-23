from __future__ import annotations

from typing import TYPE_CHECKING

from ridgeplot_examples._base import Example

if TYPE_CHECKING:
    import plotly.graph_objects as go

__all__ = [
    "ALL_EXAMPLES",
    "Example",
]


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


ALL_EXAMPLES: list[Example] = [
    Example("basic", load_basic),
    Example("basic_hist", load_basic_hist),
    Example("lincoln_weather", load_lincoln_weather),
    Example("lincoln_weather_red_blue", load_lincoln_weather_red_blue),
    Example("probly", load_probly),
]
