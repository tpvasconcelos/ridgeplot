from __future__ import annotations

from typing import Any

import numpy as np
import pytest

from ridgeplot._types import (
    _is_numeric,
    is_flat_str_collection,
    is_shallow_densities,
    is_shallow_samples,
)


@pytest.mark.parametrize(
    ("obj", "expected"),
    [
        ("not", False),
        ([1, 2], False),
        (1, True),
        (1.2, True),
        (np.int64(12), True),
    ],
)
def test_is_numeric(obj: Any, expected: bool) -> None:
    assert _is_numeric(obj) is expected


@pytest.mark.parametrize(
    ("obj", "expected"),
    [
        ("not", False),
        ([1, 2], False),
        (["a", "b"], True),
        (("c", "d"), True),
        ({"e"}, True),
    ],
)
def test_is_flat_str_collection(obj: Any, expected: bool) -> None:
    assert is_flat_str_collection(obj) is expected


@pytest.mark.parametrize(
    ("obj", "expected"),
    [
        ("not", False),
        ([1, 2], False),
        (
            [
                [
                    [(0, 0), (1, 1), (2, 2), (3, 3)],
                    [(0, 0), (1, 1), (2, 2)],
                    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
                ],
                [
                    [(-2, 2), (-1, 1), (0, 1)],
                    [(2, 2), (3, 1), (4, 1)],
                ],
            ],
            False,
        ),
        (
            [
                [(0, 0), (1, 1), (2, 2)],
                [(2, 2), (3, 1), (4, 1)],
            ],
            True,
        ),
    ],
)
def test_is_is_shallow_densities(obj: Any, expected: bool) -> None:
    assert is_shallow_densities(obj) is expected


@pytest.mark.parametrize(
    ("obj", "expected"),
    [
        ("not", False),
        ([1, 2], False),
        (
            [
                [
                    [0, 0, 1, 1, 2, 2, 3, 3],
                    [0, 0, 1, 1, 2, 2],
                    [0, 0, 1, 1, 2, 2, 3, 3, 4, 4],
                ],
                [
                    [-2, 2, -1, 1, 0, 1],
                    [2, 2, 3, 1, 4, 1],
                ],
            ],
            False,
        ),
        (
            [
                [0, 0, 1, 1, 2, 2],
                [2, 2, 3, 1, 4, 1],
            ],
            True,
        ),
    ],
)
def test_is_shallow_samples(obj: Any, expected: bool) -> None:
    assert is_shallow_samples(obj) is expected
