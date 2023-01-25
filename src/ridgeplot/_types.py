import sys
from typing import Collection, TypeVar, Union

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import numpy as np
from numpy import typing as npt

_T_co = TypeVar("_T_co", covariant=True)


class _SimpleSequence(Collection[_T_co], Protocol[_T_co]):
    def __getitem__(self, index: int) -> _T_co:
        ...


Numeric = Union[int, float, np.number]
NumericT = TypeVar("NumericT", bound=Numeric)

NestedNumericSequence = Union[_SimpleSequence[_SimpleSequence[Numeric]], npt.NDArray[np.number]]
NestedNumericSequenceT = Union[_SimpleSequence[_SimpleSequence[NumericT]], npt.NDArray[NumericT]]
