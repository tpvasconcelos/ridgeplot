from __future__ import annotations

from typing import (
    Any,
    Callable,
    Collection,
    Iterator,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

from ridgeplot._types import Numeric


def normalise_min_max(val: Numeric, min_: Numeric, max_: Numeric) -> float:
    if max_ <= min_:
        raise ValueError(
            f"max_ should be greater than min_. Got max_={max_} and min_={min_} instead."
        )
    if not (min_ <= val <= max_):
        raise ValueError(f"val ({val}) is out of bounds ({min_}, {max_}).")
    return float((val - min_) / (max_ - min_))


def get_collection_array_shape(arr: Collection) -> Tuple[Union[int, Set[int]], ...]:
    """Return the shape of a :class:`~typing.Collection` array.

    Parameters
    ----------
    arr
        The :class:`~typing.Collection` array.

    Returns
    -------
    Tuple[Union[int, Set[int]], ...]
        The elements of the shape tuple give the lengths of the corresponding
        array dimensions. If the length of a dimension is variable, the
        corresponding element is a :class:`~set` of the variable lengths.
        Otherwise, (if the length of a dimension is fixed), the corresponding
        element is an :class:`~int`.

    Examples
    --------
    >>> get_collection_array_shape([1, 2, 3])
    (3,)

    >>> get_collection_array_shape([[1, 2, 3], [4, 5]])
    (2, {2, 3})

    >>> get_collection_array_shape(
    ...     [
    ...         [
    ...             [1, 2, 3], [4, 5]
    ...         ],
    ...         [
    ...             [6, 7, 8, 9],
    ...         ],
    ...     ]
    ... )
    (2, {1, 2}, {2, 3, 4})

    >>> get_collection_array_shape(
    ...     [
    ...         [
    ...             [1], [2, 3], [4, 5, 6],
    ...         ],
    ...         [
    ...             [7, 8, 9, 10, 11],
    ...         ],
    ...     ]
    ... )
    (2, {1, 3}, {1, 2, 3, 5})

    >>> get_collection_array_shape(
    ...     [
    ...         [
    ...             [(0, 0), (1, 1), (2, 2), (3, 3)],
    ...             [(0, 0), (1, 1), (2, 2)],
    ...             [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
    ...         ],
    ...         [
    ...             [(-2, 2), (-1, 1), (0, 1)],
    ...             [(2, 2), (3, 1), (4, 1)],
    ...         ],
    ...     ]
    ... )
    (2, {2, 3}, {3, 4, 5}, 2)

    >>> get_collection_array_shape(
    ...     [
    ...         [
    ...             ["a", "b", "c", "d"], ["e", "f"],
    ...         ],
    ...         [
    ...             ["h", "i", "j", "k", "l"],
    ...         ],
    ...     ]
    ... )
    (2, {1, 2}, {2, 4, 5})
    """

    def _get_dim_length(obj: Any) -> int:
        """Return the length of a dimension of a :class:`~typing.Collection` array."""
        if not isinstance(obj, Collection) or isinstance(obj, str):
            raise TypeError(f"Expected a Collection. Got {type(obj)} instead.")
        return len(obj)

    shape: List[Union[int, Set[int]]] = [_get_dim_length(arr)]
    while isinstance(arr, Collection):
        try:
            dim_lengths = set(map(_get_dim_length, arr))
        except TypeError:
            break
        shape.append(dim_lengths.pop() if len(dim_lengths) == 1 else dim_lengths)
        arr = [item for sublist in arr for item in sublist]
    return tuple(shape)


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
