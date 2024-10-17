from __future__ import annotations

from typing import TYPE_CHECKING

from ridgeplot_examples._lincoln_weather import main as lincoln_weather

if TYPE_CHECKING:
    import plotly.graph_objects as go


def main() -> go.Figure:
    fig = lincoln_weather(
        colorscale=["orangered", "deepskyblue"],
        colormode="trace-index-row-wise",
    )
    return fig


if __name__ == "__main__":
    fig = main()
    fig.show()
