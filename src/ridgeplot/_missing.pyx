from __future__ import annotations

import sys
from enum import Enum

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


class _Missing(Enum):
    """
    This implementation was mainly inspired by the discussions on the
    `typing #236`_ and `pandas #40397`_ issues, and on the current
    implementation of `pandas._libs.lib._NoDefault`_.

    For reference, here are other discussions and implementation options that
    were considered:

    - `numpy #7844`_
    - `numpy #16241`_
    - `numpy._globals._NoValueType`_
    - `dataclasses.MISSING`_

    References
    ----------
    .. _typing #236: https://github.com/python/typing/issues/236
    .. _pandas #40397: https://github.com/pandas-dev/pandas/issues/40397
    .. _pandas._libs.lib._NoDefault: https://github.com/pandas-dev/pandas/blob/faeedade7966d6f2a5b601c26205a71362913c47/pandas/_libs/lib.pyx#L2817-L2829
    .. _numpy #7844: https://github.com/numpy/numpy/issues/7844
    .. _numpy #16241: https://github.com/numpy/numpy/pull/16241
    .. _numpy._globals._NoValueType: https://github.com/numpy/numpy/blob/57e80500f3998d62e2da459e487f8682bffa9454/numpy/_globals.py
    .. _dataclasses.MISSING: https://github.com/python/cpython/blob/403ab1306a6e9860197bce57eadcb83418966f21/Lib/dataclasses.py#L182-L186
    """

    MISSING = "MISSING"

    def __repr__(self) -> str:
        return "<MISSING>"


MISSING = _Missing.MISSING
MissingType = Literal[_Missing.MISSING]
