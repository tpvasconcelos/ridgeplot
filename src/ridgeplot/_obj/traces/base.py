"""Base trace object and utilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from typing_extensions import Literal

if TYPE_CHECKING:
    from plotly import graph_objects as go

    from ridgeplot._color.interpolation import InterpolationContext
    from ridgeplot._types import Color, ColorScale, DensityTrace


_D3HF = ".7"
"""Default (d3-format) format for floats in hover labels.

After trying to read through the plotly.py source code, I couldn't find a
simple way to replicate the default hover format using the d3-format syntax
in Plotly's 'hovertemplate' parameter. The closest I got was by using the
string below, but it's not quite the same... (see '.7~r' as well)
"""

DEFAULT_HOVERTEMPLATE = (
    f"(%{{x:{_D3HF}}}, %{{customdata[0]:{_D3HF}}})"
    "<br>"
    "<extra>%{fullData.name}</extra>"
)  # fmt: skip
"""Default ``hovertemplate`` for density traces.

The default hover template that should be used for all density traces. It
displays the x and y values of the hovered point, as well as the trace's name.
When using this as ``hovertemplate=DEFAULT_HOVERTEMPLATE``, it is expected that
the trace's ``customdata`` is set to a list of lists, where each inner list
contains a single element that is the y-value of the corresponding x-value
(e.g. ``customdata=[[y_i] for y_i in y]``). The ``name`` attribute of the trace
should also be set to the desired label for the trace (e.g. ``name=self.label``).
"""


@dataclass
class ColoringContext:
    colorscale: ColorScale
    fillgradient: bool
    opacity: float | None
    interpolation_ctx: InterpolationContext


class RidgeplotTrace(ABC):
    _DEFAULT_LINE_WIDTH: ClassVar[float] = 2.0

    def __init__(
        self,
        *,  # kw only
        trace: DensityTrace,
        label: str,
        solid_color: str,
        zorder: int,
        # Constant over the trace's row
        y_base: float,
        # Constant over the entire plot
        line_color: Color | Literal["fill-color"],
        line_width: float | None,
    ):
        super().__init__()
        self.x, self.y = zip(*trace, strict=True)
        self.label = label
        self.solid_color = solid_color
        self.zorder = zorder
        self.y_base = y_base
        self.line_color: Color = self.solid_color if line_color == "fill-color" else line_color
        self.line_width: float = line_width if line_width is not None else self._DEFAULT_LINE_WIDTH

    @abstractmethod
    def draw(self, fig: go.Figure, coloring_ctx: ColoringContext) -> go.Figure:
        raise NotImplementedError
