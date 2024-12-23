# This module contains a reference implementation to a work-in-progress
# proposal for a generic type guard function in Python. The proposal is
# inspired by the functools' `singledispatch` decorator and aims to provide
# a similar way to register type guard functions for specific types and
# generic types. The goal is to be able to use a generic `typeis(obj, tp)`
# function that checks if the given object is of the given (generic) type.
# New type guard functions can be registered for specific types using the
# `register_typeis` decorator (TBD: or a `typeis.register` method). e.g.:
#
#     @register_typeis(list[int])
#     def is_list_of_ints(obj: Any) -> TypeIs[list[int]]:
#         return isinstance(obj, list) and all(isinstance(x, int) for x in obj)
#
#     print(typeis([1, 2, 3], list[int]))  # -> True
#     print(typeis([1, 2, "3"], list[int]))  # -> False
#     print(typeis([1, 2, 3], list[str]))  # -> TypeError (unsupported type)
#
from __future__ import annotations

from types import GenericAlias
from typing import TYPE_CHECKING

from typing_extensions import Any, Protocol, TypeIs, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

_T = TypeVar("_T", bound=type)


class TypeGuardFunc(Protocol[_T]):
    def __call__(self, obj: Any) -> TypeIs[_T]: ...


_typeguard_registry = {}


def typeis(obj: Any, tp: _T) -> TypeIs[_T]:
    """Type guard function that checks if the given object is of the given type.

    Args:
        obj:
            The object to check.
        tp:
            The type to check against.

    Returns
    -------
    bool
        Whether the object is of the given type.
    """
    if tp in _typeguard_registry:
        return _typeguard_registry[tp](obj)
    if isinstance(tp, type) and not isinstance(tp, GenericAlias):  # pyright: ignore[reportUnnecessaryIsInstance]
        return isinstance(obj, tp)
    raise TypeError(
        f"Unsupported type: {tp}\n"
        f"Consider registering a type guard function for this type, e.g.:\n"
        f"\n"
        f"@register_typeis({tp})\n"
        f"def _is_{tp.__name__.lower()}(obj: Any) -> TypeIs[{tp}]:\n"
        f"    # Implement the type guard function here...\n"
    )


def register_typeis(tp: _T) -> Callable[[TypeGuardFunc[_T]], TypeGuardFunc[_T]]:
    """Register a type guard function for a given type.

    Args:
        tp:
            The type to register the type guard function for.

    Returns
    -------
    Callable[[TypeGuardFunc[_T]], TypeGuardFunc[_T]]
        A decorator that registers the given type guard function for the given
        type.
    """

    def decorator(func: TypeGuardFunc[_T]) -> TypeGuardFunc[_T]:
        _typeguard_registry[tp] = func
        return func

    return decorator
