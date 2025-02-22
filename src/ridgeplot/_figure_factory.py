"""Ridgeline plot figure factory logic."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from plotly import graph_objects as go
from typing_extensions import Literal

from ridgeplot._color.colorscale import validate_coerce_colorscale
from ridgeplot._color.interpolation import (
    InterpolationContext,
    SolidColormode,
    compute_solid_colors,
)
from ridgeplot._obj.traces import get_trace_cls
from ridgeplot._obj.traces.base import ColoringContext
from ridgeplot._types import (
    Color,
    ColorScale,
    LabelsArray,
    ShallowLabelsArray,
    ShallowTraceTypesArray,
    TraceType,
    TraceTypesArray,
    is_flat_str_collection,
    is_shallow_trace_types_array,
    is_trace_type,
    is_trace_types_array,
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

    from ridgeplot._types import Densities


def normalise_trace_types(
    densities: Densities,
    trace_types: TraceTypesArray | ShallowTraceTypesArray | TraceType,
) -> TraceTypesArray:
    if is_trace_type(trace_types):
        trace_types = cast("TraceTypesArray", [[trace_types] * len(row) for row in densities])
    elif is_shallow_trace_types_array(trace_types):
        trace_types = nest_shallow_collection(trace_types)
        trace_types = normalise_row_attrs(trace_types, l2_target=densities)
    elif is_trace_types_array(trace_types):
        trace_types = normalise_row_attrs(trace_types, l2_target=densities)
    else:
        raise TypeError(f"Invalid trace_type: {trace_types}")
    return trace_types


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
            trace_labels = nest_shallow_collection(trace_labels)
        trace_labels = normalise_row_attrs(trace_labels, l2_target=densities)
    return trace_labels


def normalise_row_labels(trace_labels: LabelsArray) -> Collection[str]:
    return [",".join(ordered_dedup(row)) for row in trace_labels]


def _update_layout(
    fig: go.Figure,
    row_labels: Collection[str] | Literal[False],
    tickvals: list[float],
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
        showticklabels=row_labels is not False,
        **axes_common,
    )
    if row_labels is not False:
        fig.update_yaxes(
            # tickmode="array",  # TODO: check if this is needed
            tickvals=tickvals,
            ticktext=row_labels,
        )
    x_padding = xpad * (x_max - x_min)
    fig.update_xaxes(
        range=[x_min - x_padding, x_max + x_padding],
        showticklabels=True,
        **axes_common,
    )
    # Settings for bar/histogram traces:
    fig.update_layout(
        # barmode can be either 'stack' or 'relative'
        barmode="stack",
        # bargap and bargroupgap should be set
        # to 0 to avoid gaps between bars
        bargap=0,
        bargroupgap=0,
    )
    return fig


def create_ridgeplot(
    densities: Densities,
    trace_labels: LabelsArray | ShallowLabelsArray | None,
    trace_types: TraceTypesArray | ShallowTraceTypesArray | TraceType,
    row_labels: Collection[str] | None | Literal[False],
    colorscale: ColorScale | Collection[Color] | str | None,
    colormode: Literal["fillgradient"] | SolidColormode,
    color_discrete_map: dict[str, str] | None,
    opacity: float | None,
    line_color: Color | Literal["fill-color"],
    line_width: float | None,
    spacing: float,
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

    trace_types = normalise_trace_types(
        densities=densities,
        trace_types=trace_types,
    )
    trace_labels = normalise_trace_labels(
        densities=densities,
        trace_labels=trace_labels,
        n_traces=n_traces,
    )
    if row_labels is None:
        row_labels = normalise_row_labels(trace_labels)
    elif row_labels is not False and len(row_labels) != n_rows:
        raise ValueError(f"Expected {n_rows} row_labels, got {len(row_labels)} instead.")

    # Force cast certain arguments to the expected types
    line_width = float(line_width) if line_width is not None else None
    spacing = float(spacing)
    xpad = float(xpad)
    colorscale = validate_coerce_colorscale(colorscale)

    # ==============================================================
    # ---  Build the figure
    # ==============================================================

    interpolation_ctx = InterpolationContext(
        densities=densities,
        n_rows=n_rows,
        n_traces=n_traces,
        x_min=x_min,
        x_max=x_max,
    )
    if color_discrete_map:
        solid_colors = (
            (color_discrete_map[label] for label in row_labels) for row_labels in trace_labels
        )
    else:
        solid_colors = compute_solid_colors(
            colorscale=colorscale,
            colormode=colormode if colormode != "fillgradient" else "mean-minmax",
            opacity=opacity,
            interpolation_ctx=interpolation_ctx,
        )

    tickvals: list[float] = []
    fig = go.Figure()
    ith_trace = 0
    for ith_row, (row_traces, row_trace_types, row_trace_labels, row_colors) in enumerate(
        zip_strict(densities, trace_types, trace_labels, solid_colors)
    ):
        y_base = float(-ith_row * y_max * spacing)
        tickvals.append(y_base)
        for trace, trace_type, label, color in zip_strict(
            row_traces, row_trace_types, row_trace_labels, row_colors
        ):
            trace_drawer = get_trace_cls(trace_type)(
                trace=trace,
                label=label,
                solid_color=color,
                zorder=ith_trace,
                y_base=y_base,
                line_color=line_color,
                line_width=line_width,
            )
            fig = trace_drawer.draw(
                fig=fig,
                coloring_ctx=ColoringContext(
                    colorscale=colorscale,
                    colormode=colormode,
                    opacity=opacity,
                    interpolation_ctx=interpolation_ctx,
                ),
            )
            ith_trace += 1

    fig = _update_layout(
        fig,
        row_labels=row_labels,
        tickvals=tickvals,
        xpad=xpad,
        x_max=x_max,
        x_min=x_min,
    )
    return fig
