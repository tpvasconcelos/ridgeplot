from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable

import pytest

from ridgeplot_examples import ALL_EXAMPLES

if TYPE_CHECKING:
    import plotly.graph_objects as go

ROOT_DIR = Path(__file__).parents[2]
PATH_CHARTS = ROOT_DIR / "docs/_static/charts"


def test_path_charts_exists() -> None:
    assert PATH_CHARTS.exists()
    assert PATH_CHARTS.is_dir()


@pytest.mark.parametrize(("plot_id", "example_loader"), ALL_EXAMPLES)
def test_examples_width_height_set(
    plot_id: str,  # noqa: ARG001
    example_loader: Callable[[], go.Figure],
) -> None:
    msg = "Both `width` and `height` should be set in all example plots."
    fig = example_loader()
    assert isinstance(fig.layout.width, int), msg
    assert isinstance(fig.layout.height, int), msg


@pytest.mark.skip(
    reason=(
        "Currently breaking in CI, probably due to small "
        "differences in output between environments. "
        "ref: https://github.com/tpvasconcelos/ridgeplot/issues/159"
    ),
)
@pytest.mark.parametrize(("plot_id", "example_loader"), ALL_EXAMPLES)
def test_regressions(plot_id: str, example_loader: Callable[[], go.Figure]) -> None:
    """Verify that the rendered WebP images match the current artifacts."""
    fig = example_loader()
    img = fig.to_image(
        format="webp",
        width=fig.layout.width,
        height=fig.layout.height,
        scale=3,
        engine="kaleido",
    )
    expected = (PATH_CHARTS / f"{plot_id}.webp").read_bytes()
    assert img == expected
