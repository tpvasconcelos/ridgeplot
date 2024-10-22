from __future__ import annotations

from itertools import product
from typing import TYPE_CHECKING, Callable, TypeVar

import numpy as np
import pytest

from ridgeplot._utils import get_xy_extrema, normalise_min_max

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


class TestNormaliseMinMax:
    """Tests for the :func:`ridgeplot._utils.normalise_min_max` function."""

    def test_raises_for_invalid_range(self) -> None:
        """Assert :func:`normalise_min_max()` fails for ``max_ <= min_`` or when ``val``
        is not in range."""
        # max_ <= min_
        with pytest.raises(ValueError, match=r"max_ should be greater than min_"):
            normalise_min_max(val=0.0, min_=3.0, max_=2.9)
        with pytest.raises(ValueError, match=r"max_ should be greater than min_"):
            normalise_min_max(val=0.0, min_=3.0, max_=3.0)
        # val is not in range
        with pytest.raises(ValueError, match=r"val (.*) is out of bounds"):
            normalise_min_max(val=1.0, min_=2.0, max_=3.0)
        with pytest.raises(ValueError, match=r"val (.*) is out of bounds"):
            normalise_min_max(val=5.0, min_=2.0, max_=3.0)

    @pytest.mark.parametrize("val", [0.0, 0.5, 1.0])
    def test_same_val_unchanged_for_range_0_to_1(self, val: float) -> None:
        """The output of :func:`normalise_min_max()` should be equal to
        ``val`` whenever ``min_ == 0`` and ``max_ == 1``."""
        assert normalise_min_max(val=val, min_=0, max_=1) == val

    @pytest.mark.parametrize("val", range(4))
    def test_if_val_is_min_then_zero(self, val: float) -> None:
        """The output of :func:`normalise_min_max()` should be equal to 0.0
        whenever ``val == min_``."""
        assert normalise_min_max(val=val, min_=val, max_=val + 12) == 0.0

    @pytest.mark.parametrize("val", range(4))
    def test_if_val_is_max_then_one(self, val: float) -> None:
        """The output of :func:`normalise_min_max()` should be equal to 1.0
        whenever ``val == max_``."""
        assert normalise_min_max(val=val, min_=val - 12, max_=val) == 1.0

    def test_simple_examples(self) -> None:
        """Test :func:`normalise_min_max()` against some simple examples."""
        assert normalise_min_max(val=24, min_=12, max_=36) == 0.5
        assert normalise_min_max(val=6, min_=4, max_=24) == 0.1
