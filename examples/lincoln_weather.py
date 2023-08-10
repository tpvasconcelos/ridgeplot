import plotly.graph_objects as go


def main() -> go.Figure:
    import numpy as np

    from ridgeplot import ridgeplot
    from ridgeplot.datasets import load_lincoln_weather

    df = load_lincoln_weather()

    months = df.index.month_name().unique()  # type: ignore
    samples = [
        [
            df[df.index.month_name() == month]["Min Temperature [F]"],  # type: ignore
            df[df.index.month_name() == month]["Max Temperature [F]"],  # type: ignore
        ]
        for month in months
    ]

    fig = ridgeplot(
        samples=samples,
        labels=months,
        coloralpha=0.98,
        bandwidth=4,
        kde_points=np.linspace(-25, 110, 400),
        spacing=0.33,
        linewidth=2,
    )
    fig.update_layout(
        title="Minimum and maximum daily temperatures in Lincoln, NE (2016)",
        height=650,
        width=950,
        font_size=14,
        plot_bgcolor="rgb(245, 245, 245)",
        xaxis_gridcolor="white",
        yaxis_gridcolor="white",
        xaxis_gridwidth=2,
        yaxis_title="Month",
        xaxis_title="Temperature [F]",
        showlegend=False,
    )
    fig.show()

    return fig


if __name__ == "__main__":
    main()
