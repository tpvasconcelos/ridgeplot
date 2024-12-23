"""Bar trace object."""

from __future__ import annotations

from typing import ClassVar

from plotly import graph_objects as go
from typing_extensions import Any, override

from ridgeplot._color.interpolation import interpolate_color
from ridgeplot._obj.traces.base import DEFAULT_HOVERTEMPLATE, ColoringContext, RidgeplotTrace
from ridgeplot._utils import normalise_min_max


class BarTrace(RidgeplotTrace):
    _DEFAULT_LINE_WIDTH: ClassVar[float] = 0.5

    def _get_coloring_kwargs(self, ctx: ColoringContext) -> dict[str, Any]:
        if ctx.colormode == "fillgradient":
            color_kwargs = dict(
                marker_line_color=self.line_color,
                marker_color=[
                    interpolate_color(
                        colorscale=ctx.colorscale,
                        p=normalise_min_max(
                            x_i, min_=ctx.interpolation_ctx.x_min, max_=ctx.interpolation_ctx.x_max
                        ),
                    )
                    for x_i in self.x
                ],
            )
        else:
            color_kwargs = dict(
                marker_line_color=self.line_color,
                marker_color=self.solid_color,
            )
        return color_kwargs

    @override
    def draw(self, fig: go.Figure, coloring_ctx: ColoringContext) -> go.Figure:
        fig.add_trace(
            go.Bar(
                x=self.x,
                y=self.y,
                name=self.label,
                base=self.y_base,
                marker_line_width=self.line_width,
                width=None,  # Plotly automatically picks the right width
                **self._get_coloring_kwargs(ctx=coloring_ctx),
                # Hover information
                customdata=[[y_i] for y_i in self.y],
                hovertemplate=DEFAULT_HOVERTEMPLATE,
                # z-order (higher z-order means the trace is drawn on top)
                zorder=self.zorder,
            ),
        )
        return fig
