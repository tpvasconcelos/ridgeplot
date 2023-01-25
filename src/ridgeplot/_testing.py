"""Testing utils"""
from __future__ import annotations

from typing import TypeVar

X = TypeVar("X")


def id_func(x: X) -> X:
    """Identity function."""
    return x
