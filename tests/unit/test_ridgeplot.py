from __future__ import annotations

import pytest
from _plotly_utils.exceptions import PlotlyError

from ridgeplot import ridgeplot
from ridgeplot._colors import get_colorscale
from ridgeplot._types import nest_shallow_collection


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


@pytest.mark.parametrize("name", ["default", "bluered", "viridis", "plasma"])
def test_colorscale_by_name(name: str) -> None:
    assert (
        ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], colorscale=name) ==
        ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], colorscale=get_colorscale(name))
    )  # fmt: skip


def test_colorscale_invalid_name() -> None:
    with pytest.raises(ValueError, match="Unknown color scale name"):
        ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], colorscale="whodis")


def test_colorscale_invalid_values() -> None:
    colorscale = (
        (0.0, "rgb(0, 0, 0)"),
        (1.2, "rgb(0, 0, 0)"),
    )
    with pytest.raises(
        PlotlyError,
        match=r"The first and last number in your scale must be 0\.0 and 1\.0 respectively",
    ):
        ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], colorscale=colorscale)


def test_colorscale_invalid_colors() -> None:
    colorscale = (
        (0.0, "rgb(0, 0, 0)"),
        (1.0, "not a valid color"),
    )
    with pytest.raises(
        ValueError, match="color should be a tuple or a str representation of a hex or rgb color"
    ):
        ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], colorscale=colorscale)


def test_coloralpha() -> None:
    fig = ridgeplot(
        samples=[[[1, 2, 3], [4, 5, 6]]],
        colorscale=(
            (0.0, "rgb(10, 10, 10)"),
            (1.0, "rgb(20, 20, 20)"),
        ),
        colormode="trace-index",
        coloralpha=0.5,
    )
    assert fig.data[1].fillcolor == "rgba(20, 20, 20, 0.5)"
    assert fig.data[3].fillcolor == "rgba(10, 10, 10, 0.5)"


@pytest.mark.parametrize("lw", [0.3, 0.7, 1.2, 3])
def test_linewidth(lw: float) -> None:
    fig = ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], linewidth=lw)
    assert fig.data[1].line.width == fig.data[3].line.width == lw


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


def test_deprecated_colormode_index() -> None:
    with pytest.warns(
        DeprecationWarning,
        match="The colormode='index' value has been deprecated in favor of colormode='row-index'",
    ):
        ridgeplot(
            samples=[[1, 2, 3], [1, 2, 3]],
            colormode="index",  # type: ignore[arg-type]
        )


def test_deprecated_show_annotations_is_not_missing() -> None:
    with pytest.warns(
        DeprecationWarning,
        match="The show_annotations argument has been deprecated in favor of show_yticklabels",
    ):
        ridgeplot(samples=[[1, 2, 3], [1, 2, 3]], show_annotations=True)
