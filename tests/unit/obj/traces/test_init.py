from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ridgeplot._obj.traces import AreaTrace, BarTrace, RidgeplotTrace, get_trace_cls

if TYPE_CHECKING:
    from ridgeplot._types import TraceType


@pytest.mark.parametrize(
    ("name", "cls"),
    [
        ("area", AreaTrace),
        ("bar", BarTrace),
    ],
)
def test_get_trace_cls(name: TraceType, cls: type[RidgeplotTrace]) -> None:
    assert get_trace_cls(name) is cls


def test_get_trace_cls_unknown() -> None:
    with pytest.raises(
        ValueError, match="Unknown trace type 'foo'. Available types: 'area', 'bar'."
    ):
        get_trace_cls("foo")  # pyright: ignore[reportArgumentType]
