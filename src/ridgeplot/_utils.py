from __future__ import annotations

from collections.abc import Collection
from typing import (
    TYPE_CHECKING,
    TypeVar,
)

if TYPE_CHECKING:
    from typing import Any

    from ridgeplot._types import CollectionL2, Densities, Numeric


def get_xy_extrema(densities: Densities) -> tuple[Numeric, Numeric, Numeric, Numeric]:
    r"""Get the global x-y extrema (x_min, x_max, y_min, y_max) over all
    :data:`~ridgeplot._types.DensityTrace`\s in the
    :data:`~ridgeplot._types.Densities` array.

    Parameters
    ----------
    densities
        A :data:`~ridgeplot._types.Densities` array.


    Returns
    -------
    Tuple[Numeric, Numeric, Numeric, Numeric]
        A tuple of the form (x_min, x_max, y_min, y_max).

    Examples
    --------
    >>> get_xy_extrema(
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
    (-2, 4, 0, 4)
    """
    if len(densities) == 0:
        raise ValueError("The densities array should not be empty.")
    x_flat: list[Numeric] = []
    y_flat: list[Numeric] = []
    for row in densities:
        for trace in row:
            for x, y in trace:
                x_flat.append(x)
                y_flat.append(y)
    return min(x_flat), max(x_flat), min(y_flat), max(y_flat)


def normalise_min_max(val: Numeric, min_: Numeric, max_: Numeric) -> float:
    if max_ <= min_:
        raise ValueError(
            f"max_ should be greater than min_. Got max_={max_} and min_={min_} instead."
        )
    if not (min_ <= val <= max_):
        raise ValueError(f"val ({val}) is out of bounds ({min_}, {max_}).")
    return float((val - min_) / (max_ - min_))


def get_collection_array_shape(arr: Collection[Any]) -> tuple[int | set[int], ...]:
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
    >>> get_collection_array_shape([])
    (0,)

    >>> get_collection_array_shape([1, 2, 3])
    (3,)

    >>> get_collection_array_shape([[1, 2, 3], [4, 5], [6], []])
    (4, {0, 1, 2, 3})

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
    ...             ["a", "b", "c", "d"],
    ...             ["e", "f"],
    ...         ],
    ...         [
    ...             ["h", "i", "j", "k", "l"],
    ...             [],
    ...         ],
    ...     ]
    ... )
    (2, 2, {0, 2, 4, 5})

    >>> get_collection_array_shape("I'm not a collection")
    Traceback (most recent call last):
    ...
    TypeError: Expected a Collection. Got <class 'str'> instead.
    """

    def _get_dim_length(obj: Any) -> int:
        """Return the length of a dimension of a :class:`~typing.Collection` array."""
        if not isinstance(obj, Collection) or isinstance(obj, str):
            raise TypeError(f"Expected a Collection. Got {type(obj)} instead.")
        return len(obj)

    shape: list[int | set[int]] = [_get_dim_length(arr)]
    while isinstance(arr, Collection) and len(arr) > 0:
        try:
            dim_lengths = set(map(_get_dim_length, arr))
        except TypeError:
            break
        shape.append(dim_lengths.pop() if len(dim_lengths) == 1 else dim_lengths)
        arr = [item for sublist in arr for item in sublist]
    return tuple(shape)


_V = TypeVar("_V")


def ordered_dedup(seq: Collection[_V]) -> list[_V]:
    """Return a list with the elements of ``seq`` in the order they first appear.

    Parameters
    ----------
    seq
        A sequence.

    Returns
    -------
    list
        A list with the elements of ``seq`` in the order they first appear.

    Examples
    --------
    >>> ordered_dedup([1, 2, 3, 1, 2, 3, 1, 2, 3])
    [1, 2, 3]

    >>> ordered_dedup([1, 2, 3, 4, 5, 6])
    [1, 2, 3, 4, 5, 6]

    >>> ordered_dedup([1, 1, 1, 1, 1, 1, 1, 1, 1])
    [1]

    >>> ordered_dedup([1, 2, 3, 3, 2, 1])
    [1, 2, 3]

    >>> ordered_dedup([3, 1, 2, 4, 2, 4, 5])
    [3, 1, 2, 4, 5]
    """
    return list(dict.fromkeys(seq))


def normalise_row_attrs(attrs: CollectionL2[_V], densities: Densities) -> CollectionL2[_V]:
    """Normalise the attributes over a Density array such that the number of
    attributes matches the number of traces in each row.

    Parameters
    ----------
    attrs
        The attributes collection to normalise.
    densities
        The densities array to normalise the attributes over.

    Returns
    -------
    CollectionL2
        The normalised attributes collection.

    Raises
    ------
    ValueError
        If the number of traces does not match the number of attributes for a
        row.

    Examples
    --------
    >>> densities = [
    ...     [                                             # Row 1
    ...         [(0, 0), (1, 1), (2, 0)],                 # Trace 1
    ...         [(1, 0), (2, 1), (3, 2), (4, 1)],         # Trace 2
    ...         [(3, 0), (4, 1), (5, 2), (6, 1), (7, 0)], # Trace 3
    ...     ],
    ...     [                                             # Row 2
    ...         [(-2, 0), (-1, 1), (0, 0)],               # Trace 4
    ...         [(0, 0), (1, 1), (2, 1), (3, 0)],         # Trace 5
    ...     ],
    ... ]
    >>> normalise_row_attrs([["A"], ["B"]], densities)
    [['A', 'A', 'A'], ['B', 'B']]
    >>> normalise_row_attrs([["A"], ["B", "C"]], densities)
    [['A', 'A', 'A'], ['B', 'C']]
    >>> normalise_row_attrs([["A", "A", "A"], ["B", "B"]], densities)
    [['A', 'A', 'A'], ['B', 'B']]
    >>> normalise_row_attrs([["A", "B"], ["C"]], densities)
    Traceback (most recent call last):
    ...
    ValueError: Mismatch between number of traces (3) and number of attrs (2) for row 0.

    """
    norm_attrs = []
    for i, (row, row_attr) in enumerate(zip(densities, attrs)):
        n_traces = len(row)
        n_attrs = len(row_attr)
        if n_traces != n_attrs:
            if n_attrs != 1:
                raise ValueError(
                    f"Mismatch between number of traces ({n_traces}) "
                    f"and number of attrs ({n_attrs}) for row {i}."
                )
            row_attr = list(row_attr) * n_traces  # noqa: PLW2901
        norm_attrs.append(row_attr)
    return norm_attrs
