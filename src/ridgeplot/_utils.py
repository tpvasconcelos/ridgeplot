from typing import Callable, Iterable, Iterator, Mapping, Optional, Tuple, TypeVar

import numpy.typing as npt


def get_xy_extrema(arrays: Iterable[npt.ArrayLike]) -> Tuple[float, float, float, float]:
    """Returns the x-y extrema (x_min, x_max, y_min, y_max) of a list of 2D
    arrays of shape (2, M)."""
    # Unpack and flatten all x and y values from `arrays`
    x = []
    y = []
    for array in arrays:
        x.extend(array[0])
        y.extend(array[1])
    return min(x), max(x), min(y), max(y)


def normalise_min_max(val: float, min_: float, max_: float) -> float:
    if max_ <= min_:
        raise ValueError(
            f"max_ should be greater than min_. Got max_={max_} and min_={min_} instead."
        )
    if not (min_ <= val <= max_):
        raise ValueError(f"val ({val}) is out of bounds ({min_}, {max_}).")
    return (val - min_) / (max_ - min_)


KT = TypeVar("KT")  # Mapping key type
VT = TypeVar("VT")  # Mapping value type


class LazyMapping(Mapping[KT, VT]):
    __slots__ = ("_loader", "_inner_mapping")

    def __init__(self, loader: Callable[[], Mapping[KT, VT]]):
        self._loader = loader
        self._inner_mapping: Optional[Mapping[KT, VT]] = None

    @property
    def _mapping(self) -> Mapping[KT, VT]:
        if self._inner_mapping is None:
            self._inner_mapping = self._loader()
        return self._inner_mapping

    def __getitem__(self, item: KT) -> VT:
        return self._mapping.__getitem__(item)

    def __iter__(self) -> Iterator[KT]:
        return self._mapping.__iter__()

    def __len__(self) -> int:
        return self._mapping.__len__()

    def __str__(self) -> str:
        return self._mapping.__str__()

    def __repr__(self) -> str:
        return self._mapping.__repr__()
