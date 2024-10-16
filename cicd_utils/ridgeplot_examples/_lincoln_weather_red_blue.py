from __future__ import annotations

from typing import TYPE_CHECKING

from ridgeplot_examples._lincoln_weather import main as lincoln_weather

if TYPE_CHECKING:
    import plotly.graph_objects as go


def main() -> go.Figure:
    fig = lincoln_weather(
        colorscale=(
            (0.0, "rgb(255, 60, 60)"),
            (1.0, "rgb(60, 60, 255)"),
        ),
        colormode="trace-index-row-wise",
    )
    return fig


if __name__ == "__main__":
    fig = main()
    fig.show()
