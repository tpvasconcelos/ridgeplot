from __future__ import annotations

from itertools import product
from typing import TYPE_CHECKING, Any, Callable, TypeVar
from unittest import mock

import numpy as np
import pytest

from ridgeplot._utils import LazyMapping, get_xy_extrema, normalise_min_max

if TYPE_CHECKING:
    from collections.abc import Mapping

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


class TestLazyMapping:
    """Tests for the :func:`ridgeplot._utils.LazyMapping` class"""

    @pytest.mark.parametrize("target_mapping", [{}, {"a": 1, "b": 2, "c": 3}])
    def test_mapping(self, target_mapping: Mapping[Any, Any]) -> None:
        """Test the part of the implantation of the ``_mapping`` property.

        This test should assert that `._inner_mapping` is not defined before
        `._mapping` is called for the first time. It should also assert that
        `._inner_mapping` holds the same values (same id) as `._mapping` after
        the latter is called.
        """
        lm = LazyMapping(loader=lambda: target_mapping)
        # _inner_mapping is None before _mapping is called
        assert lm._inner_mapping is None
        m = lm._mapping
        # _mapping returns a Mapping (dict in this case)
        assert isinstance(m, dict)
        # now that _mapping has been called,
        # _inner_mapping should point to the same object
        assert lm._inner_mapping is m

    @pytest.mark.parametrize("target_mapping", [{}, {"a": 1, "b": 2, "c": 3}])
    def test_loader_called_only_once(self, target_mapping: Mapping[Any, Any]) -> None:
        """Check that ``LazyMapping`` only calls ``._loader()`` once."""
        lm = LazyMapping(loader=lambda: target_mapping)
        with mock.patch.object(lm, "_loader") as loader:
            # Call count should be zero since `._mapping` has not been accessed yet
            assert loader.call_count == 0
            _ = lm._mapping
            # The first call to `._mapping` calls `_loader`
            assert loader.call_count == 1
            _ = lm._mapping
            _ = lm.items()
            _ = str(lm)
            assert loader.call_count == 1
            _ = lm._loader()
            assert loader.call_count == 2

    @pytest.mark.parametrize("target_mapping", [{}, {"a": 1, "b": 2, "c": 3}])
    def test_mapping_mirrors_mapping_returned_by_loader(
        self, target_mapping: Mapping[Any, Any]
    ) -> None:
        """Test that LazyMapping behaves just like the mapping returned by the
        ``loader`` callable argument.

        This test should cover __getitem__, __iter__, and __len__ from Mapping
        and __str__ and __repr__ additionally.
        """
        lm = LazyMapping(loader=lambda: target_mapping)
        assert lm.items() == target_mapping.items()
        # test __getitem__
        for k in target_mapping:
            assert lm[k] == target_mapping[k]
        # test __iter__
        assert tuple(lm) == tuple(target_mapping)
        # test __len__
        assert len(lm) == len(target_mapping)
        # test __str__
        assert str(lm) == str(target_mapping)
        # test __repr__
        assert repr(lm) == repr(target_mapping)
