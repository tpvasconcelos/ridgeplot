from __future__ import annotations

from typing import Iterable, Optional, Union

import plotly.graph_objects as go

from ridgeplot._figure_factory import RidgePlotFigureFactory
from ridgeplot._kde import get_densities
from ridgeplot._types import ColorScaleType, NestedNumericSequence


def ridgeplot(
    samples=None,
    densities: Optional[Iterable[NestedNumericSequence]] = None,
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
    r"""Return a beautiful ridgeline plot |~go.Figure|.

    You have to specify either ``samples`` or ``densities``, but not both. See
    ``samples`` and ``densities`` bellow for more information.

    .. _bandwidths.py:
        https://www.statsmodels.org/stable/_modules/statsmodels/nonparametric/bandwidths.html
    .. _Plotly's built-in color-scales:
        https://plotly.com/python/builtin-colorscales/

    Parameters
    ----------
    samples
        If ``samples`` data is specified, Kernel Density Estimation (KDE) will
        be computed. See ``kernel``, ``bandwidth``, and ``kde_points`` for more
        details and KDE configuration options.
    densities
        If ``densities`` arrays are specified instead, the KDE step will be
        skipped and all associated arguments ignored. Each density array should
        have shape :math:`(2, N)`, but :math:`N` may vary with each array.
    kernel
        The Kernel to be used during Kernel Density Estimation. The default is
        a Gaussian Kernel (``"gau"``). Choices are:

        - ``"biw"`` for biweight
        - ``"cos"`` for cosine
        - ``"epa"`` for Epanechnikov
        - ``"gau"`` for Gaussian.
        - ``"tri"`` for triangular
        - ``"triw"`` for triweight
        - ``"uni"`` for uniform
    bandwidth
        The bandwidth to use during Kernel Density Estimation. The default is
        ``normal_reference``. Choices are:

        - ``"scott"`` - 1.059 * A * nobs ** (-1/5.), where A is
          ``min(std(x),IQR/1.34)``
        - ``"silverman"`` - .9 * A * nobs ** (-1/5.), where A is
          ``min(std(x),IQR/1.34)``
        - ``"normal_reference"`` - C * A * nobs ** (-1/5.), where C is
          calculated from the kernel. Equivalent (up to 2 dp) to the
          ``"scott"`` bandwidth for gaussian kernels. See `bandwidths.py`_.
        - If a float is given, its value is used as the bandwidth.
        - If a callable is given, it's return value is used. The callable
          should take exactly two parameters, i.e., ``fn(x, kern)``, and return
          a float, where:

          - ``x``: the clipped input data
          - ``kern``: the kernel instance used
    kde_points
        This argument controls the points at which KDE is computed. If an int
        value is passed (default), the densities will be evaluated at
        ``kde_points`` evenly spaced points between the min and max of each set
        of samples. However, you may also specify a custom range by instead
        passing an array of points. This array should be one-dimensional.
    colorscale
        Any valid Plotly color-scale or a str with a valid named color-scale.
        Use :func:`~ridgeplot.get_all_colorscale_names()` to see which names
        are available or check out `Plotly's built-in color-scales`_.
    colormode
        This argument controls the logic for choosing the color filling of each
        ridgeline trace. Each option provides a different method for
        calculating the ``colorscale`` midpoint of each trace. The default is
        mode is ``"mean-means"``. Choices are:

        - ``"index"`` - uses the trace's index. e.g. if 3 traces are
          specified, then the midpoints will be [0, 0.5, 1].
        - ``"mean-minmax"`` - uses the min-max normalized (weighted) mean of
          each density to calculate the midpoints. The normalization min
          and max values are the minimum and maximum x-values from all
          densities, respectively.
        - ``"mean-means"`` - uses the min-max normalized (weighted) mean of
          each density to calculate the midpoints. The normalization min
          and max values are the minimum and maximum mean values from all
          densities, respectively.
    coloralpha
        If None (default), this argument will be ignored and the transparency
        values of the specifies color-scale will remain untouched. Otherwise,
        if a float value is passed, it will be used to overwrite the
        transparency (alpha) of the color-scale's colors.
    labels
        A list of string labels for each trace. The default value is None,
        which will result in auto-generated labels of form "Trace n". If,
        instead, a list of labels is specified, it must be of the same
        size/length as the number of traces.
    linewidth
        The traces' line width (in px).
    spacing
        The vertical spacing between density traces, which is defined in units
        of the highest distribution (i.e. the maximum y-value).
    show_annotations
        If True (default), it will show the label names as "y-tick-labels".
    xpad
        Specifies the extra padding to use on the x-axis. It is defined in
        units of the range between the minimum and maximum x-values from all
        distributions.

    Returns
    -------
    :class:`plotly.graph_objects.Figure`
        A Plotly :class:`~plotly.graph_objects.Figure` with a ridgeline plot.
        You can further customize this figure to your liking (e.g. using the
        :meth:`~plotly.graph_objects.Figure.update_layout()` method).

    Raises
    ------
    :exc:`ValueError`
        If both ``samples`` and ``densities`` arguments are not None, or if
        neither ``samples`` nor ``densities`` are specified.

    """
    has_samples = samples is not None
    has_densities = densities is not None
    if has_samples and has_densities:
        raise ValueError("You may not specify both `samples` and `densities` arguments!")
    elif not has_samples and not has_densities:
        raise ValueError("You have to specify one of: `samples` or `densities`")
    elif not has_densities:
        densities = get_densities(samples, points=kde_points, kernel=kernel, bandwidth=bandwidth)

    ridgeplot_figure_factory = RidgePlotFigureFactory(
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
    fig = ridgeplot_figure_factory.make_figure()
    return fig
