from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Protocol, cast

from plotly import express as px

from ridgeplot._color.colorscale import (
    validate_and_coerce_colorscale,
)
from ridgeplot._color.utils import apply_alpha, round_color, to_rgb
from ridgeplot._types import CollectionL2, Color, ColorScale
from ridgeplot._utils import get_xy_extrema, normalise_min_max

if TYPE_CHECKING:
    from collections.abc import Collection

    from ridgeplot._types import Densities, Numeric

Colormode = Literal["row-index", "trace-index", "trace-index-row-wise", "mean-minmax", "mean-means"]
"""The :paramref:`ridgeplot.ridgeplot.colormode` argument in
:func:`ridgeplot.ridgeplot()`."""

ColorscaleInterpolants = CollectionL2[float]
"""A :data:`ColorscaleInterpolants` contains the interpolants for a :data:`ColorScale`.

Example
-------

>>> interpolants: ColorscaleInterpolants = [
...     [0.2, 0.5, 1],
...     [0.3, 0.7],
... ]
"""


@dataclass
class InterpolationContext:
    densities: Densities
    n_rows: int
    n_traces: int
    x_min: Numeric
    x_max: Numeric

    @classmethod
    def from_densities(cls, densities: Densities) -> InterpolationContext:
        x_min, x_max, _, _ = map(float, get_xy_extrema(densities=densities))
        return cls(
            densities=densities,
            n_rows=len(densities),
            n_traces=sum(len(row) for row in densities),
            x_min=x_min,
            x_max=x_max,
        )


class InterpolationFunc(Protocol):
    def __call__(self, ctx: InterpolationContext) -> ColorscaleInterpolants: ...


def _mul(a: tuple[Numeric, ...], b: tuple[Numeric, ...]) -> tuple[Numeric, ...]:
    """Multiply two tuples element-wise."""
    return tuple(a_i * b_i for a_i, b_i in zip(a, b))


def _interpolate_row_index(ctx: InterpolationContext) -> ColorscaleInterpolants:
    return [
        [((ctx.n_rows - 1) - ith_row) / (ctx.n_rows - 1)] * len(row)
        for ith_row, row in enumerate(ctx.densities)
    ]


def _interpolate_trace_index(ctx: InterpolationContext) -> ColorscaleInterpolants:
    ps = []
    ith_trace = 0
    for row in ctx.densities:
        ps_row = []
        for _ in row:
            ps_row.append(((ctx.n_traces - 1) - ith_trace) / (ctx.n_traces - 1))
            ith_trace += 1
        ps.append(ps_row)
    return ps


def _interpolate_trace_index_row_wise(ctx: InterpolationContext) -> ColorscaleInterpolants:
    return [
        [((len(row) - 1) - ith_row_trace) / (len(row) - 1) for ith_row_trace in range(len(row))]
        for row in ctx.densities
    ]


def _interpolate_mean_minmax(ctx: InterpolationContext) -> ColorscaleInterpolants:
    ps = []
    for row in ctx.densities:
        ps_row = []
        for trace in row:
            x, y = zip(*trace)
            ps_row.append(
                normalise_min_max(sum(_mul(x, y)) / sum(y), min_=ctx.x_min, max_=ctx.x_max)
            )
        ps.append(ps_row)
    return ps


def _interpolate_mean_means(ctx: InterpolationContext) -> ColorscaleInterpolants:
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


def interpolate_color(colorscale: ColorScale, p: float) -> Color:
    """Get a color from a colorscale at a given interpolation point ``p``."""
    if not (0 <= p <= 1):
        raise ValueError(
            f"The interpolation point 'p' should be a float value between 0 and 1, not {p}."
        )
    scale = [s for s, _ in colorscale]
    colors = [c for _, c in colorscale]
    del colorscale
    if p in scale:
        return colors[scale.index(p)]
    colors = [to_rgb(c) for c in colors]
    ceil = min(filter(lambda s: s > p, scale))
    floor = max(filter(lambda s: s < p, scale))
    p_normalised = normalise_min_max(p, min_=floor, max_=ceil)
    return cast(
        str,
        px.colors.find_intermediate_color(
            lowcolor=colors[scale.index(floor)],
            highcolor=colors[scale.index(ceil)],
            intermed=p_normalised,
            colortype="rgb",
        ),
    )


def compute_trace_colors(
    colorscale: ColorScale | Collection[Color] | str | None,
    colormode: Colormode,
    coloralpha: float | None,
    interpolation_ctx: InterpolationContext,
) -> list[list[str]]:
    colorscale = validate_and_coerce_colorscale(colorscale)
    if coloralpha is not None:
        coloralpha = float(coloralpha)

    def _get_color(p: float) -> str:
        color = interpolate_color(colorscale, p=p)
        if coloralpha is not None:
            color = apply_alpha(color, alpha=coloralpha)
        # This helps us avoid floating point errors when making
        # comparisons in our test suite. The user should not
        # be able to notice *any* difference in the output
        color = round_color(color, ndigits=12)
        return color

    if colormode not in COLORMODE_MAPS:
        raise ValueError(
            f"The colormode argument should be one of "
            f"{tuple(COLORMODE_MAPS)}, got {colormode} instead."
        )

    interpolate_func = COLORMODE_MAPS[colormode]
    interpolants = interpolate_func(ctx=interpolation_ctx)
    return [[_get_color(p) for p in row] for row in interpolants]


COLORMODE_MAPS: dict[Colormode, InterpolationFunc] = {
    "row-index": _interpolate_row_index,
    "trace-index": _interpolate_trace_index,
    "trace-index-row-wise": _interpolate_trace_index_row_wise,
    "mean-minmax": _interpolate_mean_minmax,
    "mean-means": _interpolate_mean_means,
}
