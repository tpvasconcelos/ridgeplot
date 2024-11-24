from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Literal, cast

from ridgeplot._figure_factory import (
    LabelsArray,
    ShallowLabelsArray,
    create_ridgeplot,
)
from ridgeplot._missing import MISSING, MissingType
from ridgeplot._types import (
    Color,
    ColorScale,
    Densities,
    NormalisationOption,
    Samples,
    ShallowDensities,
    ShallowSamples,
    is_shallow_densities,
    is_shallow_samples,
    nest_shallow_collection,
)
from ridgeplot._utils import normalise_densities

if TYPE_CHECKING:
    from collections.abc import Collection

    import plotly.graph_objects as go

    from ridgeplot._color.interpolation import SolidColormode
    from ridgeplot._kde import (
        KDEBandwidth,
        KDEPoints,
        SampleWeights,
        SampleWeightsArray,
        ShallowSampleWeightsArray,
    )


def _coerce_to_densities(
    samples: Samples | ShallowSamples | None,
    densities: Densities | ShallowDensities | None,
    kernel: str,
    bandwidth: KDEBandwidth,
    kde_points: KDEPoints,
    sample_weights: SampleWeightsArray | ShallowSampleWeightsArray | SampleWeights,
) -> Densities:
    # Importing statsmodels, scipy, and numpy can be slow,
    # so we're hiding the kde import here to only incur
    # this cost if the user actually needs this it...
    from ridgeplot._kde import estimate_densities

    has_samples = samples is not None
    has_densities = densities is not None
    if has_samples and has_densities:
        raise ValueError("You may not specify both `samples` and `densities` arguments!")
    if not has_samples and not has_densities:
        raise ValueError("You must specify either `samples` or `densities`")
    if has_densities:
        if is_shallow_densities(densities):
            densities = nest_shallow_collection(densities)
        densities = cast(Densities, densities)
    else:
        if is_shallow_samples(samples):
            samples = nest_shallow_collection(samples)
        samples = cast(Samples, samples)
        densities = estimate_densities(
            samples=samples,
            points=kde_points,
            kernel=kernel,
            bandwidth=bandwidth,
            sample_weights=sample_weights,
        )
    return densities


def ridgeplot(
    samples: Samples | ShallowSamples | None = None,
    densities: Densities | ShallowDensities | None = None,
    kernel: str = "gau",
    bandwidth: KDEBandwidth = "normal_reference",
    kde_points: KDEPoints = 500,
    sample_weights: SampleWeightsArray | ShallowSampleWeightsArray | SampleWeights = None,
    colorscale: ColorScale | Collection[Color] | str | None = None,
    colormode: Literal["fillgradient"] | SolidColormode = "fillgradient",
    opacity: float | None = None,
    labels: LabelsArray | ShallowLabelsArray | None = None,
    norm: NormalisationOption | None = None,
    line_color: Color | Literal["fill-color"] = "black",
    line_width: float = 1.5,
    spacing: float = 0.5,
    show_yticklabels: bool = True,
    xpad: float = 0.05,
    # Deprecated arguments
    coloralpha: float | None | MissingType = MISSING,
    linewidth: float | MissingType = MISSING,
) -> go.Figure:
    r"""Return an interactive ridgeline (Plotly) |~go.Figure|.

    .. note::
        You must pass either :paramref:`samples` or :paramref:`densities` to
        this function, but not both. See descriptions below for more details.

    .. _bandwidths.py:
        https://www.statsmodels.org/stable/_modules/statsmodels/nonparametric/bandwidths.html
    .. _Plotly's built-in color-scales:
        https://plotly.com/python/builtin-colorscales/
    .. _ragged:
       https://en.wikipedia.org/wiki/Jagged_array

    Parameters
    ----------
    samples : Samples or ShallowSamples, optional
        If ``samples`` data is specified, Kernel Density Estimation (KDE) will
        be computed. See :paramref:`kernel`, :paramref:`bandwidth`,
        :paramref:`kde_points`, and :paramref:`sample_weights` for more details
        and KDE configuration options. The ``samples`` argument should be an
        array of shape :math:`(R, T_r, S_t)`. Note that we support irregular
        (`ragged`_) arrays, where:

        - :math:`R` is the number of rows in the plot
        - :math:`T_r` is the number of traces per row, where each row
          :math:`r \in R` can have a different number of traces.
        - :math:`S_t` is the number of samples per trace, where each trace
          :math:`t \in T_r` can also have a different number of samples.

        The KDE will be performed over the sample values (:math:`S_t`) for all
        traces. After the KDE, the resulting array will be a (4D)
        :paramref:`densities` array with shape :math:`(R, T_r, P_t, 2)`
        (see below for more details).

    densities : Densities or ShallowDensities, optional
        If a ``densities`` array is specified, the KDE step will be skipped and
        all associated arguments ignored. Each density array should have shape
        :math:`(R, T_r, P_t, 2)` (4D). Just like the :paramref:`samples`
        argument, we also support irregular (`ragged`_) ``densities`` arrays,
        where:

        - :math:`R` is the number of rows in the plot
        - :math:`T_r` is the number of traces per row, where each row
          :math:`r \in R` can have a different number of traces.
        - :math:`P_t` is the number of points per trace, where each trace
          :math:`t \in T_r` can also have a different number of points.
        - :math:`2` is the number of coordinates per point (x and y)

    kernel : str
        The Kernel to be used during Kernel Density Estimation. The default is
        a Gaussian Kernel (``"gau"``). Choices are:

        - ``"biw"`` for biweight
        - ``"cos"`` for cosine
        - ``"epa"`` for Epanechnikov
        - ``"gau"`` for Gaussian.
        - ``"tri"`` for triangular
        - ``"triw"`` for triweight
        - ``"uni"`` for uniform

    bandwidth : KDEBandwidth
        The bandwidth to use during Kernel Density Estimation. The default is
        ``"normal_reference"``. Choices are:

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

    kde_points : KDEPoints
        This argument controls the points at which KDE is computed. If an
        ``int`` value is passed (default=500), the densities will be evaluated
        at ``kde_points`` evenly spaced points between the min and max of each
        set of samples. Optionally, you can also pass a custom 1D numerical
        array, which will be used for all traces.

    sample_weights : SampleWeightsArray or ShallowSampleWeightsArray or SampleWeights, optional
        An (optional) array of KDE weights corresponding to each sample. The
        weights should be of the same shape as the samples array. If not
        specified (default), all samples will be weighted equally.

    colorscale : ColorScale or Collection[Color] or str
        A continuous color scale used to color the different traces in the
        ridgeline plot. It can be represented by a string name (e.g.,
        ``"viridis"``), a :data:`~ridgeplot._colors.ColorScale` object, or a
        list of colors (see :data:`~ridgeplot._colors.Color`). If a string name
        is provided, it must be one of the built-in color scales (see
        :func:`~ridgeplot.list_all_colorscale_names()` and
        `Plotly's built-in color-scales`_). If a list of colors is provided, it
        must be a list of valid CSS colors (e.g.,
        ``["rgb(255, 0, 0)", "blue", "hsl(120, 100%, 50%)"]``). The list will
        ultimately be converted to a :data:`~ridgeplot._colors.ColorScale` object, assuming the
        colors are evenly spaced.

    colormode : "fillgradient" or SolidColormode
        This argument controls the logic used for the coloring of each
        ridgeline trace.

        The ``"fillgradient"`` mode (default) will fill each trace with a
        gradient using the specified :paramref:`colorscale`. The gradient
        normalisation is done using the minimum and maximum x-values over all
        densities.

        All other modes provide different methods for calculating interpolation
        values from the specified :paramref:`colorscale` (i.e., a float value
        between 0 and 1) for each trace. The interpolated color will be used to
        color each trace with a solid color. The available modes are:

        - ``"row-index"`` - uses the row's index. This is useful when the
          desired effect is to have the same color for all traces on the same
          row. e.g., if a ridgeplot has 3 rows of traces, then the color scale
          interpolation values will be ``[[0, ...], [0.5, ...], [1, ...]]``,
          respectively.
        - ``"trace-index"`` - uses the trace's index. e.g., if a ridgeplot has
          a total of 3 traces (across all rows), then the color scale
          interpolation values will be 0, 0.5, and 1, respectively, and
          regardless of each trace's row.
        - ``"trace-index-row-wise"`` - uses the row-wise trace index. This is
          similar to the ``"trace-index"`` mode, but the trace index is reset
          for each row. e.g., if a ridgeplot has a row with only one trace and
          another with two traces, then the color scale interpolation values
          will be ``[[0], [0, 1]]``, respectively.
        - ``"mean-minmax"`` - uses the min-max normalised (weighted) mean of
          each density to calculate the interpolation values. The normalisation
          min and max values are the *absolute* minimum and maximum x-values
          over all densities. This mode is useful when the desired effect is to
          have the color of each trace reflect the mean of the distribution,
          while also taking into account the distributions' spread.
        - ``"mean-means"`` - similar to the ``"mean-minmax"`` mode, but where
          the normalisation min and max values are the minimum and maximum
          *mean* x-values over all densities. This mode is useful when the
          desired effect is to have the color of each trace reflect the mean of
          the distribution, but without taking into account the entire
          variability of the distributions.

        .. versionchanged:: 0.2.0
            The default value changed from ``"mean-minmax"`` to
            ``"fillgradient"``.

    opacity : float, optional
        If None (default), this argument will be ignored and the transparency
        values of the specifies color-scale will remain untouched. Otherwise,
        if a float value is passed, it will be used to overwrite the
        opacity/transparency of the color-scale's colors.

        .. versionadded:: 0.2.0
            Replaces the deprecated :paramref:`coloralpha` argument.

    labels : LabelsArray or ShallowLabelsArray, optional
        A list of string labels for each trace. The default value is None,
        which will result in auto-generated labels of form "Trace n". If,
        instead, a list of labels is specified, it must be of the same
        size/length as the number of traces.

    norm : NormalisationOption, optional
        The normalisation option to use when normalising the densities. The
        default is None, which means no normalisation will be applied and the
        densities will be used as is. The following normalisation options are
        available:

        - ``"probability"`` - normalise the densities by dividing each trace by
          its sum.
        - ``"percent"`` - same as ``"probability"``, but the normalised values
          are multiplied by 100.

        .. versionadded:: 0.2.0

    line_color : Color or "fill-color", optional
        The color of the traces' lines. Any valid CSS color is allowed
        (default: ``"black"``). If the value is set to "fill-color", the line
        color will be the same as the fill color of the traces (see
        :paramref:`colormode`). If ``colormode='fillgradient'``, the line color
        will be the mean color of the fill gradient (i.e., equivalent to the
        fill color when ``colormode='mean-minmax'``).

        .. versionadded:: 0.2.0

    line_width : float
        The traces' line width (in px).

        .. versionadded:: 0.2.0
            Replaces the deprecated :paramref:`linewidth` argument.

        .. versionchanged:: 0.2.0
            The default value changed from 1 to 1.5

    spacing : float
        The vertical spacing between density traces, which is defined in units
        of the highest distribution (i.e. the maximum y-value).

    show_yticklabels : bool
        Whether to show the tick labels on the y-axis. The default is True.

        .. versionadded:: 0.1.21
            Replaces the deprecated :paramref:`show_annotations` argument.

    xpad : float
        Specifies the extra padding to use on the x-axis. It is defined in
        units of the range between the minimum and maximum x-values from all
        distributions.

    coloralpha : float, optional

        .. deprecated:: 0.2.0
            Use :paramref:`opacity` instead.

    linewidth : float

        .. deprecated:: 0.2.0
            Use :paramref:`line_width` instead.

    Returns
    -------
    :class:`plotly.graph_objects.Figure`
        A Plotly :class:`~plotly.graph_objects.Figure` with a ridgeline plot.
        You can further customize this figure to your liking (e.g. using the
        :meth:`~plotly.graph_objects.Figure.update_layout()` method).

    Raises
    ------
    :exc:`ValueError`
        If both :paramref:`samples` and :paramref:`densities` are specified, or
        if neither of them is specified. i.e. you may only specify one of them.

    """
    densities = _coerce_to_densities(
        samples=samples,
        densities=densities,
        kernel=kernel,
        bandwidth=bandwidth,
        kde_points=kde_points,
        sample_weights=sample_weights,
    )
    del samples, kernel, bandwidth, kde_points

    if norm:
        densities = normalise_densities(densities, norm=norm)

    if coloralpha is not MISSING:
        if opacity is not None:
            raise ValueError(
                "You may not specify both the 'coloralpha' and 'opacity' arguments! "
                "HINT: Use the new 'opacity' argument instead of the deprecated 'coloralpha'."
            )
        warnings.warn(
            "The 'coloralpha' argument has been deprecated in favor of 'opacity'. "
            "Support for the deprecated argument will be removed in a future version.",
            DeprecationWarning,
            stacklevel=2,
        )
        opacity = coloralpha

    if linewidth is not MISSING:
        warnings.warn(
            "The 'linewidth' argument has been deprecated in favor of 'line_width'. "
            "Support for the deprecated argument will be removed in a future version.",
            DeprecationWarning,
            stacklevel=2,
        )
        line_width = linewidth

    if colorscale == "default":
        warnings.warn(
            "colorscale='default' is deprecated and support for it will be removed in a future "
            "version. Please use colorscale=px.colors.DEFAULT_PLOTLY_COLORS for the same effect. "
            "To list all supported colorscale names, please refer to Plotly's "
            "px.colors.named_colorscales(), or visit: "
            "https://plotly.com/python/builtin-colorscales/#named-builtin-continuous-color-scales",
            DeprecationWarning,
            stacklevel=2,
        )

    del coloralpha, linewidth

    fig = create_ridgeplot(
        densities=densities,
        trace_labels=labels,
        colorscale=colorscale,
        opacity=opacity,
        colormode=colormode,
        line_color=line_color,
        line_width=line_width,
        spacing=spacing,
        show_yticklabels=show_yticklabels,
        xpad=xpad,
    )
    return fig
