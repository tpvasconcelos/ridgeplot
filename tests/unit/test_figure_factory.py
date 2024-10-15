from __future__ import annotations

from itertools import product
from typing import TYPE_CHECKING, Callable, TypeVar

import numpy as np
import pytest

from ridgeplot._figure_factory import RidgePlotFigureFactory, get_xy_extrema

if TYPE_CHECKING:
    from ridgeplot._types import Densities, DensitiesRow

_X = TypeVar("_X")


def id_func(x: _X) -> _X:
    """Identity function."""
    return x


class TestGetXYExtrema:
    """Tests for the :func:`ridgeplot._utils.get_xy_extrema` function"""

    def test_raise_for_empty_sequence(self) -> None:
        # Fails for empty sequence
        with pytest.raises(ValueError, match="The densities array should not be empty"):
            get_xy_extrema(densities=[])

    def test_raise_for_non_2d_array(self) -> None:
        # Fails if one of the arrays is not 2D
        with pytest.raises(ValueError, match=r"too many values to unpack \(expected 2\)"):
            get_xy_extrema(
                densities=[
                    # valid 2D trace
                    [[(0, 0), (1, 1), (2, 2)]],
                    # invalid 3D trace
                    [[(3, 3, 3), (4, 4, 4)]],  # type: ignore[list-item]
                ]
            )

    @pytest.mark.parametrize(
        ("densities_type", "rows_type"),
        product((id_func, tuple, list), (id_func, tuple, list, np.asarray)),
    )
    def test_expected_output(
        self,
        densities_type: Callable[[Densities], Densities],
        rows_type: Callable[[DensitiesRow], DensitiesRow],
    ) -> None:
        """Test :func:`get_xy_extrema()` against a varied combination of
        possible input types."""
        # This list contains a varied set of collection types.
        # Which is to show that `get_xy_extrema` accepts any
        # iterable of a valid `Densities` object
        densities: Densities = [
            (
                [
                    (1, 1),  # x_min -> 1
                    (2, 2),
                    (3, 3),
                    (4, 4),
                ],
            ),
            [
                (
                    (2, 2),
                    (36, 3),  # x_max -> 36
                    (4, 62),  # y_max -> 62
                )
            ],
            np.asarray(
                [
                    [
                        (2, 0),  # y_min -> 0
                        (3, 1),
                    ]
                ]
            ),
        ]
        densities = densities_type([rows_type(row) for row in densities])
        # The x-y extrema of the densities array above are:
        expected = (
            1,  # x_min
            36,  # x_max
            0,  # y_min
            62,  # y_max
        )
        assert get_xy_extrema(densities) == expected


class TestRidgePlotFigureFactory:

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
            RidgePlotFigureFactory(
                densities=densities,
                colorscale=...,  # type: ignore[arg-type]
                coloralpha=...,  # type: ignore[arg-type]
                colormode=...,  # type: ignore[arg-type]
                trace_labels=...,  # type: ignore[arg-type]
                trace_type=...,  # type: ignore[arg-type]
                linewidth=...,  # type: ignore[arg-type]
                spacing=...,  # type: ignore[arg-type]
                show_yticklabels=...,  # type: ignore[arg-type]
                xpad=...,  # type: ignore[arg-type]
            )
