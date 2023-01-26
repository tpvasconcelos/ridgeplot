from __future__ import annotations

from typing import Callable, Iterable, Iterator, List, Mapping, Optional, Tuple, TypeVar

from ridgeplot._types import NestedNumericSequenceT, NumericT


def get_xy_extrema(
    arrays: Iterable[NestedNumericSequenceT],
) -> Tuple[NumericT, NumericT, NumericT, NumericT]:
    """Get the global x-y extrema (x_min, x_max, y_min, y_max) of a sequence of
    2D array-like objects.

    Parameters
    ----------
    arrays
        A sequence of 2D array-like objects.

    Returns
    -------
    Tuple[Numeric, Numeric, Numeric, Numeric]
        A tuple of the form (x_min, x_max, y_min, y_max).

    Raises
    ------
    :exc:`ValueError`
        If the ``arrays`` sequence is empty, or if one of the arrays is empty,
        or if one of the arrays is not 2D.

    Examples
    --------
    >>> get_xy_extrema([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    (1, 6, 3, 8)
    """
    x_flat: List[NumericT] = []
    y_flat: List[NumericT] = []
    for array in arrays:
        ndim = len(array)
        if ndim != 2:
            raise ValueError(f"Expected 2D array, got {ndim}D array instead.")
        x, y = array[0], array[1]
        if len(x) == 0 or len(y) == 0:
            raise ValueError("Cannot get extrema of an empty array.")
        x_flat.extend(x)
        y_flat.extend(y)
    if len(x_flat) == 0 or len(y_flat) == 0:
        raise ValueError("Cannot get extrema of empty array sequence.")
    return min(x_flat), max(x_flat), min(y_flat), max(y_flat)


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
    """A lazy mapping that loads its contents only when first needed.

    Parameters
    ----------
    loader
        A callable that returns a mapping.

    Examples
    --------
    >>> from typing import Dict
    >>>
    >>> def my_io_loader() -> Dict[str, int]:
    ...     print("Loading...")
    ...     return {"a": 1, "b": 2}
    ...
    >>> lazy_mapping = LazyMapping(my_io_loader)
    >>> lazy_mapping
    Loading...
    {'a': 1, 'b': 2}
    """

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
