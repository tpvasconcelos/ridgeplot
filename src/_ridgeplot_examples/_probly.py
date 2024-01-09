from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import plotly.graph_objects as go


def main() -> go.Figure:
    import numpy as np

    from ridgeplot import ridgeplot
    from ridgeplot.datasets import load_probly

    # Load the probly dataset
    df = load_probly()

    # Let's grab the subset of columns used in the example
    column_names = [
        "Almost Certainly",
        "Very Good Chance",
        "We Believe",
        "Likely",
        "About Even",
        "Little Chance",
        "Chances Are Slight",
        "Almost No Chance",
    ]
    df = df[column_names]

    # Not only does 'ridgeplot(...)' come configured with sensible defaults
    # but is also fully configurable to your own style and preference!
    fig = ridgeplot(
        samples=df.to_numpy().T,
        bandwidth=4,
        kde_points=np.linspace(-12.5, 112.5, 500),
        colorscale="viridis",
        colormode="row-index",
        coloralpha=0.6,
        labels=column_names,
        linewidth=2,
        spacing=5 / 9,
    )

    # And you can still update and extend the final
    # Plotly Figure using standard Plotly methods
    fig.update_layout(
        height=600,
        width=800,
        font_size=16,
        plot_bgcolor="white",
        xaxis_tickvals=[-12.5, 0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100, 112.5],
        xaxis_ticktext=["", "0", "", "25", "", "50", "", "75", "", "100", ""],
        xaxis_gridcolor="rgba(0, 0, 0, 0.1)",
        yaxis_gridcolor="rgba(0, 0, 0, 0.1)",
        yaxis_title=dict(text="Assigned Probability (%)", font_size=13),
        showlegend=False,
    )

    return fig


if __name__ == "__main__":
    fig = main()

    # Show us the work!
    fig.show()
