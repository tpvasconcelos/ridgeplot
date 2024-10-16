# Copyright (c) 2012 Erik Rose
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ==============================================================================
#
# This module contains an adapted version of more-itertools's implementation of
# the `zip_equal` function. The original source code can be found at:
# https://github.com/more-itertools/more-itertools/
#
# This vendorized version is used to avoid adding more-itertools as dependency
# to the project just for this single function.
#
# Once support for Python 3.9 is dropped, this module can be removed and the
# `zip_equal` function can be replaced with the built-in `zip` function, which
# (since Python 3.10) supports the `strict` parameter to raise an exception if
# the iterables have different lengths.
#
# The original license is included above.
#

from __future__ import annotations

import functools
import sys
from itertools import zip_longest
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Collection, Iterable

_marker = object()


class UnequalIterablesError(ValueError):
    def __init__(self, details: tuple[int, int, int] | None = None) -> None:
        msg = "Iterables have different lengths"
        if details is not None:
            msg += ": index 0 has length {}; index {} has length {}".format(*details)

        super().__init__(msg)


def _zip_equal_generator(iterables: Iterable[Any]) -> Iterable[tuple[Any, ...]]:
    for combo in zip_longest(*iterables, fillvalue=_marker):
        for val in combo:
            if val is _marker:
                raise UnequalIterablesError
        yield combo


def _zip_equal(*iterables: Collection[Any]) -> Iterable[tuple[Any, ...]]:
    # Check whether the iterables are all the same size.
    try:
        first_size = len(iterables[0])
        for i, it in enumerate(iterables[1:], 1):
            size = len(it)
            if size != first_size:
                raise UnequalIterablesError(details=(first_size, i, size))
        # All sizes are equal, we can use the built-in zip.
        return zip(*iterables)
    # If any one of the iterables didn't have a length, start reading
    # them until one runs out.
    except TypeError:
        return _zip_equal_generator(iterables)


if sys.version_info >= (3, 10):
    zip_strict = functools.partial(zip, strict=True)
else:
    zip_strict = _zip_equal
