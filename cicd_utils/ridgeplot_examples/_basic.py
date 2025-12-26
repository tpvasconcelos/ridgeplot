from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import plotly.graph_objects as go


def main() -> go.Figure:
    import numpy as np

    from ridgeplot import ridgeplot

    rng = np.random.default_rng(42)
    my_samples = [rng.normal(n, size=900) for n in range(6, 0, -2)]
    fig = ridgeplot(samples=my_samples)
    fig.update_layout(height=400, width=800)

    return fig


if __name__ == "__main__":
    fig = main()
    fig.show()
