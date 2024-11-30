from __future__ import annotations

from typing import Any, ClassVar

from plotly import graph_objects as go

from ridgeplot._color.interpolation import slice_colorscale
from ridgeplot._color.utils import apply_alpha
from ridgeplot._obj._base import DEFAULT_HOVERTEMPLATE, ColoringContext, RidgeplotTrace
from ridgeplot._utils import normalise_min_max


class AreaTrace(RidgeplotTrace):
    _DEFAULT_LINE_WIDTH: ClassVar[float] = 1.5

    def _get_coloring_kwargs(self, ctx: ColoringContext) -> dict[str, Any]:
        if ctx.colormode == "fillgradient":
            if ctx.opacity is not None:
                # HACK: Plotly doesn't yet support setting the fill opacity
                #       for traces with `fillgradient`. As a workaround, we
                #       can override the color-scale's color values and add
                #       the corresponding alpha channel to all colors.
                ctx.colorscale = [
                    (v, apply_alpha(c, float(ctx.opacity))) for v, c in ctx.colorscale
                ]
            color_kwargs = dict(
                line_color=self.line_color,
                fillgradient=go.scatter.Fillgradient(
                    colorscale=slice_colorscale(
                        colorscale=ctx.colorscale,
                        p_lower=normalise_min_max(
                            min(self.x),
                            min_=ctx.interpolation_ctx.x_min,
                            max_=ctx.interpolation_ctx.x_max,
                        ),
                        p_upper=normalise_min_max(
                            max(self.x),
                            min_=ctx.interpolation_ctx.x_min,
                            max_=ctx.interpolation_ctx.x_max,
                        ),
                    ),
                    type="horizontal",
                ),
            )
        else:
            color_kwargs = dict(
                line_color=self.line_color,
                fillcolor=self.solid_color,
            )
        return color_kwargs

    def draw(self, fig: go.Figure, coloring_ctx: ColoringContext) -> go.Figure:
        # Draw an invisible trace at constance y=y_shifted so that we
        # can set fill="tonexty" below and get a filled area plot.
        fig.add_trace(
            go.Scatter(
                x=self.x,
                y=[self.y_shifted] * len(self.x),
                # make trace 'invisible'
                # Note: visible=False does not work with fill="tonexty"
                line=dict(color="rgba(0,0,0,0)", width=0),
                # Hide this invisible helper trace from the legend and hoverinfo
                showlegend=False,
                hoverinfo="skip",
                # z-order (higher z-order means the trace is drawn on top)
                zorder=self.zorder,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=self.x,
                y=[y_i + self.y_shifted for y_i in self.y],
                name=self.label,
                fill="tonexty",
                mode="lines",
                line=dict(width=self.line_width if self.line_width is not None else 1.5),
                **self._get_coloring_kwargs(ctx=coloring_ctx),
                # Hover information
                customdata=[[y_i] for y_i in self.y],
                hovertemplate=DEFAULT_HOVERTEMPLATE,
                # z-order (higher z-order means the trace is drawn on top)
                zorder=self.zorder,
            ),
        )
        return fig