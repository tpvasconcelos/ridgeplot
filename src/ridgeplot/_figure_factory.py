from __future__ import annotations

from typing import Callable, Collection, Dict, List, Optional, Tuple, Union

from plotly import graph_objects as go

from ridgeplot._colors import (
    apply_alpha,
    get_color,
    get_colorscale,
    validate_colorscale,
)
from ridgeplot._types import (
    ColorsArrayT,
    ColorScaleT,
    DensitiesT,
    LabelsArray,
    MidpointsArrayT,
    NumericT,
)
from ridgeplot._utils import normalise_min_max


def get_xy_extrema(densities: DensitiesT) -> Tuple[NumericT, NumericT, NumericT, NumericT]:
    """Get the global x-y extrema (x_min, x_max, y_min, y_max) from all the
    :data:`~ridgeplot._types.DensityTrace`s in the
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
    x_flat: List[NumericT] = []
    y_flat: List[NumericT] = []
    for row in densities:
        for trace in row:
            for x, y in trace:
                x_flat.append(x)
                y_flat.append(y)
    return min(x_flat), max(x_flat), min(y_flat), max(y_flat)


def _mul(a: Tuple[NumericT, ...], b: Tuple[NumericT, ...]) -> Tuple[NumericT, ...]:
    """Multiply two tuples element-wise."""
    return tuple(a_i * b_i for a_i, b_i in zip(a, b))


class RidgePlotFigureFactory:
    """Refer to :func:`~ridgeplot.ridgeplot()`."""

    def __init__(
        self,
        densities: DensitiesT,
        colorscale: Union[str, ColorScaleT],
        coloralpha: Optional[float],
        colormode: str,
        labels: Optional[LabelsArray],
        linewidth: float,
        spacing: float,
        show_annotations: bool,
        xpad: float,
    ) -> None:
        # ==============================================================
        # ---  Get clean and validated input arguments
        # ==============================================================

        # TODO: Validate the densities array
        # densities = validate_densities(densities)

        n_rows = len(densities)
        n_traces = sum(len(row) for row in densities)

        if isinstance(colorscale, str):
            colorscale = get_colorscale(name=colorscale)
        validate_colorscale(colorscale)

        if colormode not in self.colormode_maps.keys():
            raise ValueError(
                f"The colormode argument should be one of "
                f"{tuple(self.colormode_maps.keys())}, got {colormode} instead."
            )

        if coloralpha is not None:
            coloralpha = float(coloralpha)

        if labels is None:
            ids = iter(range(1, n_traces + 1))
            labels = [[f"Trace {next(ids)}" for _ in row] for row in densities]

        self.densities: DensitiesT = densities
        self.colorscale: ColorScaleT = colorscale
        self.coloralpha: Optional[float] = coloralpha
        self.colormode = colormode
        self.labels: LabelsArray = labels
        self.linewidth: float = float(linewidth)
        self.spacing: float = float(spacing)
        self.show_annotations: bool = bool(show_annotations)
        self.xpad: float = float(xpad)

        # ==============================================================
        # ---  Other instance variables
        # ==============================================================
        self.n_rows: int = n_rows
        self.n_traces: int = n_traces
        self.x_min, self.x_max, _, self.y_max = get_xy_extrema(densities=self.densities)
        self.fig: go.Figure = go.Figure()
        self.colors: ColorsArrayT = self.pre_compute_colors()

    @property
    def colormode_maps(self) -> Dict[str, Callable[[], MidpointsArrayT]]:
        return {
            "row-index": self._compute_midpoints_row_index,
            "trace-index": self._compute_midpoints_trace_index,
            "mean-minmax": self._compute_midpoints_mean_minmax,
            "mean-means": self._compute_midpoints_mean_means,
        }

    def draw_base(self, x: Collection[NumericT], y_shifted: float) -> None:
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
            )
        )

    def draw_density_trace(
        self,
        x: Collection[NumericT],
        y: Collection[NumericT],
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
            ),
        )

    def update_layout(self, y_ticks: list) -> None:
        """Update figure's layout."""
        # TODO: Fix hover information
        self.fig.update_layout(
            hovermode=False,
            legend=dict(traceorder="normal"),
        )
        axes_common = dict(
            zeroline=False,
            showgrid=True,
        )
        self.fig.update_yaxes(
            showticklabels=self.show_annotations,
            tickvals=y_ticks,
            ticktext=self.labels,
            **axes_common,
        )
        x_padding = self.xpad * (self.x_max - self.x_min)
        self.fig.update_xaxes(
            range=[self.x_min - x_padding, self.x_max + x_padding],
            showticklabels=True,
            **axes_common,
        )

    def _compute_midpoints_row_index(self) -> MidpointsArrayT:
        """colormode='row-index'

        Uses the row's index. e.g. if the ridgeplot has 3 rows of traces, then
        the midpoints will be [[1, ...], [0.5, ...], [0, ...]].
        """
        return [
            [((self.n_rows - 1) - ith_row) / (self.n_rows - 1)] * len(row)
            for ith_row, row in enumerate(self.densities)
        ]

    def _compute_midpoints_trace_index(self) -> MidpointsArrayT:
        """colormode='trace-index'

        Uses the trace's index. e.g. if the ridgeplot has a total of 3 traces
        (across all rows), then the midpoints will be  0, 0.5, and 1,
        respectively.
        """
        midpoints = []
        ith_trace = 0
        for row in self.densities:
            midpoints_row = []
            for _ in row:
                midpoints_row.append(((self.n_traces - 1) - ith_trace) / (self.n_traces - 1))
                ith_trace += 1
            midpoints.append(midpoints_row)
        return midpoints

    def _compute_midpoints_mean_minmax(self) -> MidpointsArrayT:
        """colormode='mean-minmax'

        Uses the min-max normalized (weighted) mean of each density to calculate
        the midpoints. The normalization min and max values are the minimum and
        maximum x-values from all densities, respectively.
        """
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

    def _compute_midpoints_mean_means(self) -> MidpointsArrayT:
        """colormode='mean-means'

        Uses the min-max normalized (weighted) mean of each density to calculate
        the midpoints. The normalization min and max values are the minimum and
        maximum mean values from all densities, respectively.
        """
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

    def pre_compute_colors(self) -> ColorsArrayT:
        def _get_color(mp: float) -> str:
            color = get_color(self.colorscale, midpoint=mp)
            if self.coloralpha is not None:
                color = apply_alpha(color, alpha=self.coloralpha)
            return color

        midpoints = self.colormode_maps[self.colormode]()
        return [[_get_color(midpoint) for midpoint in row] for row in midpoints]

    def make_figure(self) -> go.Figure:
        y_ticks = []
        for i, (row, labels, colors) in enumerate(zip(self.densities, self.labels, self.colors)):
            # y_shifted is the y-origin for the new trace
            y_shifted = -i * float(self.y_max * self.spacing)
            y_ticks.append(y_shifted)
            for trace, label, color in zip(row, labels, colors):
                x, y = zip(*trace)
                self.draw_density_trace(x=x, y=y, y_shifted=y_shifted, label=label, color=color)
        self.update_layout(y_ticks=y_ticks)
        return self.fig
