from __future__ import annotations

import pytest

from ridgeplot._color.interpolation import InterpolationContext
from ridgeplot._obj.traces.bar import BarTrace
from ridgeplot._obj.traces.base import ColoringContext


@pytest.fixture
def bar_trace() -> BarTrace:
    return BarTrace(
        trace=[(0, 0), (1, 1), (2, 0)],
        label="Trace 1",
        solid_color="red",
        zorder=1,
        y_base=0,
        line_color="black",
        line_width=0.5,
    )


@pytest.fixture
def interpolation_ctx() -> InterpolationContext:
    return InterpolationContext(
        densities=[
            [[(0, 0), (1, 1), (2, 0)]],
            [[(1, 0), (2, 1), (3, 0)]],
        ],
        n_rows=2,
        n_traces=2,
        x_min=0,
        x_max=3,
    )


class TestBarTrace:
    def test_coloring_kwargs_fillgradient(
        self, bar_trace: BarTrace, interpolation_ctx: InterpolationContext
    ) -> None:
        coloring_ctx = ColoringContext(
            colorscale=[(0.0, "red"), (1.0, "blue")],
            fillgradient=True,
            opacity=None,
            interpolation_ctx=interpolation_ctx,
        )
        color_kwargs = bar_trace._get_coloring_kwargs(ctx=coloring_ctx)  # pyright: ignore[reportPrivateUsage]
        assert color_kwargs == {
            "marker_line_color": "black",
            "marker_color": ["rgb(255, 0, 0)", "rgb(170.0, 0.0, 85.0)", "rgb(85.0, 0.0, 170.0)"],
        }

    def test_coloring_kwargs_fillcolor(
        self, bar_trace: BarTrace, interpolation_ctx: InterpolationContext
    ) -> None:
        coloring_ctx = ColoringContext(
            colorscale=[(0.0, "red"), (1.0, "blue")],
            fillgradient=False,
            opacity=None,
            interpolation_ctx=interpolation_ctx,
        )
        color_kwargs = bar_trace._get_coloring_kwargs(ctx=coloring_ctx)  # pyright: ignore[reportPrivateUsage]
        assert color_kwargs == {
            "marker_line_color": "black",
            "marker_color": "red",
        }
