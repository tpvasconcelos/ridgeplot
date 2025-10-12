from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ridgeplot._figure_factory import create_ridgeplot, normalise_trace_labels
from ridgeplot._types import is_densities

if TYPE_CHECKING:
    from ridgeplot._types import Densities, LabelsArray, ShallowLabelsArray


@pytest.mark.parametrize(
    ("densities", "expected_trace_labels"),
    [
        # single row, single trace
        (
            [[[(0, 0), (1, 1), (2, 0)]]],
            [["Trace 1"]],
        ),
        # single row, multi trace
        (
            [[[(0, 0), (1, 1), (2, 0)], [(1, 0), (2, 1), (3, 0)]]],
            [["Trace 1", "Trace 2"]],
        ),
        # multi row, single trace
        (
            [[[(0, 0), (1, 1), (2, 0)]], [[(1, 0), (2, 2), (3, 0)]], [[(2, 1), (3, 2), (4, 1)]]],
            [["Trace 1"], ["Trace 2"], ["Trace 3"]],
        ),
        # multi row, multi trace
        (
            [
                [[(0, 0), (1, 1), (2, 0)], [(1, 0), (2, 2), (3, 0)], [(2, 1), (3, 2), (4, 1)]],
                [[(0, 4), (1, 4), (2, 8)], [(1, 4), (2, 4), (3, 2)]],
            ],
            [["Trace 1", "Trace 2", "Trace 3"], ["Trace 4", "Trace 5"]],
        ),
    ],
    ids=[
        "single-row, single-trace",
        "single-row, multi-trace",
        "multi-row, single-trace",
        "multi-row, multi-trace",
    ],
)
def test_normalise_trace_labels_no_labels(
    densities: Densities,
    expected_trace_labels: LabelsArray,
) -> None:
    assert is_densities(densities)
    n_traces = sum(len(row) for row in densities)
    trace_labels = normalise_trace_labels(densities=densities, trace_labels=None, n_traces=n_traces)
    assert trace_labels == expected_trace_labels


@pytest.mark.parametrize(
    ("densities", "trace_labels", "expected_trace_labels"),
    [
        # single row, single trace
        (
            [[[(0, 0), (1, 1), (2, 0)]]],
            ["A"],
            [["A"]],
        ),
        # single row, multi trace
        (
            [[[(0, 0), (1, 1), (2, 0)], [(1, 0), (2, 1), (3, 0)]]],
            ["A", "B"],
            [["A", "B"]],
        ),
        # multi row, single trace
        (
            [[[(0, 0), (1, 1), (2, 0)]], [[(1, 0), (2, 2), (3, 0)]], [[(2, 1), (3, 2), (4, 1)]]],
            ["A", "B", "C"],
            [["A"], ["B"], ["C"]],
        ),
        # multi row, multi trace
        (
            [
                [[(0, 0), (1, 1), (2, 0)], [(1, 0), (2, 2), (3, 0)], [(2, 1), (3, 2), (4, 1)]],
                [[(0, 4), (1, 4), (2, 8)], [(1, 4), (2, 4), (3, 2)]],
            ],
            [["A", "B", "C"], ["D", "E"]],
            [["A", "B", "C"], ["D", "E"]],
        ),
    ],
    ids=[
        "single-row, single-trace",
        "single-row, multi-trace",
        "multi-row, single-trace",
        "multi-row, multi-trace",
    ],
)
def test_normalise_trace_labels(
    densities: Densities,
    trace_labels: LabelsArray | ShallowLabelsArray,
    expected_trace_labels: LabelsArray,
) -> None:
    assert is_densities(densities)
    n_traces = sum(len(row) for row in densities)
    norm_trace_labels = normalise_trace_labels(
        densities=densities,
        trace_labels=trace_labels,
        n_traces=n_traces,
    )
    assert norm_trace_labels == expected_trace_labels


class TestCreateRidgeplot:
    @pytest.mark.parametrize(
        "densities",
        [
            [],
            [1, 2, 3],
            [[1, 2, 3]],
            [(1, 2)],
            [[(1, 2)]],
        ],
    )
    def test_densities_must_be_4d(self, densities: Densities) -> None:
        with pytest.raises(ValueError, match="Expected a 4D array of densities"):
            create_ridgeplot(
                densities=densities,
                trace_labels=...,  # type: ignore[reportArgumentType]
                trace_types=...,  # type: ignore[reportArgumentType]
                row_labels=...,  # type: ignore[reportArgumentType]
                colorscale=...,  # type: ignore[reportArgumentType]
                colormode=...,  # type: ignore[reportArgumentType]
                color_discrete_map=...,  # type: ignore[reportArgumentType]
                opacity=...,  # type: ignore[reportArgumentType]
                line_color=...,  # type: ignore[reportArgumentType]
                line_width=...,  # type: ignore[reportArgumentType]
                spacing=...,  # type: ignore[reportArgumentType]
                xpad=...,  # type: ignore[reportArgumentType]
            )
