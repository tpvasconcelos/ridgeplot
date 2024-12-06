from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ridgeplot import ridgeplot
from ridgeplot._color.interpolation import (
    SOLID_COLORMODE_MAPS,
    ColorscaleInterpolants,
    InterpolationContext,
    SolidColormode,
    _interpolate_mean_means,  # pyright: ignore[reportPrivateUsage]
    _interpolate_mean_minmax,  # pyright: ignore[reportPrivateUsage]
    interpolate_color,
    slice_colorscale,
)
from ridgeplot._color.utils import to_rgb

if TYPE_CHECKING:
    from ridgeplot._types import ColorScale, Densities


# ==============================================================
# ---  interpolate_color()
# ==============================================================


def test_interpolate_color_p_in_scale(viridis_colorscale: ColorScale) -> None:
    viridis_colorscale = list(viridis_colorscale)
    assert interpolate_color(colorscale=viridis_colorscale, p=0) == to_rgb(viridis_colorscale[0][1])
    assert interpolate_color(colorscale=viridis_colorscale, p=1) == to_rgb(
        viridis_colorscale[-1][1]
    )
    # Test that the alpha channels are also properly handled here
    cs = ((0, "rgba(0, 0, 0, 0)"), (1, "rgba(255, 255, 255, 1)"))
    assert interpolate_color(colorscale=cs, p=0) == cs[0][1]
    assert interpolate_color(colorscale=cs, p=1) == cs[-1][1]


def test_interpolate_color_p_not_in_scale(viridis_colorscale: ColorScale) -> None:
    # Hard-coded test case for the Viridis colorscale
    assert interpolate_color(colorscale=viridis_colorscale, p=0.5) == "rgb(34.5, 144.0, 139.5)"
    # Test that the alpha channels are also properly handled here
    cs = ((0, "rgba(0, 0, 0, 0)"), (1, "rgba(255, 255, 255, 1)"))
    assert interpolate_color(colorscale=cs, p=0.5) == "rgba(127.5, 127.5, 127.5, 0.5)"


@pytest.mark.parametrize("p", [-10.0, -1.3, 1.9, 100.0])
def test_interpolate_color_fails_for_p_out_of_bounds(p: float) -> None:
    with pytest.raises(ValueError, match="should be a float value between 0 and 1"):
        interpolate_color(colorscale=..., p=p)


# ==============================================================
# --- slice_colorscale()
# ==============================================================


def test_slice_colorscale_lower_less_than_upper() -> None:
    with pytest.raises(ValueError, match="p_lower should be less than p_upper"):
        slice_colorscale(colorscale=[(0, "...")], p_lower=1, p_upper=0)


def test_slice_colorscale_lower_than_0() -> None:
    with pytest.raises(ValueError, match="p_lower should be >= 0"):
        slice_colorscale(colorscale=[(0, "...")], p_lower=-1, p_upper=0)


def test_slice_colorscale_upper_than_1() -> None:
    with pytest.raises(ValueError, match="p_upper should be <= 1"):
        slice_colorscale(colorscale=[(0, "...")], p_lower=0, p_upper=1.1)


def test_slice_colorscale_unchanged() -> None:
    cs = ((0, "rgb(0, 0, 0)"), (1, "rgb(255, 255, 255)"))
    assert slice_colorscale(colorscale=cs, p_lower=0, p_upper=1) == cs


def test_slice_colorscale() -> None:
    cs = (
        (0, "rgb(0, 0, 0)"),
        (0.5, "rgb(127.5, 127.5, 127.5)"),
        (1, "rgb(255, 255, 255)"),
    )
    assert slice_colorscale(colorscale=cs, p_lower=0.25, p_upper=0.75) == (
        (0.0, "rgb(63.75, 63.75, 63.75)"),
        (0.5, "rgb(127.5, 127.5, 127.5)"),
        (1.0, "rgb(191.25, 191.25, 191.25)"),
    )


def test_slice_colorscale_no_intermediate_values() -> None:
    cs = ((0, "rgb(0, 0, 0)"), (1, "rgb(255, 255, 255)"))
    assert slice_colorscale(colorscale=cs, p_lower=0.25, p_upper=0.75) == (
        (0.0, "rgb(63.75, 63.75, 63.75)"),
        (1.0, "rgb(191.25, 191.25, 191.25)"),
    )


def test_slice_colorscale_alpha() -> None:
    cs = (
        (0, "rgba(0, 0, 0, 0)"),
        (0.5, "rgba(127.5, 127.5, 127.5, 0.5)"),
        (1, "rgba(255, 255, 255, 1)"),
    )
    assert slice_colorscale(colorscale=cs, p_lower=0.25, p_upper=0.75) == (
        (0.0, "rgba(63.75, 63.75, 63.75, 0.25)"),
        (0.5, "rgba(127.5, 127.5, 127.5, 0.5)"),
        (1.0, "rgba(191.25, 191.25, 191.25, 0.75)"),
    )


def test_slice_colorscale_mixed_alpha_channels() -> None:
    cs = (
        (0, "rgba(0, 0, 0, 0)"),
        (0.5, "rgba(127.5, 127.5, 127.5, 1)"),
        (1, "rgba(255, 255, 255, 0)"),
    )
    assert slice_colorscale(colorscale=cs, p_lower=0.25, p_upper=0.75) == (
        (0.0, "rgba(63.75, 63.75, 63.75, 0.5)"),
        (0.5, "rgba(127.5, 127.5, 127.5, 1)"),
        (1.0, "rgba(191.25, 191.25, 191.25, 0.5)"),
    )


# ==============================================================
# --- Solid color modes
# ==============================================================


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


def test_interpolate_mean_minmax() -> None:
    ctx = InterpolationContext.from_densities(
        [
            [[(0, 1), (1, 2), (2, 1)]],
            [[(2, 2), (3, 4), (4, 2)]],
            [[(4, 1), (5, 6), (6, 1)]],
        ]
    )
    ps = _interpolate_mean_minmax(ctx)
    assert ps == [[1 / 6], [3 / 6], [5 / 6]]


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


_DENSITY_01 = [(0, 1), (1, 2), (2, 1)]
_DENSITY_02 = [(1, 1), (2, 2), (3, 1)]

_DENSITIES_ONE_TRACE = [[_DENSITY_01]]
_DENSITIES_ONE_ROW = [[_DENSITY_01, _DENSITY_02]]
_DENSITIES_ONE_TRACE_PER_ROW = [[_DENSITY_01, _DENSITY_02], [_DENSITY_02]]


@pytest.mark.parametrize(
    ("colormode", "densities", "expected"),
    [
        # One trace
        ("row-index", _DENSITIES_ONE_TRACE, [[0.0]]),
        ("trace-index", _DENSITIES_ONE_TRACE, [[0.0]]),
        ("trace-index-row-wise", _DENSITIES_ONE_TRACE, [[0.0]]),
        # One row
        ("row-index", _DENSITIES_ONE_ROW, [[0.0, 0.0]]),
        ("trace-index", _DENSITIES_ONE_ROW, [[1.0, 0.0]]),
        ("trace-index-row-wise", _DENSITIES_ONE_ROW, [[1.0, 0.0]]),
        # One trace per row
        ("row-index", _DENSITIES_ONE_TRACE_PER_ROW, [[1.0, 1.0], [0.0]]),
        ("trace-index", _DENSITIES_ONE_TRACE_PER_ROW, [[1.0, 0.5], [0.0]]),
        ("trace-index-row-wise", _DENSITIES_ONE_TRACE_PER_ROW, [[1.0, 0.0], [0.0]]),
    ],
)
def test_index_based_colormodes(
    colormode: SolidColormode, densities: Densities, expected: ColorscaleInterpolants
) -> None:
    """ZeroDivisionError should never be raised, even when there is only one
    trace, one row, or one trace per row."""
    interpolate_func = SOLID_COLORMODE_MAPS[colormode]
    interpolants = interpolate_func(ctx=InterpolationContext.from_densities(densities))
    assert interpolants == expected
