from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Protocol

from ridgeplot._colors import ColorScale, apply_alpha, interpolate_color, normalise_colorscale
from ridgeplot._types import CollectionL2
from ridgeplot._utils import get_xy_extrema, normalise_min_max

if TYPE_CHECKING:
    from collections.abc import Collection

    from ridgeplot._colors import Color
    from ridgeplot._types import Densities, Numeric

Colormode = Literal["row-index", "trace-index", "trace-index-row-wise", "mean-minmax", "mean-means"]
"""The :paramref:`ridgeplot.ridgeplot.colormode` argument in
:func:`ridgeplot.ridgeplot()`."""

ColorsArray = CollectionL2[str]
"""A :data:`ColorsArray` represents the colors of traces in a ridgeplot.

Example
-------

>>> colors_array: ColorsArray = [
...     ["red", "blue", "green"],
...     ["orange", "purple"],
... ]
"""

MidpointsArray = CollectionL2[float]
"""A :data:`MidpointsArray` represents the midpoints of color scales in a
ridgeplot.

Example
-------

>>> midpoints_array: MidpointsArray = [
...     [0.2, 0.5, 1],
...     [0.3, 0.7],
... ]
"""


@dataclass
class MidpointsContext:
    densities: Densities
    n_rows: int
    n_traces: int
    x_min: Numeric
    x_max: Numeric

    @classmethod
    def from_densities(cls, densities: Densities) -> MidpointsContext:
        x_min, x_max, _, _ = map(float, get_xy_extrema(densities=densities))
        return cls(
            densities=densities,
            n_rows=len(densities),
            n_traces=sum(len(row) for row in densities),
            x_min=x_min,
            x_max=x_max,
        )


class MidpointsFunc(Protocol):
    def __call__(self, ctx: MidpointsContext) -> MidpointsArray: ...


def _mul(a: tuple[Numeric, ...], b: tuple[Numeric, ...]) -> tuple[Numeric, ...]:
    """Multiply two tuples element-wise."""
    return tuple(a_i * b_i for a_i, b_i in zip(a, b))


def _compute_midpoints_row_index(ctx: MidpointsContext) -> MidpointsArray:
    return [
        [((ctx.n_rows - 1) - ith_row) / (ctx.n_rows - 1)] * len(row)
        for ith_row, row in enumerate(ctx.densities)
    ]


def _compute_midpoints_trace_index(ctx: MidpointsContext) -> MidpointsArray:
    midpoints = []
    ith_trace = 0
    for row in ctx.densities:
        midpoints_row = []
        for _ in row:
            midpoints_row.append(((ctx.n_traces - 1) - ith_trace) / (ctx.n_traces - 1))
            ith_trace += 1
        midpoints.append(midpoints_row)
    return midpoints


def _compute_midpoints_trace_index_row_wise(ctx: MidpointsContext) -> MidpointsArray:
    return [
        [((len(row) - 1) - ith_row_trace) / (len(row) - 1) for ith_row_trace in range(len(row))]
        for row in ctx.densities
    ]


def _compute_midpoints_mean_minmax(ctx: MidpointsContext) -> MidpointsArray:
    midpoints = []
    for row in ctx.densities:
        midpoints_row = []
        for trace in row:
            x, y = zip(*trace)
            midpoints_row.append(
                normalise_min_max(sum(_mul(x, y)) / sum(y), min_=ctx.x_min, max_=ctx.x_max)
            )
        midpoints.append(midpoints_row)
    return midpoints


def _compute_midpoints_mean_means(ctx: MidpointsContext) -> MidpointsArray:
    means = []
    for row in ctx.densities:
        means_row = []
        for trace in row:
            x, y = zip(*trace)
            means_row.append(sum(_mul(x, y)) / sum(y))
        means.append(means_row)
    min_mean = min([min(row) for row in means])
    max_mean = max([max(row) for row in means])
    return [
        [normalise_min_max(mean, min_=min_mean, max_=max_mean) for mean in row] for row in means
    ]


def compute_trace_colors(
    colorscale: ColorScale | Collection[Color] | str,
    colormode: Colormode,
    coloralpha: float | None,
    midpoints_context: MidpointsContext,
) -> ColorsArray:
    colorscale = normalise_colorscale(colorscale)
    if coloralpha is not None:
        coloralpha = float(coloralpha)

    def _get_color(mp: float) -> str:
        color = interpolate_color(colorscale, midpoint=mp)
        if coloralpha is not None:
            color = apply_alpha(color, alpha=coloralpha)
        return color

    if colormode not in COLORMODE_MAPS:
        raise ValueError(
            f"The colormode argument should be one of "
            f"{tuple(COLORMODE_MAPS)}, got {colormode} instead."
        )

    midpoints_func = COLORMODE_MAPS[colormode]
    midpoints = midpoints_func(ctx=midpoints_context)
    return [[_get_color(midpoint) for midpoint in row] for row in midpoints]


COLORMODE_MAPS: dict[Colormode, MidpointsFunc] = {
    "row-index": _compute_midpoints_row_index,
    "trace-index": _compute_midpoints_trace_index,
    "trace-index-row-wise": _compute_midpoints_trace_index_row_wise,
    "mean-minmax": _compute_midpoints_mean_minmax,
    "mean-means": _compute_midpoints_mean_means,
}
