"""ridgeplot: beautiful ridgeline plots in Python

The ridgeplot python library aims at providing a simple API for plotting
beautiful ridgeline plots within the extensive Plotly interactive graphing
environment.


  Sensible defaults:

  from numpy.random import normal
  from ridgeplot import ridgeplot

  # Put your real samples here...
  synthetic_samples = [normal(n / 1.2, size=600) for n in reversed(range(9))]

  # The `ridgeplot()` helper comes packed with sensible defaults
  fig = ridgeplot(samples=synthetic_samples)

  # and the returned Plotly figure is still fully customizable
  fig.update_layout(height=500, width=800)

  # show us the work!!
  fig.show()

"""
from typing import List, Optional, Union

import numpy as np
import plotly.graph_objects as go
from plotly.colors import validate_colorscale

from ridgeplot._colors import ColorScaleType, apply_alpha, get_color, get_plotly_colorscale
from ridgeplot._kde import get_densities
from ridgeplot._utils import get_extrema_3d, normalise


class RidgePlot:
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

        self.colormode_maps = {
            "index": self._compute_midpoints_index,
            "mean-minmax": self._compute_midpoints_mean_minmax,
            "mean-means": self._compute_midpoints_mean_means,
        }
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

    def update_layout(self, y_ticks: list) -> go.Figure:
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

    def build_plot(self) -> go.Figure:
        y_ticks = []
        for i, ((x, y), label, color) in enumerate(zip(self.densities, self.labels, self.colors)):
            # y_shifted is the y-origin for the new trace
            y_shifted = -i * (self.y_max * self.spacing)
            self.draw_base(x=x, y_shifted=y_shifted)
            self.draw_density_trace(x=x, y=y + y_shifted, label=label, color=color)
            y_ticks.append(y_shifted)
        self.update_layout(y_ticks=y_ticks)
        return self.fig


def ridgeplot(
    samples=None,
    densities=None,
    kernel: str = "gau",
    bandwidth="normal_reference",
    kde_points=500,
    colorscale: Union[str, ColorScaleType] = "plasma",
    colormode: str = "mean-means",
    coloralpha: Optional[float] = None,
    labels=None,
    linewidth: float = 1.4,
    spacing: float = 0.5,
    show_annotations: bool = True,
    xpad: float = 0.05,
) -> go.Figure:
    """Creates and returns a Plotly figure with a beautiful ridgeline plot.

    Note:
      If you specify both `samples` and `densities` arguments, a `ValueError`
      exception will be raised! One of these arguments should always remain set
      to `None`. See `samples` and `densities` bellow.

    Args:
      samples:
        If `samples` data is specified, Kernel Density Estimation (KDE) will be
        computed. See `kernel`, `bandwidth`, and `kde_points` for more details
         and KDE configuration options.
      densities:
        If `densities` arrays are specified instead, the KDE step will be
        skipped and all associated arguments ignored. Each density array should
        have shape `(2, N)`, but `N` may vary with each array.
      kernel:
        The Kernel to be used during Kernel Density Estimation. The default is
        a Gaussian Kernel ("gau"). Choices are:
          - "biw" for biweight
          - "cos" for cosine
          - "epa" for Epanechnikov
          - "gau" for Gaussian.
          - "tri" for triangular
          - "triw" for triweight
          - "uni" for uniform
      bandwidth:
        The bandwidth to use during Kernel Density Estimation. The default is
        "normal_reference". Choices are:
          - "scott" - 1.059 * A * nobs ** (-1/5.), where A is
          `min(std(x),IQR/1.34)`
          - "silverman" - .9 * A * nobs ** (-1/5.), where A is
            `min(std(x),IQR/1.34)`
          - "normal_reference" - C * A * nobs ** (-1/5.), where C is calculated
           from the kernel. Equivalent (up to 2 dp) to the "scott" bandwidth
           for gaussian kernels. See `statsmodels/nonparametric/bandwidths.py`
          - If a float is given, its value is used as the bandwidth.
          - If a callable is given, it's return value is used. The callable
          should take exactly two parameters, i.e., fn(x, kern), and return a
          float, where:
            * x - the clipped input data
            * kern - the kernel instance used
      kde_points:
        This argument controls the points at which KDE is computed. If an `int`
        value is passed (default), the densities will be evaluated at
        `kde_points` evenly spaced points between the min and max of each set
        of samples. However, you may also specify a custom range by instead
        passing an array of points. This array should be one-dimensional.
      colorscale:
        Any valid Plotly color-scale or a `str` with a valid named color-scale.
        See `ridgeplot.named_colorscales()` to see which names are available,
        <https://plotly.com/python/builtin-colorscales/> for more on Plotly's
        built-in color-scales.
      colormode:
        This argument controls the logic for choosing the color filling of each
        ridgeline trace. Each option provides a different method for
        calculating the `colorscale` midpoint of each trace. The default is
        mode is "mean-means". Choices are:
          - "index" - uses the trace's index. e.g. if 3 traces are specified,
           then the midpoints will be [0, 0.5, 1].
          - "mean-minmax" - uses the min-max normalized (weighted) mean of
          each density to calculate the midpoints. The normalization min and
          max values are the minimum and maximum x-values from all densities,
           respectively.
          - "mean-means" - uses the min-max normalized (weighted) mean of
          each density to calculate the midpoints. The normalization min and
          max values are the minimum and maximum mean values from all
          densities, respectively.
      coloralpha:
        If None (default), this argument will be ignored and the transparency
        values of the specifies color-scale will remain untouched. Otherwise,
        if a `float` value is passed, it will be used to overwrite the
        transparency (alpha) of the color-scale's colors.
      labels:
        A list of string labels for each trace. The default value is `None`,
        which will result in auto-generated labels of form "Trace n". If,
        instead, a list of labels is specified, it must be of the same
        size/length as the number of traces.
      linewidth:
        The traces' line width (in px).
      spacing:
        The vertical spacing between density traces, which is defined in units
        of the highest distribution (i.e. the maximum y-value).
      show_annotations:
        If `True` (default), it will show the label names as "y-tick-labels".
      xpad:
        Specifies the extra padding to use on the x-axis. It is defined in
        units of the range between the minimum and maximum x-values from all
        distributions.

    Returns:
        A Plotly figure with a ridgeline plot. You can further customize this
        figure to your liking (e.g. using the `fig.update_layout()` method).

    Raises:
      ValueError: If both `samples` and `densities` arguments are not `None`.
    """
    has_samples = samples is not None
    has_densities = densities is not None
    if has_samples and has_densities:
        raise ValueError("You may not specify both `samples` and `densities` arguments!")

    if not has_densities:
        densities = get_densities(samples, points=kde_points, kernel=kernel, bandwidth=bandwidth)

    rp = RidgePlot(
        densities=densities,
        labels=labels,
        colorscale=colorscale,
        coloralpha=coloralpha,
        colormode=colormode,
        linewidth=linewidth,
        spacing=spacing,
        show_annotations=show_annotations,
        xpad=xpad,
    )
    fig = rp.build_plot()
    return fig
