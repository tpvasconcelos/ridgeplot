from __future__ import annotations

from typing import TYPE_CHECKING, Any

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


# ==============================================================
# ---  param: labels
# ==============================================================


def test_shallow_labels() -> None:
    fig1 = ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], labels=["A", "B"])
    fig2 = ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], labels=[["A"], ["B"]])
    assert fig1 == fig2
    assert fig1.data[1].name == "A"
    assert fig1.data[3].name == "B"


def test_y_labels_dedup() -> None:
    fig1 = ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], labels=["A"])
    fig2 = ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], labels=[["A", "A"]])
    assert fig1 == fig2
    assert fig1.data[1].name == "A"
    assert fig1.data[3].name == "A"


# ==============================================================
# ---  param: trace_type
# ==============================================================


def test_shallow_trace_type() -> None:
    assert (
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], trace_type="bar") ==
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], trace_type=["bar", "bar"]) ==
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], trace_type=[["bar"], ["bar"]])
    )  # fmt: skip


def test_unknown_trace_type() -> None:
    with pytest.raises(TypeError, match="Invalid trace_type: foo"):
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], trace_type="foo")  # pyright: ignore[reportArgumentType]


# ==============================================================
# ---  param: row_labels
# ==============================================================


@pytest.mark.parametrize(
    "row_labels",
    [
        ["row 1"],
        ["Trace 1", "Trace 2", "Trace 3", "Trace 4", "Trace 5"],
    ],
)
def test_row_labels_wrong_len(row_labels: Any) -> None:
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
    with pytest.raises(ValueError, match=r"Expected 2 row_labels, got .* instead"):
        ridgeplot(densities=densities, row_labels=row_labels)


def test_row_labels_auto() -> None:
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
    assert (
        ridgeplot(densities=densities) ==
        ridgeplot(densities=densities, row_labels=["Trace 1,Trace 2,Trace 3", "Trace 4,Trace 5"])
    )  # fmt: skip


def test_row_labels_false() -> None:
    fig = ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], row_labels=False)
    assert fig.layout.yaxis.tickvals is None
    assert fig.layout.yaxis.ticktext is None
    assert fig.layout.yaxis.showticklabels is False


# ==============================================================
# ---  param: nbins
# ==============================================================


def test_nbins() -> None:
    fig = ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], nbins=3)
    assert len(fig.data) == 2
    assert fig.data[0]._plotly_name == "bar"


# ==============================================================
# ---  param: colorscale
# ==============================================================


def test_colorscale_coercion(
    valid_colorscale: tuple[ColorScale | Collection[Color] | str, ColorScale],
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
# ---  param: color_discrete_map
# ==============================================================


def test_color_discrete_map() -> None:
    fig = ridgeplot(
        samples=[[[1, 2, 3], [4, 5, 6]]],
        color_discrete_map={"A": "rgba(0, 128, 0, 1.0)", "B": "rgba(255, 165, 0, 1.0)"},
        labels=["A", "B"],
    )
    assert fig.data[1].fillcolor == "rgba(0, 128, 0, 1.0)"
    assert fig.data[3].fillcolor == "rgba(255, 165, 0, 1.0)"


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


@pytest.mark.parametrize(
    ("arg_dep", "val_dep", "arg_new", "val_new"),
    [
        ("coloralpha", 0.5, "opacity", 0.5),
        ("linewidth", 0.5, "line_width", 0.5),
        ("show_yticklabels", True, "row_labels", ["Trace 1", "Trace 2"]),
    ],
)
def test_deprecated_arguments(
    arg_dep: str,
    val_dep: Any,
    arg_new: str,
    val_new: Any,
) -> None:
    samples = [[1, 2, 3], [1, 2, 3]]

    # Test that using the new argument works without warnings
    fig_new = ridgeplot(samples=samples, **{arg_new: val_new})

    # Test that using the deprecated argument raises a DeprecationWarning
    with pytest.warns(
        DeprecationWarning,
        match=f"The '{arg_dep}' argument has been deprecated in favor of '{arg_new}'",
    ):
        fig_dep = ridgeplot(samples=samples, **{arg_dep: val_dep})

    # Test that both approaches yield the same figure
    assert fig_new == fig_dep

    # Test that using both the deprecated and new argument raises the expected exception
    with pytest.raises(
        ValueError,
        match=f"You may not specify both the '{arg_dep}' and '{arg_new}' arguments!",
    ):
        ridgeplot(samples=samples, **{arg_dep: val_dep, arg_new: val_new})


def test_ridgeplot_colorscale_default_deprecation_warning() -> None:
    with pytest.warns(DeprecationWarning, match="colorscale='default' is deprecated"):
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], colorscale="default")
