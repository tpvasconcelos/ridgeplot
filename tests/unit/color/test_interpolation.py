from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ridgeplot import ridgeplot
from ridgeplot._color.interpolation import (
    InterpolationContext,
    _interpolate_mean_means,
    interpolate_color,
)

if TYPE_CHECKING:
    from ridgeplot._types import ColorScale


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


# ==============================================================
# ---  interpolate_color()
# ==============================================================


def test_interpolate_color_p_in_scale(viridis_colorscale: ColorScale) -> None:
    viridis_colorscale = list(viridis_colorscale)
    assert interpolate_color(colorscale=viridis_colorscale, p=0) == viridis_colorscale[0][1]
    assert interpolate_color(colorscale=viridis_colorscale, p=1) == viridis_colorscale[-1][1]


def test_interpolate_color_p_not_in_scale(viridis_colorscale: ColorScale) -> None:
    # Hard-coded test case.
    assert interpolate_color(colorscale=viridis_colorscale, p=0.5) == "rgb(34.5, 144.0, 139.5)"


@pytest.mark.parametrize("p", [-10.0, -1.3, 1.9, 100.0])
def test_interpolate_color_fails_for_p_out_of_bounds(p: float) -> None:
    with pytest.raises(ValueError, match="should be a float value between 0 and 1"):
        interpolate_color(colorscale=..., p=p)  # type: ignore[arg-type]
