from __future__ import annotations

import sys
from typing import Any, Callable, Collection, Iterable, Tuple, TypeVar, Union, overload

from statsmodels.sandbox.nonparametric.kernels import CustomKernel as StatsmodelsKernel

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

import numpy as np

# ========================================================
# ---  Internal base Collection types
# ========================================================

_T = TypeVar("_T")

_CollectionL1 = Collection[_T]
"""A :class:`~typing.TypeAlias` for a (standard) shallow :class:`~Collection`
(1 level).

Example:

>>> c: CollectionL1[int] = [1, 2, 3]
"""

_CollectionL2 = Collection[Collection[_T]]
"""A :class:`~typing.TypeAlias` for a 2-level-deep :class:`~Collection`.

Example:

>>> c: CollectionL2[int] = [[1, 2, 3], [4, 5, 6]]
"""

_CollectionL3 = Collection[Collection[Collection[_T]]]
"""A :class:`~typing.TypeAlias` for a 3-level-deep :class:`~Collection`.

Example:

>>> c: CollectionL3[int] = [
...     [[1, 2], [3, 4]],
...     [[5, 6], [7, 8]],
... ]
"""

# ========================================================
# ---  Basic types
# ========================================================

NumericT = Union[int, float, np.number]
"""A :class:`~typing.TypeAlias` for numeric types."""


@overload
def _is_numeric(obj: NumericT) -> Literal[True]:
    ...


def _is_numeric(obj: Any) -> bool:
    """Check if the given object is a :data:`Numeric` type."""
    return isinstance(obj, (int, float, np.number))


KDEPointsT = Union[int, _CollectionL1[NumericT]]
KDEBandwidthT = Union[str, float, Callable[[_CollectionL1[NumericT], StatsmodelsKernel], float]]

ColorScaleT = Iterable[Tuple[float, str]]
"""A colorscale is an iterable of tuples of two elements:

0. the first element (a *scale value*) is a float bounded to the
   interval ``[0, 1]``
1. the second element (a *color*) is a string representation of a color parsable
   by Plotly

For instance, the Viridis colorscale would be defined as

>>> get_colorscale("viridis")
((0.0, 'rgb(68, 1, 84)'),
 (0.1111111111111111, 'rgb(72, 40, 120)'),
 (0.2222222222222222, 'rgb(62, 73, 137)'),
 (0.3333333333333333, 'rgb(49, 104, 142)'),
 (0.4444444444444444, 'rgb(38, 130, 142)'),
 (0.5555555555555556, 'rgb(31, 158, 137)'),
 (0.6666666666666666, 'rgb(53, 183, 121)'),
 (0.7777777777777777, 'rgb(110, 206, 88)'),
 (0.8888888888888888, 'rgb(181, 222, 43)'),
 (1.0, 'rgb(253, 231, 37)'))
"""

LabelsArray = _CollectionL2[str]
"""A :data:`LabelsArray` represents the labels of traces in a ridgeplot.

For instance, the following is a valid :data:`LabelsArray`:

>>> labels_array: LabelsArray = [
...     ["trace 1", "trace 2", "trace 3"],
...     ["trace 4", "trace 5"],
... ]
"""

ColorsArrayT = _CollectionL2[str]
"""A :data:`ColorsArray` represents the colors of traces in a ridgeplot.

For instance, the following is a valid :data:`ColorsArray`:

>>> colors_array: ColorsArray = [
...     ["red", "blue", "green"],
...     ["orange", "purple"],
... ]
"""

MidpointsArrayT = _CollectionL2[NumericT]
"""A :data:`MidpointsArray` represents the midpoints of colorscales in a
ridgeplot.

For instance, the following is a valid :data:`MidpointsArray`:

>>> midpoints_array: MidpointsArray = [
...     [0.2, 0.5, 1],
...     [0.3, 0.7],
... ]
"""

# ========================================================
# ---  `Densities` type
# ========================================================

XYCoordinateT = Tuple[NumericT, NumericT]
"""A :data:`XYCoordinate` is a :class:`~typing.Tuple` of two numeric values
representing a :math:`(x, y)` coordinate."""

DensityTraceT = _CollectionL1[XYCoordinateT]
"""A 2D line trace is a collection of :math:`(x, y)` tuples
(:data:`XYCoordinate`).

By convention, the :math:`x` values are non-repeating and increasing. For
instance, the following is a valid 2D line trace:

>>> density_trace: DensityTrace = [(0, 0), (1, 1), (2, 2), (3, 3)]
"""

DensitiesRowT = _CollectionL1[DensityTraceT]
"""A :data:`DensitiesRow` represents a set of :data:`DensityTrace`s that are to
be plotted on the same row of a ridgeplot.

For instance, the following is a valid ``DensitiesRow``:

>>> densities_row: DensitiesRow = [
...     [(0, 0), (1, 1), (2, 2), (3, 3)],
...     [(0, 0), (1, 1), (2, 2)],
...     [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
... ]
"""

DensitiesT = _CollectionL1[DensitiesRowT]
"""The :data:`Densities` type aims at representing the traces that are to be
plotted on a ridgeplot.

In a ridgeplot, several traces can be plotted on different rows. Each row is
represented by a :data:`DensitiesRow` object which, in turn, is a collection of
:data:`DensityTrace`s. Therefore, the :data:`Densities` type is a collection
of :data:`DensitiesRow`s.

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

# ========================================================
# --- `Samples` type
# ========================================================

SamplesTraceT = _CollectionL1[NumericT]
"""A :data:`SamplesTrace` is a collection of numeric values representing a
set of samples from which a density trace can be estimated.

i.e. a :data:`SamplesTrace` can be converted into a :data:`DensityTrace` by
applying a kernel density estimation algorithm.
"""

SamplesRowT = _CollectionL1[SamplesTraceT]
"""A :data:`SamplesRow` represents a set of :data:`SamplesTrace`s that are to be
plotted on the same row of a ridgeplot.

i.e. a :data:`SamplesRow` is a collection of :data:`SamplesTrace`s and can be
converted into a :data:`DensitiesRow` by applying a kernel density estimation
algorithm to each trace.
"""

SamplesT = _CollectionL1[SamplesRowT]
"""The :data:`Samples` type aims at representing the samples that are to be
plotted on a ridgeplot.

It is a collection of :data:`SamplesRow`s. Each row is represented by a
:data:`SamplesRow` type which, in turn, is a collection of :data:`SamplesTrace`s
which can be converted into :data:`DensityTrace`s by applying a kernel density
estimation algorithm. Therefore, the :data:`Samples` type can also be converted
into a :data:`Densities` type by applying a kernel density estimation algorithm
to each trace.

See :data:`Densities` for more details.

Note: The ``CollectionL1[SamplesRow]`` type is equivalent to
``CollectionL3[Numeric]`` or ``CollectionL2[Collection[Numeric]]``, which are
both type aliases for ``Collection[Collection[Collection[Numeric]]]``.
"""

# ========================================================
# ---  Deprecated shallow types
# ========================================================


ShallowLabelsArrayT = _CollectionL1[str]
"""Deprecated shallow type for :data:`LabelsArray`.

Example:

>>> labels_array: ShallowLabelsArray = ["trace 1", "trace 2", "trace 3"]
"""

ShallowColorsArrayT = _CollectionL1[str]
"""Deprecated shallow type for :data:`ColorsArray`.

Example:

>>> colors_array: ShallowColorsArray = ["red", "blue", "green"]
"""


@overload
def is_flat_str_collection(obj: Collection[str]) -> Literal[True]:
    ...


def is_flat_str_collection(obj: Any) -> bool:
    """Check if the given object is a :data:`CollectionL1[str]` type but not a
    string itself."""
    if isinstance(obj, str):
        # Catch edge case where the obj is actually a
        # str collection, but it is a string itself
        return False
    return isinstance(obj, Collection) and all(map(lambda x: isinstance(x, str), obj))


ShallowDensitiesT = _CollectionL1[DensityTraceT]
"""Deprecated shallow type for :data:`Densities` where each row of the ridgeplot
contains only a single trace.

Note: The ``CollectionL1[DensityTrace]`` type is equivalent to
``CollectionL2[XYCoordinate]``, which is a type alias for
``Collection[Collection[Tuple[Numeric, Numeric]]]``.
"""


@overload
def is_shallow_densities(obj: ShallowDensitiesT) -> Literal[True]:
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


ShallowSamplesT = _CollectionL1[SamplesTraceT]
"""Deprecated shallow type for :data:`Samples` where each row of the ridgeplot
contains only a single trace.

Note: The ``CollectionL1[SamplesTrace]`` type is equivalent to
``CollectionL2[Numeric]`` or ``CollectionL1[Collection[Numeric]]``, which are
both type aliases for ``Collection[Collection[Numeric]]``.
"""


@overload
def is_shallow_samples(obj: ShallowSamplesT) -> Literal[True]:
    ...


def is_shallow_samples(obj: Any) -> bool:
    """Check if the given object is a :data:`ShallowSamples` type."""

    def is_trace_samples(x: Any) -> bool:
        """Check if the given object is a :data:`SamplesTrace` type."""
        return isinstance(x, Collection) and all(map(_is_numeric, x))

    return isinstance(obj, Collection) and all(map(is_trace_samples, obj))


def nest_shallow_collection(shallow_collection: _CollectionL2[_T]) -> _CollectionL3[_T]:
    """Internal helper to convert a shallow collection type into a deep
    collection type.

    This function should really only be used in the ``ridgeplot._ridgeplot``
    module to normalize user input.
    """
    return [[x] for x in shallow_collection]
