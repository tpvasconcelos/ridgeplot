from __future__ import annotations

import pytest

from ridgeplot import ridgeplot
from ridgeplot._colormodes import InterpolationContext, _interpolate_mean_means


def test_colormode_invalid() -> None:
    with pytest.raises(
        ValueError, match="The colormode argument should be one of .* got INVALID instead"
    ):
        ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], colormode="INVALID")  # type: ignore[arg-type]


def test_colormode_trace_index_row_wise() -> None:
    fig = ridgeplot(
        samples=[[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]],
        colorscale=(
            (0.0, "rgb(100, 100, 100)"),
            (1.0, "rgb(200, 200, 200)"),
        ),
        colormode="trace-index-row-wise",
    )
    assert fig.data[1].fillcolor == fig.data[5].fillcolor == "rgb(200, 200, 200)"
    assert fig.data[3].fillcolor == fig.data[7].fillcolor == "rgb(100, 100, 100)"


def test_interpolate_mean_means() -> None:
    ctx = InterpolationContext.from_densities(
        [
            [[(0, 1), (1, 2), (2, 1)]],
            [[(2, 2), (3, 4), (4, 2)]],
            [[(4, 1), (5, 6), (6, 1)]],
        ]
    )
    ps = _interpolate_mean_means(ctx)
    assert ps == [[0.0], [0.5], [1.0]]
