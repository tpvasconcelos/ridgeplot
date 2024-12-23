"""Color interpolation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from typing_extensions import Literal, Protocol

from ridgeplot._color.utils import apply_alpha, round_color, to_rgb, unpack_rgb
from ridgeplot._types import CollectionL2, ColorScale
from ridgeplot._utils import get_xy_extrema, normalise_min_max
from ridgeplot._vendor.more_itertools import zip_strict

if TYPE_CHECKING:
    from collections.abc import Generator

    from ridgeplot._types import Densities, Numeric


# ==============================================================
# --- Interpolation utilities
# ==============================================================


def interpolate_color(colorscale: ColorScale, p: float) -> str:
    """Get a color from a colorscale at a given interpolation point ``p``.

    This function always returns a color in the RGB format, even if the input
    colorscale contains colors in other formats.
    """
    if not (0 <= p <= 1):
        raise ValueError(
            f"The interpolation point 'p' should be a float value between 0 and 1, not {p}."
        )
    scale = [s for s, _ in colorscale]
    colors = [to_rgb(c) for _, c in colorscale]
    if p in scale:
        return colors[scale.index(p)]
    ceil = min(filter(lambda s: s > p, scale))
    floor = max(filter(lambda s: s < p, scale))
    color_floor = unpack_rgb(colors[scale.index(floor)])
    color_ceil = unpack_rgb(colors[scale.index(ceil)])
    p_norm = normalise_min_max(p, min_=floor, max_=ceil)
    rgb = to_rgb(
        (
            color_floor[0] + (p_norm * (color_ceil[0] - color_floor[0])),
            color_floor[1] + (p_norm * (color_ceil[1] - color_floor[1])),
            color_floor[2] + (p_norm * (color_ceil[2] - color_floor[2])),
        )
    )
    alpha_floor = color_floor[3] if len(color_floor) == 4 else 1
    alpha_ceil = color_ceil[3] if len(color_ceil) == 4 else 1
    alpha = alpha_floor + (p_norm * (alpha_ceil - alpha_floor))
    if alpha < 1:
        rgb = apply_alpha(rgb, alpha)
    # To address floating point errors, we round all color channels to a
    # reasonable precision, which should result in the exact some result
    # being rendered by any browsers and most Plotly output formats.
    return round_color(rgb, 5)


def slice_colorscale(
    colorscale: ColorScale,
    p_lower: float,
    p_upper: float,
) -> ColorScale:
    """Slice a continuous colorscale between two intermediate points.

    Parameters
    ----------
    colorscale
        The continuous colorscale to slice.
    p_lower
        The lower bound of the slicing interval. Must be >= 0 and < p_upper.
    p_upper
        The upper bound of the slicing interval. Must be <= 1 and > p_lower.

    Returns
    -------
    ColorScale
        The sliced colorscale.

    Raises
    ------
    ValueError
        If ``p_lower`` is >= ``p_upper``, or if either ``p_lower`` or ``p_upper``
        are outside the range [0, 1].
    """
    if p_lower >= p_upper:
        raise ValueError("p_lower should be less than p_upper.")
    if p_lower < 0 or p_upper > 1:
        raise ValueError("p_lower should be >= 0 and p_upper should be <= 1.")
    if p_lower == 0 and p_upper == 1:
        return colorscale

    return (
        (0.0, interpolate_color(colorscale, p=p_lower)),
        *[
            (normalise_min_max(v, min_=p_lower, max_=p_upper), c)
            for v, c in colorscale
            if p_lower < v < p_upper
        ],
        (1.0, interpolate_color(colorscale, p=p_upper)),
    )


# ==============================================================
# --- Solid color modes
# ==============================================================


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
    """Context information needed by the interpolation functions."""

    densities: Densities
    n_rows: int
    n_traces: int
    x_min: Numeric
    x_max: Numeric

    @classmethod
    def from_densities(cls, densities: Densities) -> InterpolationContext:
        x_min, x_max, _, _ = get_xy_extrema(densities=densities)
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
    return tuple(a_i * b_i for a_i, b_i in zip_strict(a, b))


def _interpolate_row_index(ctx: InterpolationContext) -> ColorscaleInterpolants:
    if ctx.n_rows == 1:
        return [[0.0] * ctx.n_traces]
    return [
        [((ctx.n_rows - 1) - ith_row) / (ctx.n_rows - 1)] * len(row)
        for ith_row, row in enumerate(ctx.densities)
    ]


def _interpolate_trace_index(ctx: InterpolationContext) -> ColorscaleInterpolants:
    if ctx.n_traces == 1:
        return [[0.0]]
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
        [
            ((len(row) - 1) - ith_row_trace) / (len(row) - 1) if len(row) > 1 else 0.0
            for ith_row_trace in range(len(row))
        ]
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
    min_mean = min(min(row) for row in means)
    max_mean = max(max(row) for row in means)
    return [
        [normalise_min_max(mean, min_=min_mean, max_=max_mean) for mean in row] for row in means
    ]


SolidColormode = Literal[
    "row-index",
    "trace-index",
    "trace-index-row-wise",
    "mean-minmax",
    "mean-means",
]
"""See :paramref:`ridgeplot.ridgeplot.colormode` for more information."""

SOLID_COLORMODE_MAPS: dict[SolidColormode, InterpolationFunc] = {
    "row-index": _interpolate_row_index,
    "trace-index": _interpolate_trace_index,
    "trace-index-row-wise": _interpolate_trace_index_row_wise,
    "mean-minmax": _interpolate_mean_minmax,
    "mean-means": _interpolate_mean_means,
}


def compute_solid_colors(
    colorscale: ColorScale,
    colormode: SolidColormode,
    opacity: float | None,
    interpolation_ctx: InterpolationContext,
) -> Generator[Generator[str]]:
    """Compute the solid colors for all traces in the plot."""

    def get_fill_color(p: float) -> str:
        fill_color = interpolate_color(colorscale, p=p)
        if opacity is not None:
            # Sometimes the interpolation logic can drop the alpha channel
            fill_color = apply_alpha(fill_color, alpha=float(opacity))
        return fill_color

    interpolate_func = SOLID_COLORMODE_MAPS[colormode]
    interpolants = interpolate_func(ctx=interpolation_ctx)
    return ((get_fill_color(p) for p in row) for row in interpolants)
