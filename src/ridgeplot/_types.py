from __future__ import annotations

import sys
from typing import Collection, Iterable, Tuple, TypeVar, Union

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import numpy as np
from numpy import typing as npt

_T_co = TypeVar("_T_co", covariant=True)


class SimpleSequence(Collection[_T_co], Protocol[_T_co]):
    """A simple Sequence protocol that inherits from
    :class:`~collections.abc.Collection` and implements a ``__getitem__``
    method."""

    def __getitem__(self, index: int) -> _T_co:
        ...


Numeric = Union[int, float, np.number]
"""A :class:`~typing.TypeAlias` for numeric types."""

NumericT = TypeVar("NumericT", bound=Numeric)
"""A :class:`~typing.TypeVar` version of :class:`Numeric`."""

NestedNumericSequence = Union[SimpleSequence[SimpleSequence[Numeric]], npt.NDArray[np.number]]
"""A :class:`~typing.TypeAlias` for a sequence of sequences of numeric values.

Examples of valid types:

    >>> [[1, 2], [3, 4]]
    >>> ((1, 2), [3, 4])
    >>> np.array([[1, 2], [3, 4]])
    >>> np.array([[1, 2], [3, 4]], dtype=np.float32)
"""

NestedNumericSequenceT = Union[SimpleSequence[SimpleSequence[NumericT]], npt.NDArray[NumericT]]
"""Same as :data:`NestedNumericSequence`, but with a :data:`NumericT`
type variable bound to :data:`Numeric` instead the :data:`Numeric` type
alias."""

ColorScaleType = Iterable[Tuple[float, str]]
"""A colorscale is an :class:`~typing.Iterable` of tuples of two elements:

0. the first element (a *scale value*) is a float bounded to the
   interval ``[0, 1]``
1. the second element (a *color*) is a string representation of a color parsable
   by Plotly

For instance, The Viridis colorscale would be defined as

>>> get_colorscale("viridis")
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
