from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from collections.abc import Collection

    import plotly.graph_objects as go

    from ridgeplot._color.interpolation import SolidColormode
    from ridgeplot._types import Color, ColorScale


def main(
    colorscale: ColorScale | Collection[Color] | str | None = "Inferno",
    colormode: SolidColormode | Literal["fillgradient"] = "fillgradient",
) -> go.Figure:
    import numpy as np

    from ridgeplot import ridgeplot
    from ridgeplot.datasets import load_lincoln_weather

    df = load_lincoln_weather()

    months = df.index.month_name().unique()  # type: ignore[attr-defined]
    samples = [
        [
            df[df.index.month_name() == month]["Min Temperature [F]"],  # type: ignore[attr-defined]
            df[df.index.month_name() == month]["Max Temperature [F]"],  # type: ignore[attr-defined]
        ]
        for month in months
    ]

    fig = ridgeplot(
        samples=samples,
        labels=months,
        colorscale=colorscale,
        colormode=colormode,
        bandwidth=4,
        kde_points=np.linspace(-40, 110, 400),
        spacing=0.3,
    )
    fig.update_layout(
        title="Minimum and maximum daily temperatures in Lincoln, NE (2016)",
        height=600,
        width=800,
        font_size=14,
        plot_bgcolor="rgb(245, 245, 245)",
        xaxis_gridcolor="white",
        yaxis_gridcolor="white",
        xaxis_gridwidth=2,
        yaxis_title="Month",
        xaxis_title="Temperature [F]",
        showlegend=False,
    )

    return fig


if __name__ == "__main__":
    fig = main()
    fig.show()
