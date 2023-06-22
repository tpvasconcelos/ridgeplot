from itertools import product
from typing import Callable, Iterable, TypeVar

import numpy as np
import pytest

from ridgeplot._figure_factory import get_xy_extrema
from ridgeplot._types import DensitiesT

_X = TypeVar("_X")


def id_func(x: _X) -> _X:
    """Identity function."""
    return x


class TestGetXYExtrema:
    """Tests for the :func:`ridgeplot._utils.get_xy_extrema` function"""

    def test_raise_for_empty_sequence(self) -> None:
        # Fails for empty sequence
        with pytest.raises(ValueError, match="arg is an empty sequence"):
            get_xy_extrema(densities=[])

    def test_raise_for_non_2d_array(self) -> None:
        # Fails if one of the arrays is not 2D
        with pytest.raises(ValueError, match=r"too many values to unpack \(expected 2\)"):
            get_xy_extrema(
                densities=[
                    [[(0, 0), (1, 1), (2, 2)]],  # valid 2D trace
                    [[(3, 3, 3), (4, 4, 4)]],  # invalid 3D trace
                ]
            )

    @pytest.mark.parametrize(
        ("iterable_type", "collection_type"),
        product((id_func, tuple, list), (id_func, tuple, list, np.asarray)),
    )
    def test_expected_output(
        self,
        iterable_type: Callable[[Iterable], Iterable],
        collection_type: Callable[[DensitiesT], DensitiesT],
    ) -> None:
        """Test :func:`get_xy_extrema()` against a varied combination of
        possible input types."""
        # This tuple contains a varied set of collection types.
        # Which is to show that get_xy_extrema accepts any
        # iterable of any valid `Densities` objects
        densities: Iterable[DensitiesT] = [
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
        densities = iterable_type(collection_type(arr) for arr in densities)
        # The x-y extrema of the densities array above are:
        expected = (
            1,  # x_min
            36,  # x_max
            0,  # y_min
            62,  # y_max
        )
        assert get_xy_extrema(densities) == expected
