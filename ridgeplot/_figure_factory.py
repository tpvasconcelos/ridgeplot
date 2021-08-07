from typing import Callable, Dict, List, Optional

import numpy as np
from _plotly_utils.colors import validate_colorscale
from plotly import graph_objects as go

from ridgeplot._colors import (
    ColorScaleType,
    apply_alpha,
    get_color,
    get_plotly_colorscale,
)
from ridgeplot._utils import get_extrema_3d, normalise


class _RidgePlotFigureFactory:
    """Refer to ridgeplot.ridgeplot() for docstring."""

    def __init__(
        self,
        densities,
        colorscale,
        coloralpha,
        colormode,
        labels,
        linewidth,
        spacing,
        show_annotations,
        xpad,
    ) -> None:
        # ==============================================================
        # ---  Get clean and validated input arguments
        # ==============================================================
        n_traces = len(densities)

        # Check whether all density arrays have shape (2, N)
        new_densities = []
        for i in range(n_traces):
            d = np.asarray(densities[i])
            if d.shape[0] != 2 or d.ndim != 2:
                raise ValueError(f"Each density array should have shape (2, N), got {d.shape}")
            new_densities.append(d)

        if isinstance(colorscale, str):
            colorscale = get_plotly_colorscale(name=colorscale)
        validate_colorscale(colorscale)

        if colormode not in self.colormode_maps.keys():
            raise ValueError(
                f"The colormode argument should be one of "
                f"{tuple(self.colormode_maps.keys())}, got {colormode} instead."
            )

        if coloralpha is not None:
            coloralpha = float(coloralpha)

        if labels is not None:
            n_labels = len(labels)
            if n_labels != n_traces:
                raise ValueError(f"Expected {n_traces} labels, got {n_labels}.")
            labels = list(map(str, labels))
        else:
            labels = [f"Trace {i + 1}" for i in range(n_traces)]

        self.densities: List[np.ndarray] = new_densities
        self.colorscale: ColorScaleType = colorscale
        self.coloralpha: Optional[float] = coloralpha
        self.colormode = str(colormode)
        self.labels: list = labels
        self.linewidth: float = float(linewidth)
        self.spacing: float = float(spacing)
        self.show_annotations: bool = bool(show_annotations)
        self.xpad: float = float(xpad)

        # ==============================================================
        # ---  Other instance variables
        # ==============================================================
        self.n_traces: int = n_traces
        self.x_min, self.x_max, _, self.y_max = get_extrema_3d(densities)
        self.fig: go.Figure = go.Figure()
        self.colors: List[str] = self.pre_compute_colors()

    @property
    def colormode_maps(self) -> Dict[str, Callable[[], List[float]]]:
        return {
            "index": self._compute_midpoints_index,
            "mean-minmax": self._compute_midpoints_mean_minmax,
            "mean-means": self._compute_midpoints_mean_means,
        }

    def draw_base(self, x, y_shifted) -> None:
        """Adds an invisible trace at constant y that will serve as the
        fill-limit for the corresponding density trace."""
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

    def draw_density_trace(self, x, y, label, color) -> None:
        """Adds a density 'trace' to the Figure. The fill="tonexty" option
        fills the trace until the previously drawn trace (see `draw_base`)."""
        line_color = "rgba(0,0,0,0.6)" if color is not None else None
        self.fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                fillcolor=color,
                name=label,
                fill="tonexty",
                mode="lines",
                line=dict(color=line_color, width=self.linewidth),
            ),
        )

    def update_layout(self, y_ticks: list) -> None:
        """Update figure's layout."""
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

    def _compute_midpoints_index(self) -> List[float]:
        return [i / (self.n_traces - 1) for i in reversed(range(self.n_traces))]

    def _compute_midpoints_mean_minmax(self) -> List[float]:
        means = [np.sum(x * y) / np.sum(y) for x, y in self.densities]
        return [normalise(mean, min_=self.x_min, max_=self.x_max) for mean in means]

    def _compute_midpoints_mean_means(self) -> List[float]:
        means = [np.sum(x * y) / np.sum(y) for x, y in self.densities]
        return [normalise(mean, min_=min(means), max_=max(means)) for mean in means]

    def pre_compute_colors(self) -> List[str]:
        midpoints = self.colormode_maps[self.colormode]()
        colors = []
        for midpoint in midpoints:
            color = get_color(self.colorscale, midpoint=midpoint)
            if self.coloralpha is not None:
                color = apply_alpha(color, alpha=self.coloralpha)
            colors.append(color)
        return colors

    def make_figure(self) -> go.Figure:
        y_ticks = []
        for i, ((x, y), label, color) in enumerate(zip(self.densities, self.labels, self.colors)):
            # y_shifted is the y-origin for the new trace
            y_shifted = -i * (self.y_max * self.spacing)
            self.draw_base(x=x, y_shifted=y_shifted)
            self.draw_density_trace(x=x, y=y + y_shifted, label=label, color=color)
            y_ticks.append(y_shifted)
        self.update_layout(y_ticks=y_ticks)
        return self.fig
