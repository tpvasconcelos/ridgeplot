from __future__ import annotations

import sys
from enum import Enum
from typing import Final, Literal

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias


if "_is_loaded" in globals():
    raise RuntimeError("Reloading ridgeplot._missing is not allowed")
_is_loaded = True


class _Missing(Enum):
    """
    A singleton class that represents a missing value.

    This implementation was mainly inspired by the discussions in
    `#236 (typing)`_, `#40397 (pandas)`_, and on the current
    implementation of `pandas._libs.lib._NoDefault`_.

    For reference, here are other discussions and implementations that
    were also considered:

    - `PEP 484 - Support for singleton types in unions`_
    - `#7844 (numpy)`_
    - `#16241 (numpy)`_
    - `numpy._globals._NoValueType`_
    - `dataclasses.MISSING`_

    .. _#236 (typing): https://github.com/python/typing/issues/236
    .. _#40397 (pandas): https://github.com/pandas-dev/pandas/issues/40397
    .. _pandas._libs.lib._NoDefault: https://github.com/pandas-dev/pandas/blob/faeedade7966d6f2a5b601c26205a71362913c47/pandas/_libs/lib.pyx#L2817-L2829
    .. _PEP 484 - Support for singleton types in unions: https://peps.python.org/pep-0484/#support-for-singleton-types-in-unions
    .. _#7844 (numpy): https://github.com/numpy/numpy/issues/7844
    .. _#16241 (numpy): https://github.com/numpy/numpy/pull/16241
    .. _numpy._globals._NoValueType: https://github.com/numpy/numpy/blob/57e80500f3998d62e2da459e487f8682bffa9454/numpy/_globals.py
    .. _dataclasses.MISSING: https://github.com/python/cpython/blob/403ab1306a6e9860197bce57eadcb83418966f21/Lib/dataclasses.py#L182-L186
    """

    MISSING = "MISSING"

    def __repr__(self) -> str:
        return "<MISSING>"


MISSING: Final = _Missing.MISSING
MissingType: TypeAlias = Literal[_Missing.MISSING]
