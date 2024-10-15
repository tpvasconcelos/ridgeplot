from __future__ import annotations

import pytest

from ridgeplot import ridgeplot
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
        ridgeplot(samples=[[[1, 2, 3], [4, 5, 6]]], labels=["a", "a"])
    )  # fmt: skip


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
