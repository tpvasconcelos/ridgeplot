from __future__ import annotations

import pytest

from ridgeplot import ridgeplot


def test_fails_when_both_samples_and_densities_are_passed() -> None:
    with pytest.raises(ValueError, match="You may not specify both `samples` and `densities`"):
        ridgeplot(samples=[[1, 2, 3]], densities=[[(1, 1), (2, 2), (3, 3)]])


def test_fails_when_neither_samples_nor_densities_are_passed() -> None:
    with pytest.raises(ValueError, match="You must specify either `samples` or `densities`"):
        ridgeplot()
