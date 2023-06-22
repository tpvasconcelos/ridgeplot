from typing import Mapping
from unittest import mock

import pytest

from ridgeplot._utils import LazyMapping, normalise_min_max


class TestNormaliseMinMax:
    """Tests for the :func:`ridgeplot._utils.normalise_min_max` function."""

    def test_raises_for_invalid_range(self) -> None:
        """Assert :func:`normalise_min_max()` fails for ``max_ <= min_`` or when ``val``
        is not in range."""
        # max_ <= min_
        pytest.raises(ValueError, normalise_min_max, val=0.0, min_=3.0, max_=2.9).match(
            r"max_ should be greater than min_"
        )
        pytest.raises(ValueError, normalise_min_max, val=0.0, min_=3.0, max_=3.0).match(
            r"max_ should be greater than min_"
        )
        # val is not in range
        pytest.raises(ValueError, normalise_min_max, val=1.0, min_=2.0, max_=3.0).match(
            r"val (.*) is out of bounds"
        )
        pytest.raises(ValueError, normalise_min_max, val=5.0, min_=2.0, max_=3.0).match(
            r"val (.*) is out of bounds"
        )

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
    def test_mapping(self, target_mapping: Mapping) -> None:
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
    def test_loader_called_only_once(self, target_mapping: Mapping) -> None:
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
    def test_mapping_mirrors_mapping_returned_by_loader(self, target_mapping: Mapping) -> None:
        """Test that LazyMapping behaves just like the mapping returned by the
        ``loader`` callable argument.

        This test should cover __getitem__, __iter__, and __len__ from Mapping
        and __str__ and __repr__ additionally.
        """
        lm = LazyMapping(loader=lambda: target_mapping)
        assert lm.items() == target_mapping.items()
        # test: __getitem__
        for k in target_mapping.keys():
            assert lm[k] == target_mapping[k]
        # test: __iter__
        assert tuple(lm) == tuple(target_mapping)
        # test: __len__
        assert len(lm) == len(target_mapping)
        # test: __str__
        assert str(lm) == str(target_mapping)
        # test: __repr__
        assert repr(lm) == repr(target_mapping)
