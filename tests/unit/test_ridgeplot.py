from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.express as px
import pytest

from ridgeplot import ridgeplot
from ridgeplot._color.utils import round_color
from ridgeplot._types import Color, ColorScale, nest_shallow_collection

if TYPE_CHECKING:
    from collections.abc import Collection


def test_fails_when_both_samples_and_densities_are_passed() -> None:
    with pytest.raises(ValueError, match="You may not specify both `samples` and `densities`"):
        ridgeplot(samples=[[1, 2, 3]], densities=[[(1, 1), (2, 2), (3, 3)]])


def test_fails_when_neither_samples_nor_densities_are_passed() -> None:
    with pytest.raises(ValueError, match="You must specify either `samples` or `densities`"):
        ridgeplot()


def test_shallow_densities() -> None:
    shallow_densities = [
        [(0, 0), (1, 1), (2, 0)],  # Trace 1
        [(1, 0), (2, 1), (3, 0)],  # Trace 2
        [(2, 0), (3, 1), (4, 0)],  # Trace 3
    ]
    assert (
        ridgeplot(densities=shallow_densities) ==
        ridgeplot(densities=nest_shallow_collection(shallow_densities))
    )  # fmt: skip


def test_shallow_samples() -> None:
    shallow_samples = [
        [0, 1, 1, 2, 2, 2, 3, 3, 4],  # Trace 1
        [1, 2, 2, 3, 3, 3, 4, 4, 5],  # Trace 2
    ]
    assert (
        ridgeplot(samples=shallow_samples) ==
        ridgeplot(samples=nest_shallow_collection(shallow_samples))
    )  # fmt: skip


def test_shallow_labels() -> None:
    shallow_labels = ["trace 1", "trace 2"]
    assert (
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], labels=shallow_labels) ==
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], labels=nest_shallow_collection(shallow_labels))
    )  # fmt: skip


def test_y_labels_dedup() -> None:
    assert (
        ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], labels=["a"]) ==
        ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], labels=[["a", "a"]])
    )  # fmt: skip


# ==============================================================
# ---  param: colorscale
# ==============================================================


def test_colorscale_coercion(
    valid_colorscale: tuple[ColorScale | Collection[Color] | str, ColorScale]
) -> None:
    colorscale, coerced = valid_colorscale
    assert ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], colorscale=colorscale) == ridgeplot(
        samples=[[[1, 2, 3], [4, 5, 6]]], colorscale=coerced
    )


def test_colorscale_invalid(invalid_colorscale: ColorScale | Collection[Color] | str) -> None:
    with pytest.raises(
        ValueError, match=r"Invalid value .* received for the 'colorscale' property"
    ):
        ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], colorscale=invalid_colorscale)


# ==============================================================
# ---  param: opacity
# ==============================================================


def test_opacity() -> None:
    fig = ridgeplot(
        samples=[[[1, 2, 3], [4, 5, 6]]],
        colorscale=(
            (0.0, "rgb(10, 10, 10)"),
            (1.0, "rgb(20, 20, 20)"),
        ),
        colormode="trace-index",
        opacity=0.5,
    )
    assert fig.data[1].fillcolor == "rgba(20, 20, 20, 0.5)"
    assert fig.data[3].fillcolor == "rgba(10, 10, 10, 0.5)"


# ==============================================================
# ---  param: norm
# ==============================================================


def test_norm() -> None:
    densities = [
        [
            [(0, 0), (1, 1), (2, 0)],  # Trace 1
            [(1, 0), (2, 2), (3, 0)],  # Trace 2
            [(2, 1), (3, 2), (4, 1)],  # Trace 3
        ],
        [
            [(0, 4), (1, 4), (2, 8)],  # Trace 4
            [(1, 4), (2, 4), (3, 2)],  # Trace 5
        ],
    ]
    fig = ridgeplot(densities=densities, norm="percent")
    assert fig.data[1].customdata == ([0], [100], [0])
    assert fig.data[3].customdata == ([0], [100], [0])
    assert fig.data[5].customdata == ([25], [50], [25])
    assert fig.data[7].customdata == ([25], [25], [50])
    assert fig.data[9].customdata == ([40], [40], [20])


# ==============================================================
# ---  param: line_color
# ==============================================================


def test_line_color() -> None:
    fig = ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], line_color="red")
    assert fig.data[1].line.color == fig.data[3].line.color == "red"


def test_line_color_fill_color() -> None:
    fig = ridgeplot(
        samples=[[[1, 2, 3], [4, 5, 6]]],
        colorscale=((0.0, "red"), (1.0, "blue")),
        colormode="trace-index",
        line_color="fill-color",
    )
    assert fig.data[1].line.color == "rgb(0, 0, 255)"
    assert fig.data[3].line.color == "rgb(255, 0, 0)"


def test_line_color_fill_color_fillgradient() -> None:
    colorscale = px.colors.sequential.Blues[:6]
    fig = ridgeplot(
        samples=[[[1, 2, 3], [4, 5, 6]]],
        colorscale=colorscale,
        colormode="fillgradient",
        line_color="fill-color",
    )
    assert round_color(fig.data[1].line.color) == round_color(colorscale[1])
    assert round_color(fig.data[3].line.color) == round_color(colorscale[4])


# ==============================================================
# ---  param: line_width
# ==============================================================


@pytest.mark.parametrize("lw", [0.3, 0.7, 1.2, 3])
def test_line_width(lw: float) -> None:
    fig = ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], line_width=lw)
    assert fig.data[1].line.width == fig.data[3].line.width == lw


# ==============================================================
# ---  param: spacing
# ==============================================================


@pytest.mark.parametrize("spacing", [0.3, 0.7, 1.2, 3])
def test_spacing(spacing: float) -> None:
    densities = [
        [
            [(0, 0), (1, 1), (2, 0)],
            [(1, 0), (2, 1), (3, 2), (4, 1)],
            [(3, 0), (4, 1), (5, 2), (6, 1), (7, 0)],
        ],
        [
            [(-2, 0), (-1, 1), (0, 0)],
            [(0, 0), (1, 1), (2, 1), (3, 0)],
        ],
    ]
    y_max = 2
    fig = ridgeplot(densities=densities, spacing=spacing)
    assert fig.layout.yaxis.tickvals[-1] == -y_max * spacing


# ==============================================================
# ---  Deprecations...
# ==============================================================


def test_deprecated_coloralpha_is_not_missing() -> None:
    with pytest.warns(
        DeprecationWarning,
        match="The 'coloralpha' argument has been deprecated in favor of 'opacity'",
    ):
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], coloralpha=0.5)


def test_deprecated_coloralpha_and_opacity_together_raises() -> None:
    with pytest.raises(
        ValueError,
        match="You may not specify both the 'coloralpha' and 'opacity' arguments!",
    ):
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], coloralpha=0.4, opacity=0.6)


def test_deprecated_linewidth_is_not_missing() -> None:
    with pytest.warns(
        DeprecationWarning,
        match="The 'linewidth' argument has been deprecated in favor of 'line_width'",
    ):
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], linewidth=0.5)


def test_ridgeplot_colorscale_default_deprecation_warning() -> None:
    with pytest.warns(DeprecationWarning, match="colorscale='default' is deprecated"):
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], colorscale="default")
