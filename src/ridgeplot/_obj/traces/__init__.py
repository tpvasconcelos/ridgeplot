from __future__ import annotations

from typing import TYPE_CHECKING

from ridgeplot._obj.traces.area import AreaTrace
from ridgeplot._obj.traces.bar import BarTrace

if TYPE_CHECKING:
    from ridgeplot._obj.traces.base import RidgeplotTrace
    from ridgeplot._types import TraceType


TRACE_TYPES: dict[TraceType, type[RidgeplotTrace]] = {
    "area": AreaTrace,
    "bar": BarTrace,
}
"""Mapping of trace types to trace classes."""


def get_trace_cls(trace_type: TraceType) -> type[RidgeplotTrace]:
    """Get a trace class by its type."""
    try:
        return TRACE_TYPES[trace_type]
    except KeyError as err:
        types = ", ".join(repr(t) for t in TRACE_TYPES)
        raise ValueError(f"Unknown trace type {trace_type!r}. Available types: {types}.") from err
