from __future__ import annotations

import warnings
from typing import Optional, Union, cast

import plotly.graph_objects as go

from ridgeplot._figure_factory import RidgePlotFigureFactory
from ridgeplot._kde import estimate_densities
from ridgeplot._types import (
    ColorScaleT,
    DensitiesT,
    KDEBandwidthT,
    KDEPointsT,
    LabelsArray,
    SamplesT,
    ShallowDensitiesT,
    ShallowLabelsArrayT,
    ShallowSamplesT,
    is_flat_str_collection,
    is_shallow_densities,
    is_shallow_samples,
    nest_shallow_collection,
)


def ridgeplot(
    samples: Union[SamplesT, ShallowSamplesT, None] = None,
    densities: Union[DensitiesT, ShallowDensitiesT, None] = None,
    kernel: str = "gau",
    bandwidth: KDEBandwidthT = "normal_reference",
    kde_points: KDEPointsT = 500,
    colorscale: Union[str, ColorScaleT] = "plasma",
    colormode: str = "mean-means",
    coloralpha: Optional[float] = None,
    labels: Union[LabelsArray, ShallowLabelsArrayT, None] = None,
    linewidth: float = 1.4,
    spacing: float = 0.5,
    show_annotations: bool = True,
    xpad: float = 0.05,
) -> go.Figure:
    r"""Return a beautiful ridgeline plot |~go.Figure|.

    You have to specify either ``samples`` or ``densities``, but not both. See
    ``samples`` and ``densities`` below for more information.

    .. _bandwidths.py:
        https://www.statsmodels.org/stable/_modules/statsmodels/nonparametric/bandwidths.html
    .. _Plotly's built-in color-scales:
        https://plotly.com/python/builtin-colorscales/

    Parameters
    ----------
    samples
        If ``samples`` data is specified, Kernel Density Estimation (KDE) will
        be computed. See ``kernel``, ``bandwidth``, and ``kde_points`` for more
        details and KDE configuration options. The ``samples`` argument should
        be a 3D array with shape :math:`(R, T, P_t)`, where:

        - :math:`R` is the number of rows in the plot
        - :math:`T` is the number of traces per row (this value can be different
          for each row, *à la* awkward array)
        - :math:`P_t` is the number of points per trace (this value can be also
           different for each trace :math:`t \in T`)

        The KDE will be performed at the points :math:`P_t` for each trace
        :math:`t \in T`. The resulting array will be a ``densities`` array with
        shape :math:`(R, T, P_t, 2)` (see ``densities`` below).
    densities
        If ``densities`` arrays are specified instead, the KDE step will be
        skipped and all associated arguments ignored. Each density array should
        have shape :math:`(R, T, P_t, 2)` (4D), where:

        - :math:`R` is the number of rows in the plot
        - :math:`T` is the number of traces per row (this value can be different
          for each row, *à la* awkward array)
        - :math:`P_t` is the number of points per trace (this value can be also
          different for each trace :math:`t \in T`)
        - :math:`2` is the number of coordinates per point (x and y)
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
        This argument controls the points at which KDE is computed. If an
        ``int`` value is passed (default=500), the densities will be evaluated
        at ``kde_points`` evenly spaced points between the min and max of each
        set of samples. Optionally, you can also pass a custom 1D numerical
        array, which will be used for all traces.
    colorscale
        Any valid Plotly color-scale or a str with a valid named color-scale.
        Use :func:`~ridgeplot.get_all_colorscale_names()` to see which names
        are available or check out `Plotly's built-in color-scales`_.
    colormode
        This argument controls the logic for choosing the color filling of each
        ridgeline trace. Each option provides a different method for
        calculating the ``colorscale`` midpoint of each trace. The default is
        mode is ``"mean-means"``. Choices are:

        - ``"row-index"`` - uses the row's index. e.g. if the ridgeplot has 3
          rows of traces, then the midpoints will be
          ``[[0, ...], [0.5, ...], [1, ...]]``.
        - ``"trace-index"`` - uses the trace's index. e.g. if the ridgeplot has
          a total of 3 traces (across all rows), then the midpoints will be
          0, 0.5, and 1, respectively.
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

    if has_densities and is_shallow_densities(densities):
        densities = cast(ShallowDensitiesT, densities)
        densities = cast(DensitiesT, nest_shallow_collection(densities))
    else:
        if is_shallow_samples(samples):
            samples = cast(ShallowSamplesT, samples)
            samples = nest_shallow_collection(samples)
        samples = cast(SamplesT, samples)
        # Convert samples to densities
        densities = estimate_densities(
            samples=samples,
            points=kde_points,
            kernel=kernel,
            bandwidth=bandwidth,
        )

    if is_flat_str_collection(labels):
        labels = cast(ShallowLabelsArrayT, labels)
        labels = cast(LabelsArray, nest_shallow_collection(labels))

    if colormode == "index":
        warnings.warn(
            "The colormode='index' value has been deprecated in favor of "
            "colormode='row-index', which provides the same functionality but "
            "is more explicit and allows to distinguishing between the "
            "'row-index' and 'trace-index' modes. Support for the deprecated "
            "colormode='index' value will be removed in a future version.",
            DeprecationWarning,
            stacklevel=2,
        )
        colormode = "row-index"

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
