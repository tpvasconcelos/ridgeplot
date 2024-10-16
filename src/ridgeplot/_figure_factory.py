from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, cast

from plotly import graph_objects as go

from ridgeplot._colors import apply_alpha, get_color, get_colorscale, validate_colorscale
from ridgeplot._types import (
    CollectionL1,
    CollectionL2,
    DensityTrace,
    is_flat_str_collection,
    nest_shallow_collection,
)
from ridgeplot._utils import (
    get_collection_array_shape,
    normalise_min_max,
    normalise_row_attrs,
    ordered_dedup,
)
from ridgeplot._vendor.more_itertools import zip_strict

if TYPE_CHECKING:
    from collections.abc import Collection
    from typing import Callable

    from ridgeplot._colors import ColorScale
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

ColorsArray = CollectionL2[str]
"""A :data:`ColorsArray` represents the colors of traces in a ridgeplot.

Example
-------

>>> colors_array: ColorsArray = [
...     ["red", "blue", "green"],
...     ["orange", "purple"],
... ]
"""

ShallowColorsArray = CollectionL1[str]
"""Shallow type for :data:`ColorsArray`.

Example
-------

>>> colors_array: ShallowColorsArray = ["red", "blue", "green"]
"""

MidpointsArray = CollectionL2[float]
"""A :data:`MidpointsArray` represents the midpoints of colorscales in a
ridgeplot.

Example
-------

>>> midpoints_array: MidpointsArray = [
...     [0.2, 0.5, 1],
...     [0.3, 0.7],
... ]
"""

Colormode = Literal["row-index", "trace-index", "trace-index-row-wise", "mean-minmax", "mean-means"]
"""The :paramref:`ridgeplot.ridgeplot.colormode` argument in
:func:`ridgeplot.ridgeplot()`."""

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

See :func:`ridgeplot._figure_factory.RidgeplotFigureFactory.draw_density_trace`.
"""


def get_xy_extrema(densities: Densities) -> tuple[Numeric, Numeric, Numeric, Numeric]:
    r"""Get the global x-y extrema (x_min, x_max, y_min, y_max) over all
    :data:`~ridgeplot._types.DensityTrace`\s in the
    :data:`~ridgeplot._types.Densities` array.

    Parameters
    ----------
    densities
        A :data:`~ridgeplot._types.Densities` array.


    Returns
    -------
    Tuple[Numeric, Numeric, Numeric, Numeric]
        A tuple of the form (x_min, x_max, y_min, y_max).

    Examples
    --------
    >>> get_xy_extrema(
    ...     [
    ...         [
    ...             [(0, 0), (1, 1), (2, 2), (3, 3)],
    ...             [(0, 0), (1, 1), (2, 2)],
    ...             [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
    ...         ],
    ...         [
    ...             [(-2, 2), (-1, 1), (0, 1)],
    ...             [(2, 2), (3, 1), (4, 1)],
    ...         ],
    ...     ]
    ... )
    (-2, 4, 0, 4)
    """
    if len(densities) == 0:
        raise ValueError("The densities array should not be empty.")
    x_flat: list[Numeric] = []
    y_flat: list[Numeric] = []
    for row in densities:
        for trace in row:
            for x, y in trace:
                x_flat.append(x)
                y_flat.append(y)
    return min(x_flat), max(x_flat), min(y_flat), max(y_flat)


def _mul(a: tuple[Numeric, ...], b: tuple[Numeric, ...]) -> tuple[Numeric, ...]:
    """Multiply two tuples element-wise."""
    return tuple(a_i * b_i for a_i, b_i in zip(a, b))


@dataclass
class RidgeplotTrace:
    trace: DensityTrace
    label: str
    color: str


@dataclass
class RidgeplotRow:
    traces: list[RidgeplotTrace]
    y_shifted: float


class RidgeplotFigureFactory:
    """Refer to :func:`ridgeplot.ridgeplot()`."""

    def __init__(
        self,
        densities: Densities,
        colorscale: str | ColorScale,
        coloralpha: float | None,
        colormode: Colormode,
        trace_labels: LabelsArray | ShallowLabelsArray | None,
        linewidth: float,
        spacing: float,
        show_yticklabels: bool,
        xpad: float,
    ) -> None:
        # ==============================================================
        # ---  Get clean and validated input arguments
        # ==============================================================
        shape = get_collection_array_shape(densities)
        if len(shape) != 4:
            raise ValueError(
                f"Expected a 4D array of densities, got a {len(shape)}D array instead."
            )

        n_rows = len(densities)
        n_traces = sum(len(row) for row in densities)

        if isinstance(colorscale, str):
            colorscale = get_colorscale(name=colorscale)
        else:
            validate_colorscale(colorscale)

        if colormode not in self.colormode_maps:
            raise ValueError(
                f"The colormode argument should be one of "
                f"{tuple(self.colormode_maps.keys())}, got {colormode} instead."
            )

        if trace_labels is None:
            ids = iter(range(1, n_traces + 1))
            trace_labels = [[f"Trace {next(ids)}" for _ in row] for row in densities]
        else:
            if is_flat_str_collection(trace_labels):
                trace_labels = cast(ShallowLabelsArray, trace_labels)
                trace_labels = cast(LabelsArray, nest_shallow_collection(trace_labels))
            trace_labels = normalise_row_attrs(trace_labels, densities=densities)

        self.densities = densities
        self.colorscale = colorscale
        self.coloralpha = float(coloralpha) if coloralpha is not None else None
        self.colormode = colormode
        self.trace_labels: LabelsArray = trace_labels
        self.y_labels: LabelsArray = [ordered_dedup(row) for row in trace_labels]
        self.linewidth = float(linewidth)
        self.spacing = float(spacing)
        self.show_yticklabels = bool(show_yticklabels)
        self.xpad = float(xpad)

        # ==============================================================
        # ---  Other instance variables
        # ==============================================================
        self.n_rows: int = n_rows
        self.n_traces: int = n_traces
        self.x_min, self.x_max, _, self.y_max = get_xy_extrema(densities=self.densities)
        self.fig: go.Figure = go.Figure()
        self.colors: ColorsArray = self.pre_compute_colors()

        # ==============================================================
        # ---  Eagerly validate and build the RidgeplotTrace instances
        # ==============================================================
        self.rows: list[RidgeplotRow] = [
            RidgeplotRow(
                traces=[
                    RidgeplotTrace(trace=trace, label=label, color=color)
                    for trace, label, color in zip_strict(traces, labels, colors)
                ],
                y_shifted=float(-ith_row * self.y_max * self.spacing),
            )
            for ith_row, (traces, labels, colors) in enumerate(
                zip_strict(self.densities, self.trace_labels, self.colors)
            )
        ]

    @property
    def colormode_maps(self) -> dict[Colormode, Callable[[], MidpointsArray]]:
        return {
            "row-index": self._compute_midpoints_row_index,
            "trace-index": self._compute_midpoints_trace_index,
            "trace-index-row-wise": self._compute_midpoints_trace_index_row_wise,
            "mean-minmax": self._compute_midpoints_mean_minmax,
            "mean-means": self._compute_midpoints_mean_means,
        }

    def draw_base(self, x: Collection[Numeric], y_shifted: float) -> None:
        """Draw the base for a density trace.

        Adds an invisible trace at constant y that will serve as the fill-limit
        for the corresponding density trace.
        """
        self.fig.add_trace(
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

    def draw_density_trace(
        self,
        x: Collection[Numeric],
        y: Collection[Numeric],
        y_shifted: float,
        label: str,
        color: str,
    ) -> None:
        """Draw a density trace.

        Adds a density 'trace' to the Figure. The ``fill="tonexty"`` option
        fills the trace until the previously drawn trace (see
        :meth:`draw_base`). This is why the base trace must be drawn first.
        """
        self.draw_base(x=x, y_shifted=y_shifted)
        self.fig.add_trace(
            go.Scatter(
                x=x,
                y=[y_i + y_shifted for y_i in y],
                fillcolor=color,
                name=label,
                fill="tonexty",
                mode="lines",
                line=dict(
                    color="rgba(0,0,0,0.6)" if color is not None else None,
                    width=self.linewidth,
                ),
                # Hover information
                customdata=[[y_i] for y_i in y],
                hovertemplate=_DEFAULT_HOVERTEMPLATE,
            ),
        )

    def update_layout(self) -> None:
        """Update figure's layout."""
        self.fig.update_layout(
            legend=dict(traceorder="normal"),
        )
        axes_common = dict(
            zeroline=False,
            showgrid=True,
        )
        self.fig.update_yaxes(
            showticklabels=self.show_yticklabels,
            tickvals=[row.y_shifted for row in self.rows],
            ticktext=self.y_labels,
            **axes_common,
        )
        x_padding = self.xpad * (self.x_max - self.x_min)
        self.fig.update_xaxes(
            range=[self.x_min - x_padding, self.x_max + x_padding],
            showticklabels=True,
            **axes_common,
        )

    def _compute_midpoints_row_index(self) -> MidpointsArray:
        return [
            [((self.n_rows - 1) - ith_row) / (self.n_rows - 1)] * len(row)
            for ith_row, row in enumerate(self.densities)
        ]

    def _compute_midpoints_trace_index(self) -> MidpointsArray:
        midpoints = []
        ith_trace = 0
        for row in self.densities:
            midpoints_row = []
            for _ in row:
                midpoints_row.append(((self.n_traces - 1) - ith_trace) / (self.n_traces - 1))
                ith_trace += 1
            midpoints.append(midpoints_row)
        return midpoints

    def _compute_midpoints_trace_index_row_wise(self) -> MidpointsArray:
        return [
            [((len(row) - 1) - ith_row_trace) / (len(row) - 1) for ith_row_trace in range(len(row))]
            for row in self.densities
        ]

    def _compute_midpoints_mean_minmax(self) -> MidpointsArray:
        midpoints = []
        for row in self.densities:
            midpoints_row = []
            for trace in row:
                x, y = zip(*trace)
                midpoints_row.append(
                    normalise_min_max(sum(_mul(x, y)) / sum(y), min_=self.x_min, max_=self.x_max)
                )
            midpoints.append(midpoints_row)
        return midpoints

    def _compute_midpoints_mean_means(self) -> MidpointsArray:
        means = []
        for row in self.densities:
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

    def pre_compute_colors(self) -> ColorsArray:
        def _get_color(mp: float) -> str:
            color = get_color(self.colorscale, midpoint=mp)
            if self.coloralpha is not None:
                color = apply_alpha(color, alpha=self.coloralpha)
            return color

        midpoints = self.colormode_maps[self.colormode]()
        return [[_get_color(midpoint) for midpoint in row] for row in midpoints]

    def make_figure(self) -> go.Figure:
        for row in self.rows:
            for trace in row.traces:
                x, y = zip(*trace.trace)
                self.draw_density_trace(
                    x=x, y=y, y_shifted=row.y_shifted, label=trace.label, color=trace.color
                )
        self.update_layout()
        return self.fig
