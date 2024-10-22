from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from plotly import graph_objects as go

from ridgeplot._color.interpolation import (
    Colormode,
    InterpolationContext,
    compute_trace_colors,
)
from ridgeplot._types import (
    CollectionL1,
    CollectionL2,
    Color,
    ColorScale,
    DensityTrace,
    is_flat_str_collection,
    nest_shallow_collection,
)
from ridgeplot._utils import (
    get_collection_array_shape,
    get_xy_extrema,
    normalise_row_attrs,
    ordered_dedup,
)
from ridgeplot._vendor.more_itertools import zip_strict

if TYPE_CHECKING:
    from collections.abc import Collection

    from ridgeplot._types import Densities, Numeric


LabelsArray = CollectionL2[str]
"""A :data:`LabelsArray` represents the labels of traces in a ridgeplot.

Example
-------

>>> labels_array: LabelsArray = [
...     ["trace 1", "trace 2", "trace 3"],
...     ["trace 4", "trace 5"],
... ]
"""

ShallowLabelsArray = CollectionL1[str]
"""Shallow type for :data:`LabelsArray`.

Example
-------

>>> labels_array: ShallowLabelsArray = ["trace 1", "trace 2", "trace 3"]
"""

_D3HF = ".7"
"""Default (d3-format) format for floats in hover labels.

After trying to read through the plotly.py source code, I couldn't find a
simple way to replicate the default hover format using the d3-format syntax
in Plotly's 'hovertemplate' parameter. The closest I got was by using the
string below, but it's not quite the same... (see '.7~r' as well)
"""

_DEFAULT_HOVERTEMPLATE = (
    f"(%{{x:{_D3HF}}}, %{{customdata[0]:{_D3HF}}})"
    "<br>"
    "<extra>%{fullData.name}</extra>"
)  # fmt: skip
"""Default ``hovertemplate`` for density traces.

See :func:`draw_density_trace`.
"""


def normalise_trace_labels(
    densities: Densities,
    trace_labels: LabelsArray | ShallowLabelsArray | None,
    n_traces: int,
) -> LabelsArray:
    if trace_labels is None:
        ids = iter(range(1, n_traces + 1))
        trace_labels = [[f"Trace {next(ids)}" for _ in row] for row in densities]
    else:
        if is_flat_str_collection(trace_labels):
            trace_labels = cast(ShallowLabelsArray, trace_labels)
            trace_labels = cast(LabelsArray, nest_shallow_collection(trace_labels))
        trace_labels = normalise_row_attrs(trace_labels, densities=densities)
    return trace_labels


def normalise_y_labels(trace_labels: LabelsArray) -> LabelsArray:
    return [ordered_dedup(row) for row in trace_labels]


@dataclass
class RidgeplotTrace:
    trace: DensityTrace
    label: str
    color: str


@dataclass
class RidgeplotRow:
    traces: list[RidgeplotTrace]
    y_shifted: float


def draw_base(
    fig: go.Figure,
    x: Collection[Numeric],
    y_shifted: float,
) -> go.Figure:
    """Draw the base for a density trace.

    Adds an invisible trace at constant y that will serve as the fill-limit
    for the corresponding density trace.
    """
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[y_shifted] * len(x),
            # make trace 'invisible'
            # Note: visible=False does not work with fill="tonexty"
            line=dict(color="rgba(0,0,0,0)", width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    return fig


def draw_density_trace(
    fig: go.Figure,
    x: Collection[Numeric],
    y: Collection[Numeric],
    y_shifted: float,
    label: str,
    color: str,
    linewidth: float,
) -> go.Figure:
    """Draw a density trace.

    Adds a density 'trace' to the Figure. The ``fill="tonexty"`` option
    fills the trace until the previously drawn trace (see
    :meth:`draw_base`). This is why the base trace must be drawn first.
    """
    fig = draw_base(fig, x=x, y_shifted=y_shifted)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[y_i + y_shifted for y_i in y],
            fillcolor=color,
            name=label,
            fill="tonexty",
            mode="lines",
            line=dict(
                color="rgba(0,0,0,0.6)" if color is not None else None,
                width=linewidth,
            ),
            # Hover information
            customdata=[[y_i] for y_i in y],
            hovertemplate=_DEFAULT_HOVERTEMPLATE,
        ),
    )
    return fig


def update_layout(
    fig: go.Figure,
    y_labels: LabelsArray,
    tickvals: list[float],
    show_yticklabels: bool,
    xpad: float,
    x_max: float,
    x_min: float,
) -> go.Figure:
    """Update figure's layout."""
    fig.update_layout(
        legend=dict(traceorder="normal"),
    )
    axes_common = dict(
        zeroline=False,
        showgrid=True,
    )
    fig.update_yaxes(
        showticklabels=show_yticklabels,
        tickvals=tickvals,
        ticktext=y_labels,
        **axes_common,
    )
    x_padding = xpad * (x_max - x_min)
    fig.update_xaxes(
        range=[x_min - x_padding, x_max + x_padding],
        showticklabels=True,
        **axes_common,
    )
    return fig


def create_ridgeplot(
    densities: Densities,
    colorscale: ColorScale | Collection[Color] | str | None,
    coloralpha: float | None,
    colormode: Colormode,
    trace_labels: LabelsArray | ShallowLabelsArray | None,
    linewidth: float,
    spacing: float,
    show_yticklabels: bool,
    xpad: float,
) -> go.Figure:
    # ==============================================================
    # ---  Get clean and validated input arguments
    # ==============================================================
    shape = get_collection_array_shape(densities)
    if len(shape) != 4:
        raise ValueError(f"Expected a 4D array of densities, got a {len(shape)}D array instead.")

    n_rows = len(densities)
    n_traces = sum(len(row) for row in densities)
    x_min, x_max, _, y_max = map(float, get_xy_extrema(densities=densities))

    trace_labels = normalise_trace_labels(
        densities=densities,
        trace_labels=trace_labels,
        n_traces=n_traces,
    )
    y_labels = normalise_y_labels(trace_labels)

    # Force cast certain arguments to the expected types
    linewidth = float(linewidth)
    spacing = float(spacing)
    show_yticklabels = bool(show_yticklabels)
    xpad = float(xpad)

    # ==============================================================
    # ---  Build the figure
    # ==============================================================

    colors = compute_trace_colors(
        colorscale=colorscale,
        colormode=colormode,
        coloralpha=coloralpha,
        interpolation_ctx=InterpolationContext(
            densities=densities,
            n_rows=n_rows,
            n_traces=n_traces,
            x_min=x_min,
            x_max=x_max,
        ),
    )
    rows: list[RidgeplotRow] = [
        RidgeplotRow(
            traces=[
                RidgeplotTrace(trace=trace, label=label, color=color)
                for trace, label, color in zip_strict(traces, labels, colors)
            ],
            y_shifted=float(-ith_row * y_max * spacing),
        )
        for ith_row, (traces, labels, colors) in enumerate(
            zip_strict(densities, trace_labels, colors)
        )
    ]

    fig = go.Figure()
    for row in rows:
        for trace in row.traces:
            x, y = zip(*trace.trace)
            fig = draw_density_trace(
                fig,
                x=x,
                y=y,
                y_shifted=row.y_shifted,
                label=trace.label,
                color=trace.color,
                linewidth=linewidth,
            )
    fig = update_layout(
        fig,
        y_labels=y_labels,
        tickvals=[row.y_shifted for row in rows],
        show_yticklabels=show_yticklabels,
        xpad=xpad,
        x_max=x_max,
        x_min=x_min,
    )
    return fig
