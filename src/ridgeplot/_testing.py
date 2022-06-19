"""Testing utils"""
from typing import TypeVar

X = TypeVar("X")


def id_func(x: X) -> X:
    """Identity function."""
    return x
