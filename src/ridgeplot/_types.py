from __future__ import annotations

import sys
from typing import Any, Collection, Tuple, TypeVar, Union, overload

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

import numpy as np

# ========================================================
# ---  Base nested Collection types (ragged arrays)
# ========================================================

_T = TypeVar("_T")

CollectionL1 = Collection[_T]
"""A :data:`~typing.TypeAlias` for a standard :class:`~Collection`
(1 level).

Example:

>>> c: CollectionL1[int] = [1, 2, 3]
"""

CollectionL2 = Collection[Collection[_T]]
"""A :data:`~typing.TypeAlias` for a 2-level-deep :class:`~Collection`.

Example:

>>> c: CollectionL2[int] = [[1, 2, 3], [4, 5, 6]]
"""

CollectionL3 = Collection[Collection[Collection[_T]]]
"""A :data:`~typing.TypeAlias` for a 3-level-deep :class:`~Collection`.

Example:

>>> c: CollectionL3[int] = [
...     [[1, 2], [3, 4]],
...     [[5, 6], [7, 8]],
... ]
"""

# ========================================================
# ---  Numeric types
# ========================================================

Float = Union[float, np.floating]
"""A :data:`~typing.TypeAlias` for a float type."""

Int = Union[int, np.integer]
"""A :data:`~typing.TypeAlias` for an int type."""

Numeric = Union[Int, Float]
"""A :data:`~typing.TypeAlias` for numeric types."""

NumericT = TypeVar("NumericT", bound=Numeric)


@overload
def _is_numeric(obj: Numeric) -> Literal[True]:
    ...


@overload
def _is_numeric(obj: Any) -> bool:
    ...


def _is_numeric(obj: Any) -> bool:
    """Check if the given object is a :data:`Numeric` type."""
    return isinstance(obj, (int, float, np.number))


# ========================================================
# ---  `Densities` array
# ========================================================

XYCoordinate = Tuple[NumericT, NumericT]
"""A :data:`XYCoordinate` is a :class:`~typing.Tuple` of two numeric values
representing a :math:`(x, y)` coordinate."""

DensityTrace = CollectionL1[XYCoordinate]
"""A 2D line trace is a collection of :math:`(x, y)` tuples
(:data:`XYCoordinate`).

By convention, the :math:`x` values are non-repeating and increasing. For
instance, the following is a valid 2D line trace:

>>> density_trace: DensityTrace = [(0, 0), (1, 1), (2, 2), (3, 3)]
"""

DensitiesRow = CollectionL1[DensityTrace]
r"""A :data:`DensitiesRow` represents a set of :data:`DensityTrace`\s that
are to be plotted on the same row of a ridgeplot.

For instance, the following is a valid ``DensitiesRow``:

>>> densities_row: DensitiesRow = [
...     [(0, 0), (1, 1), (2, 2), (3, 3)],
...     [(0, 0), (1, 1), (2, 2)],
...     [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
... ]
"""

Densities = CollectionL1[DensitiesRow]
r"""The :data:`Densities` type aims at representing the traces that are to be
plotted on a ridgeplot.

In a ridgeplot, several traces can be plotted on different rows. Each row is
represented by a :data:`DensitiesRow` object which, in turn, is a collection of
:data:`DensityTrace`\s. Therefore, the :data:`Densities` type is a collection
of :data:`DensitiesRow`\s.

Note: The ``CollectionL1[DensitiesRow]`` type is equivalent to
``CollectionL3[XYCoordinate]``, which is a type alias for
``Collection[Collection[Collection[Tuple[Numeric, Numeric]]]]``.

For instance, the following is a valid ``Densities`` object:

>>> densities: Densities = [
...     [
...         [(0, 0), (1, 1), (2, 2), (3, 3)],
...         [(0, 0), (1, 1), (2, 2)],
...         [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
...     ],
...     [
...         [(-2, 2), (-1, 1), (0, 1)],
...         [(2, 2), (3, 1), (4, 1)],
...     ],
... ]
"""


ShallowDensities = CollectionL1[DensityTrace]
"""Shallow type for :data:`Densities` where each row of the ridgeplot contains
only a single trace.

Note: The ``CollectionL1[DensityTrace]`` type is equivalent to
``CollectionL2[XYCoordinate]``, which is a type alias for
``Collection[Collection[Tuple[Numeric, Numeric]]]``.
"""


@overload
def is_shallow_densities(obj: ShallowDensities) -> Literal[True]:
    ...


@overload
def is_shallow_densities(obj: Any) -> bool:
    ...


def is_shallow_densities(obj: Any) -> bool:
    """Check if the given object is a :data:`ShallowDensities` type."""

    def is_xy_coord(x: Any) -> bool:
        """Check if the given object is a :data:`XYCoordinate` type."""
        return isinstance(x, tuple) and len(x) == 2 and all(map(_is_numeric, x))

    def is_density_trace(x: Any) -> bool:
        """Check if the given object is a :data:`DensityTrace` type."""
        return isinstance(x, Collection) and all(map(is_xy_coord, x))

    return isinstance(obj, Collection) and all(map(is_density_trace, obj))


# ========================================================
# --- `Samples` array
# ========================================================

SamplesTrace = CollectionL1[Numeric]
"""A :data:`SamplesTrace` is a collection of numeric values representing a
set of samples from which a density trace can be estimated.

i.e. a :data:`SamplesTrace` can be converted into a :data:`DensityTrace` by
applying a kernel density estimation algorithm.
"""

SamplesRow = CollectionL1[SamplesTrace]
r"""A :data:`SamplesRow` represents a set of :data:`SamplesTrace`\s that are to be
plotted on the same row of a ridgeplot.

i.e. a :data:`SamplesRow` is a collection of :data:`SamplesTrace`\s and can be
converted into a :data:`DensitiesRow` by applying a kernel density estimation
algorithm to each trace.
"""

Samples = CollectionL1[SamplesRow]
r"""The :data:`Samples` type aims at representing the samples that are to be
plotted on a ridgeplot.

It is a collection of :data:`SamplesRow` objects. Each row is represented by a
:data:`SamplesRow` type which, in turn, is a collection of :data:`SamplesTrace`\s
which can be converted into :data:`DensityTrace` 's by applying a kernel density
estimation algorithm. Therefore, the :data:`Samples` type can also be converted
into a :data:`Densities` type by applying a kernel density estimation algorithm
to each trace.

See :data:`Densities` for more details.

Note: The ``CollectionL1[SamplesRow]`` type is equivalent to
``CollectionL3[Numeric]`` or ``CollectionL2[Collection[Numeric]]``, which are
both type aliases for ``Collection[Collection[Collection[Numeric]]]``.
"""

ShallowSamples = CollectionL1[SamplesTrace]
"""Shallow type for :data:`Samples` where each row of the ridgeplot contains
only a single trace.

Note: The ``CollectionL1[SamplesTrace]`` type is equivalent to
``CollectionL2[Numeric]`` or ``CollectionL1[Collection[Numeric]]``, which are
both type aliases for ``Collection[Collection[Numeric]]``.
"""


@overload
def is_shallow_samples(obj: ShallowSamples) -> Literal[True]:
    ...


@overload
def is_shallow_samples(obj: Any) -> bool:
    ...


def is_shallow_samples(obj: Any) -> bool:
    """Check if the given object is a :data:`ShallowSamples` type."""

    def is_trace_samples(x: Any) -> bool:
        """Check if the given object is a :data:`SamplesTrace` type."""
        return isinstance(x, Collection) and all(map(_is_numeric, x))

    return isinstance(obj, Collection) and all(map(is_trace_samples, obj))


# ========================================================
# ---  Shallow types
# ========================================================


@overload
def is_flat_str_collection(obj: Collection[str]) -> Literal[True]:
    ...


@overload
def is_flat_str_collection(obj: Any) -> bool:
    ...


def is_flat_str_collection(obj: Any) -> bool:
    """Check if the given object is a :data:`CollectionL1[str]` type but not a
    string itself."""
    if isinstance(obj, str):
        # Catch edge case where the obj is actually a
        # str collection, but it is a string itself
        return False
    return isinstance(obj, Collection) and all(map(lambda x: isinstance(x, str), obj))


def nest_shallow_collection(shallow_collection: CollectionL2[_T]) -> CollectionL3[_T]:
    """Internal helper to convert a shallow collection type into a deep
    collection type.

    This function should really only be used in the ``ridgeplot._ridgeplot``
    module to normalize user input.
    """
    return [[x] for x in shallow_collection]
