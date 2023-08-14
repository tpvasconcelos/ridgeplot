import plotly.graph_objects as go


def main() -> go.Figure:
    import numpy as np

    from ridgeplot import ridgeplot

    rng = np.random.default_rng(42)
    my_samples = [rng.normal(n / 1.2, size=600) for n in range(8, 0, -1)]
    fig = ridgeplot(samples=my_samples)
    fig.update_layout(height=450, width=800)
    fig.show()

    return fig


if __name__ == "__main__":
    main()
