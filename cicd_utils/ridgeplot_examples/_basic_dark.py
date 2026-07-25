from __future__ import annotations

from typing import TYPE_CHECKING

from ridgeplot_examples._basic import main as basic

if TYPE_CHECKING:
    import plotly.graph_objects as go


def main() -> go.Figure:
    fig = basic(template="plotly_dark")
    return fig


if __name__ == "__main__":
    fig = main()
    fig.show()
