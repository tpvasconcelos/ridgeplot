"""Miscellaneous types, type aliases, type guards, and other related utilities
used throughout the package."""

from __future__ import annotations

from collections.abc import Collection
from typing import Optional, Union

import numpy as np
from typing_extensions import Any, Literal, TypeIs, TypeVar

# Snippet used to generate and store the image artefacts:
# >>> def save_fig(fig, name):
# ...     height = 400
# ...     width = 800
# ...     fig.update_layout(
# ...         height=height,
# ...         width=width,
# ...         margin=dict(l=0, r=0, t=40, b=0),
# ...         showlegend=False,
# ...     )
# ...     out = f"docs/_static/img/api/types/{name}.webp"
# ...     print(f"Writing to: {out}")
# ...     fig.write_image(
# ...         out,
# ...         format="webp",
# ...         width=width,
# ...         height=height,
# ...         scale=2,
# ...         engine="kaleido",
# ...     )


_T = TypeVar("_T")

# ========================================================
# ---  Miscellaneous types
# ========================================================

Color = Union[str, tuple[float, float, float]]
"""A color can be represented by a tuple of ``(r, g, b)`` values or any valid
CSS color string - including hex, rgb/a, hsl/a, hsv/a, and named CSS colors."""

ColorScale = Collection[tuple[float, Color]]
"""The canonical form for a color scale is represented by a list of tuples of
two elements:

0. the first element (a *scale value*) is a float bounded to the
   interval ``[0, 1]``
1. the second element should be a valid :data:`Color` representation.

For instance, the Viridis color scale can be represented as:

>>> viridis: ColorScale = [
  (0.0, 'rgb(68, 1, 84)'),
  (0.1111111111111111, 'rgb(72, 40, 120)'),
  (0.2222222222222222, 'rgb(62, 73, 137)'),
  (0.3333333333333333, 'rgb(49, 104, 142)'),
  (0.4444444444444444, 'rgb(38, 130, 142)'),
  (0.5555555555555556, 'rgb(31, 158, 137)'),
  (0.6666666666666666, 'rgb(53, 183, 121)'),
  (0.7777777777777777, 'rgb(110, 206, 88)'),
  (0.8888888888888888, 'rgb(181, 222, 43)'),
  (1.0, 'rgb(253, 231, 37)')
]
"""

NormalisationOption = Literal["probability", "percent"]
"""A :data:`~typing.Literal` type that represents the normalisation options
available for the ridgeplot. See :paramref:`ridgeplot.ridgeplot.norm` for more
details."""

# ========================================================
# ---  Base nested Collection types (ragged arrays)
# ========================================================

CollectionL1 = Collection[_T]
"""A :data:`~typing.TypeAlias` for a 1-level-deep :class:`~collections.abc.Collection`.

Example
-------

>>> c1 = [1, 2, 3]
"""

CollectionL2 = Collection[Collection[_T]]
"""A :data:`~typing.TypeAlias` for a 2-level-deep :class:`~collections.abc.Collection`.

Example
-------

>>> c2 = [[1, 2, 3], [4, 5, 6]]
"""

CollectionL3 = Collection[Collection[Collection[_T]]]
"""A :data:`~typing.TypeAlias` for a 3-level-deep :class:`~collections.abc.Collection`.

Example
-------

>>> c3 = [
...     [[1, 2], [3, 4]],
...     [[5, 6], [7, 8]],
... ]
"""

# ========================================================
# ---  Numeric types
# ========================================================

Float = Union[float, np.floating[Any]]
"""A :data:`~typing.TypeAlias` for float types."""

Int = Union[int, np.integer[Any]]
"""A :data:`~typing.TypeAlias` for a int types."""

Numeric = Union[Int, Float]
"""A :data:`~typing.TypeAlias` for *numeric* types."""

NumericT = TypeVar("NumericT", bound=Numeric)
"""A :class:`~typing.TypeVar` variable bound to :data:`Numeric` types."""


def _is_numeric(obj: Any) -> TypeIs[Numeric]:
    """Type guard for :data:`Numeric`.

    Examples
    --------
    >>> _is_numeric(42)
    True
    >>> _is_numeric(12.3)
    True
    >>> _is_numeric(np.int64(17))
    True
    >>> _is_numeric(np.float64(3.14))
    True
    >>> _is_numeric("42")
    False
    >>> _is_numeric("12.3")
    False
    >>> _is_numeric([42])
    False
    >>> _is_numeric(None)
    False
    """
    return isinstance(obj, (int, float, np.number))


# ========================================================
# ---  `Densities` array
# ========================================================

XYCoordinate = tuple[Numeric, Numeric]
"""A 2D :math:`(x, y)` coordinate, represented as a :class:`~tuple` of
two :data:`Numeric` values.

Example
-------

>>> xy_coord = (1, 2)
"""

DensityTrace = CollectionL1[XYCoordinate]
r"""A 2D line/trace represented as a collection of :math:`(x, y)` coordinates
(i.e. :data:`XYCoordinate`\s).

These are equivalent:

- ``DensityTrace``
- ``CollectionL1[XYCoordinate]``
- ``Collection[tuple[Numeric, Numeric]]``

By convention, the :math:`x` values should be non-repeating and increasing. For
instance, the following is a valid 2D line trace:

.. tab-set::

    .. tab-item:: Code example

        >>> density_trace = [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)]

    .. tab-item:: Graphical representation

        ..
            The plot below was generated using the following code:
            >>> save_fig(ridgeplot(densities=[[density_trace]]), "density_trace")

        .. image:: /_static/img/api/types/density_trace.webp

"""

DensitiesRow = CollectionL1[DensityTrace]
r"""A :data:`DensitiesRow` represents a set of :data:`DensityTrace`\s that
are to be plotted on a given row of a ridgeplot.

These are equivalent:

- ``DensitiesRow``
- ``CollectionL2[XYCoordinate]``
- ``Collection[Collection[Tuple[Numeric, Numeric]]]``

Example
-------

.. tab-set::

    .. tab-item:: Code example

        >>> densities_row = [
        ...     [(0, 0), (1, 1), (2, 0)],                 # Trace 1
        ...     [(1, 0), (2, 1), (3, 2), (4, 1)],         # Trace 2
        ...     [(3, 0), (4, 1), (5, 2), (6, 1), (7, 0)], # Trace 3
        ... ]

    .. tab-item:: Graphical representation

        ..
            The plot below was generated using the following code:
            >>> save_fig(ridgeplot(densities=[densities_row]), "densities_row")

        .. image:: /_static/img/api/types/densities_row.webp
"""

Densities = CollectionL1[DensitiesRow]
r"""The :data:`Densities` type represents the entire collection of traces that
are to be plotted on a ridgeplot.

In a ridgeplot, several traces can be plotted on different rows. Each row is
represented by a :data:`DensitiesRow` object which, in turn, is a collection of
:data:`DensityTrace`\s. Therefore, the :data:`Densities` type is a collection
of :data:`DensitiesRow`\s.

These are equivalent:

- ``Densities``
- ``CollectionL1[DensitiesRow]``
- ``CollectionL3[XYCoordinate]``
- ``Collection[Collection[Collection[Tuple[Numeric, Numeric]]]]``

Example
-------

.. tab-set::

    .. tab-item:: Code example

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

    .. tab-item:: Graphical representation

        ..
            The plot below was generated using the following code:
            >>> save_fig(ridgeplot(densities=densities, spacing=1), "densities")

        .. image:: /_static/img/api/types/densities.webp
"""


ShallowDensities = CollectionL1[DensityTrace]
"""Shallow type for :data:`Densities` where each row of the ridgeplot contains
only a single trace.

These are equivalent:

- ``Densities``
- ``CollectionL1[DensityTrace]``
- ``CollectionL2[XYCoordinate]``
- ``Collection[Collection[Tuple[Numeric, Numeric]]]``

Example
-------

.. tab-set::

    .. tab-item:: Code example

        >>> shallow_densities = [
        ...     [(0, 0), (1, 1), (2, 0)], # Trace 1
        ...     [(1, 0), (2, 1), (3, 0)], # Trace 2
        ...     [(2, 0), (3, 1), (4, 0)], # Trace 3
        ... ]

    .. tab-item:: Graphical representation

        ..
            The plot below was generated using the following code:
            >>> save_fig(ridgeplot(densities=shallow_densities), "shallow_densities")

        .. image:: /_static/img/api/types/shallow_densities.webp
"""


def is_xy_coord(obj: Any) -> TypeIs[XYCoordinate]:
    """Type guard for :data:`XYCoordinate`."""
    return isinstance(obj, tuple) and len(obj) == 2 and all(map(_is_numeric, obj))


def is_density_trace(obj: Any) -> TypeIs[DensityTrace]:
    """Type guard for :data:`DensityTrace`."""
    return isinstance(obj, Collection) and all(map(is_xy_coord, obj))


def is_shallow_densities(obj: Any) -> TypeIs[ShallowDensities]:
    """Type guard for :data:`ShallowDensities`.

    Examples
    --------
    >>> is_shallow_densities("definitely not")
    False
    >>> is_shallow_densities([["also"], ["not"]])
    False
    >>> deep_density = [
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
    >>> is_shallow_densities(deep_density)
    False
    >>> shallow_density = [[(0, 0), (1, 1)], [(2, 2), (3, 1)]]
    >>> is_shallow_densities(shallow_density)
    True
    >>> shallow_samples = [[0, 1, 2], [2, 3, 4]]
    >>> is_shallow_densities(shallow_samples)
    False
    """
    return isinstance(obj, Collection) and all(map(is_density_trace, obj))


# ========================================================
# --- `Samples` array
# ========================================================

SamplesTrace = CollectionL1[Numeric]
"""A :data:`SamplesTrace` is a collection of numeric values representing a
set of samples from which a :data:`DensityTrace` can be estimated via KDE.

Example
-------

.. tab-set::

    .. tab-item:: Code example

        >>> samples_trace = [0, 1, 1, 2, 2, 2, 3, 3, 4]

    .. tab-item:: Graphical representation

        ..
            The plot below was generated using the following code:
            >>> save_fig(ridgeplot(samples=[[samples_trace]]), "samples_trace")

        .. image:: /_static/img/api/types/samples_trace.webp
"""

SamplesRow = CollectionL1[SamplesTrace]
r"""A :data:`SamplesRow` represents a set of :data:`SamplesTrace`\s that are to be
plotted on a given row of a ridgeplot.

i.e. a :data:`SamplesRow` is a collection of :data:`SamplesTrace`\s and can be
converted into a :data:`DensitiesRow` by applying KDE to each trace.

Example
-------

.. tab-set::

    .. tab-item:: Code example

        >>> samples_row = [
        ...     [0, 1, 1, 2, 2, 2, 3, 3, 4], # Trace 1
        ...     [1, 2, 2, 3, 3, 3, 4, 4, 5], # Trace 2
        ... ]

    .. tab-item:: Graphical representation

        ..
            The plot below was generated using the following code:
            >>> save_fig(ridgeplot(samples=[samples_row]), "samples_row")

        .. image:: /_static/img/api/types/samples_row.webp
"""

Samples = CollectionL1[SamplesRow]
r"""The :data:`Samples` type represents the entire collection of samples that
are to be plotted on a ridgeplot.

It is a collection of :data:`SamplesRow` objects. Each row is represented by a
:data:`SamplesRow` type which, in turn, is a collection of :data:`SamplesTrace`\s
which can be converted into :data:`DensityTrace` 's by applying a kernel density
estimation algorithm.

Therefore, the :data:`Samples` type can be converted into a :data:`Densities`
type by applying a kernel density estimation (KDE) algorithm to each trace.

See :data:`Densities` for more details.

Example
-------

.. tab-set::

    .. tab-item:: Code example

        >>> samples = [
        ...     [                                # Row 1
        ...         [0, 1, 1, 2, 2, 2, 3, 3, 4], # Trace 1
        ...         [1, 2, 2, 3, 3, 3, 4, 4, 5], # Trace 2
        ...     ],
        ...     [                                # Row 2
        ...         [2, 3, 3, 4, 4, 4, 5, 5, 6], # Trace 3
        ...         [3, 4, 4, 5, 5, 5, 6, 6, 7], # Trace 4
        ...     ],
        ... ]

    .. tab-item:: Graphical representation

        ..
            The plot below was generated using the following code:
            >>> save_fig(ridgeplot(samples=samples), "samples")

        .. image:: /_static/img/api/types/samples.webp
"""

ShallowSamples = CollectionL1[SamplesTrace]
"""Shallow type for :data:`Samples` where each row of the ridgeplot contains
only a single trace.

Example
-------

.. tab-set::

    .. tab-item:: Code example

        >>> shallow_samples = [
        ...     [0, 1, 1, 2, 2, 2, 3, 3, 4], # Trace 1
        ...     [1, 2, 2, 3, 3, 3, 4, 4, 5], # Trace 2
        ... ]

    .. tab-item:: Graphical representation

        ..
            The plot below was generated using the following code:
            >>> save_fig(ridgeplot(samples=shallow_samples), "shallow_samples")

        .. image:: /_static/img/api/types/shallow_samples.webp
"""


def is_trace_samples(obj: Any) -> TypeIs[SamplesTrace]:
    """Check if the given object is a :data:`SamplesTrace` type."""
    return isinstance(obj, Collection) and all(map(_is_numeric, obj))


def is_shallow_samples(obj: Any) -> TypeIs[ShallowSamples]:
    """Type guard for :data:`ShallowSamples`.

    Examples
    --------
    >>> is_shallow_samples("definitely not")
    False
    >>> is_shallow_samples([["also"], ["not"]])
    False
    >>> deep_samples = [
    ...     [
    ...         [0, 0, 1, 1, 2, 2, 3, 3],
    ...         [0, 0, 1, 1, 2, 2],
    ...         [0, 0, 1, 1, 2, 2, 3, 3, 4, 4],
    ...     ],
    ...     [
    ...         [-2, 2, -1, 1, 0, 1],
    ...         [2, 2, 3, 1, 4, 1],
    ...     ],
    ... ]
    >>> is_shallow_samples(deep_samples)
    False
    >>> shallow_samples = [[0, 1, 2], [2, 3, 4]]
    >>> is_shallow_samples(shallow_samples)
    True
    >>> shallow_density = [[(0, 0), (1, 1)], [(2, 2), (3, 1)]]
    >>> is_shallow_samples(shallow_density)
    False
    """
    return isinstance(obj, Collection) and all(map(is_trace_samples, obj))


# ========================================================
# ---  Other array types
# ========================================================


# Trace types ---

TraceType = Literal["area", "bar"]
"""The type of trace to draw in a ridgeplot. See
:paramref:`ridgeplot.ridgeplot.trace_type` for more information."""

TraceTypesArray = CollectionL2[TraceType]
"""A :data:`TraceTypesArray` represents the types of traces in a ridgeplot.

Example
-------
>>> trace_types_array: TraceTypesArray = [
...     ["area", "bar", "area"],
...     ["bar", "area"],
... ]
"""

ShallowTraceTypesArray = CollectionL1[TraceType]
"""Shallow type for :data:`TraceTypesArray`.

Example
-------
>>> trace_types_array: ShallowTraceTypesArray = ["area", "bar", "area"]
"""


def is_trace_type(obj: Any) -> TypeIs[TraceType]:
    """Type guard for :data:`TraceType`.

    Examples
    --------
    >>> is_trace_type("area")
    True
    >>> is_trace_type("bar")
    True
    >>> is_trace_type("foo")
    False
    >>> is_trace_type(42)
    False
    """
    from typing_extensions import get_args

    return isinstance(obj, str) and obj in get_args(TraceType)


def is_shallow_trace_types_array(obj: Any) -> TypeIs[ShallowTraceTypesArray]:
    """Type guard for :data:`ShallowTraceTypesArray`.

    Examples
    --------
    >>> is_shallow_trace_types_array(["area", "bar", "area"])
    True
    >>> is_shallow_trace_types_array(["area", "bar", "foo"])
    False
    >>> is_shallow_trace_types_array([1, 2, 3])
    False
    """
    return isinstance(obj, Collection) and all(map(is_trace_type, obj))


def is_trace_types_array(obj: Any) -> TypeIs[TraceTypesArray]:
    """Type guard for :data:`TraceTypesArray`.

    Examples
    --------
    >>> is_trace_types_array([["area", "bar"], ["area", "bar"]])
    True
    >>> is_trace_types_array([["area", "bar"], ["area", "foo"]])
    False
    >>> is_trace_types_array([["area", "bar"], ["area", 42]])
    False
    """
    return isinstance(obj, Collection) and all(map(is_shallow_trace_types_array, obj))


# Labels ---

LabelsArray = CollectionL2[str]
"""A :data:`LabelsArray` represents the labels of traces in a ridgeplot.

Example
-------

>>> labels_array: LabelsArray = [
...     ["trace 1", "trace 2", "trace 3"],
...     ["trace 4", "trace 5"],
... ]
"""

ShallowLabelsArray = CollectionL1[str]
"""Shallow type for :data:`LabelsArray`.

Example
-------

>>> labels_array: ShallowLabelsArray = ["trace 1", "trace 2", "trace 3"]
"""

# Sample weights ---

SampleWeights = Optional[CollectionL1[Numeric]]
"""An array of KDE weights corresponding to each sample."""

SampleWeightsArray = CollectionL2[SampleWeights]
"""A :data:`SampleWeightsArray` represents the weights of the datapoints in a
:data:`Samples` array. The shape of the :data:`SampleWeightsArray` array should
match the shape of the corresponding :data:`Samples` array."""

ShallowSampleWeightsArray = CollectionL1[SampleWeights]
"""Shallow type for :data:`SampleWeightsArray`."""

# ========================================================
# ---  More type guards and other utilities
# ========================================================


def is_flat_str_collection(obj: Any) -> TypeIs[CollectionL1[str]]:
    """Type guard for :data:`CollectionL1[str]`.

    Note that this type-guard explicitly excludes the case where the object is
    a string itself (which can be considered a collection of string characters).

    Examples
    --------
    >>> is_flat_str_collection(["a", "b", "c"])
    True
    >>> is_flat_str_collection("abc")
    False
    >>> is_flat_str_collection(["a", "b", 1])
    False
    >>> is_flat_str_collection({"also", "a", "collection"})
    True
    >>> is_flat_str_collection((1, 2))
    False
    """
    if isinstance(obj, str):
        # Catch edge case where the obj is actually a
        # str collection, but it is a string itself
        return False
    return isinstance(obj, Collection) and all(isinstance(x, str) for x in obj)


def is_flat_numeric_collection(obj: Any) -> TypeIs[CollectionL1[Numeric]]:
    """Type guard for :data:`CollectionL1[Numeric]`.

    Examples
    --------
    >>> is_flat_numeric_collection({1, 2, 3.14})
    True
    >>> is_flat_numeric_collection((1, np.nan, np.inf))
    True
    >>> is_flat_numeric_collection([3.14, np.float64(2.71), np.int64(42)])
    True
    >>> is_flat_numeric_collection([1, 2, "3"])
    False
    >>> is_flat_numeric_collection([1, 2, None])
    False
    >>> is_flat_numeric_collection("definitely not")
    False
    """
    return isinstance(obj, Collection) and all(map(_is_numeric, obj))


def nest_shallow_collection(shallow_collection: Collection[_T]) -> Collection[Collection[_T]]:
    """Convert a *shallow* collection type into a *deep* collection type.

    This function should really only be used in the :mod:`ridgeplot._ridgeplot`
    module to normalise user input.

    Examples
    --------
    >>> nest_shallow_collection([1, "2", {"a": 3}])
    [[1], ['2'], [{'a': 3}]]
    """
    return [[x] for x in shallow_collection]
