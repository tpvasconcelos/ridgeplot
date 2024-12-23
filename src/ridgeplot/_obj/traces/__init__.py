"""Object-oriented trace interfaces."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ridgeplot._obj.traces.area import AreaTrace
from ridgeplot._obj.traces.bar import BarTrace
from ridgeplot._obj.traces.base import RidgeplotTrace

if TYPE_CHECKING:
    from ridgeplot._types import TraceType

__all__ = [
    "AreaTrace",
    "BarTrace",
    "RidgeplotTrace",
    "get_trace_cls",
]

_TRACE_TYPES: dict[TraceType, type[RidgeplotTrace]] = {
    "area": AreaTrace,
    "bar": BarTrace,
}
"""Mapping of trace types to trace classes."""


def get_trace_cls(trace_type: TraceType) -> type[RidgeplotTrace]:
    """Get a trace class by its type."""
    try:
        return _TRACE_TYPES[trace_type]
    except KeyError as err:
        types = ", ".join(repr(t) for t in _TRACE_TYPES)
        raise ValueError(f"Unknown trace type {trace_type!r}. Available types: {types}.") from err
