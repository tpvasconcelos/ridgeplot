from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import plotly.graph_objects as go


def main(
    color_discrete_map: dict[str, str] | None = None,
) -> go.Figure:
    import numpy as np

    from ridgeplot import ridgeplot
    from ridgeplot.datasets import load_lincoln_weather

    df = load_lincoln_weather()

    months = df.index.month_name().unique()  # pyright: ignore[reportAttributeAccessIssue]
    samples = [
        [
            df[df.index.month_name() == month]["Min Temperature [F]"],  # pyright: ignore[reportAttributeAccessIssue]
            df[df.index.month_name() == month]["Max Temperature [F]"],  # pyright: ignore[reportAttributeAccessIssue]
        ]
        for month in months
    ]

    fig = ridgeplot(
        samples=samples,
        labels=[["Min Temperatures", "Max Temperatures"]] * len(months),
        row_labels=months,
        legendgroup=True,
        colorscale="Inferno",
        color_discrete_map=color_discrete_map,
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
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
        ),
    )

    return fig


if __name__ == "__main__":
    fig = main()
    fig.show()
