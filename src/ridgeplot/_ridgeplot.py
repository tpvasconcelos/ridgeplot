from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, cast

from ridgeplot._figure_factory import create_ridgeplot
from ridgeplot._missing import MISSING
from ridgeplot._types import (
    Densities,
    Samples,
    is_shallow_densities,
    is_shallow_samples,
    nest_shallow_collection,
)
from ridgeplot._utils import normalise_densities

if TYPE_CHECKING:
    from collections.abc import Collection

    import plotly.graph_objects as go
    from typing_extensions import Literal

    from ridgeplot._color.interpolation import SolidColormode
    from ridgeplot._kde import (
        KDEBandwidth,
        KDEPoints,
    )
    from ridgeplot._missing import MissingType
    from ridgeplot._types import (
        Color,
        ColorScale,
        LabelsArray,
        NormalisationOption,
        SampleWeights,
        SampleWeightsArray,
        ShallowDensities,
        ShallowLabelsArray,
        ShallowSamples,
        ShallowSampleWeightsArray,
        ShallowTraceTypesArray,
        TraceType,
        TraceTypesArray,
    )


def _coerce_to_densities(
    samples: Samples | ShallowSamples | None,
    densities: Densities | ShallowDensities | None,
    # KDE parameters
    kernel: str,
    bandwidth: KDEBandwidth,
    kde_points: KDEPoints,
    # Histogram parameters
    nbins: int | None,
    # Common parameters for density estimation
    sample_weights: SampleWeightsArray | ShallowSampleWeightsArray | SampleWeights,
) -> Densities:
    # Importing statsmodels, scipy, and numpy can be slow,
    # so we're hiding the kde import here to only incur
    # this cost if the user actually needs this it...
    from ridgeplot._hist import bin_samples
    from ridgeplot._kde import estimate_densities

    # Input validation
    has_samples = samples is not None
    has_densities = densities is not None
    if has_samples and has_densities:
        raise ValueError("You may not specify both `samples` and `densities` arguments!")
    if not has_samples and not has_densities:
        raise ValueError("You must specify either `samples` or `densities`")

    # Exit early if densities are already provided
    if has_densities:
        if is_shallow_densities(densities):
            densities = nest_shallow_collection(densities)
        return densities

    # Transform samples into densities via KDE or histogram binning
    if is_shallow_samples(samples):
        samples = nest_shallow_collection(samples)
    samples = cast("Samples", samples)
    if nbins is not None:
        densities = bin_samples(
            samples=samples,
            nbins=nbins,
            sample_weights=sample_weights,
        )
    else:
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
    trace_type: TraceTypesArray | ShallowTraceTypesArray | TraceType | None = None,
    labels: LabelsArray | ShallowLabelsArray | None = None,
    row_labels: Collection[str] | None | Literal[False] = None,
    # KDE parameters
    kernel: str = "gau",
    bandwidth: KDEBandwidth = "normal_reference",
    kde_points: KDEPoints = 500,
    # Histogram parameters
    nbins: int | None = None,
    # Common parameters for density estimation
    sample_weights: SampleWeightsArray | ShallowSampleWeightsArray | SampleWeights = None,
    norm: NormalisationOption | None = None,
    # Coloring and styling parameters
    colorscale: ColorScale | Collection[Color] | str | None = None,
    colormode: Literal["fillgradient"] | SolidColormode = "fillgradient",
    opacity: float | None = None,
    line_color: Color | Literal["fill-color"] = "black",
    line_width: float | None = None,
    spacing: float = 0.5,
    xpad: float = 0.05,
    # Deprecated parameters
    coloralpha: float | None | MissingType = MISSING,
    linewidth: float | MissingType = MISSING,
    show_yticklabels: bool | MissingType = MISSING,
) -> go.Figure:
    r"""Return an interactive ridgeline (Plotly) |~go.Figure|.

    .. note::
        You must specify either :paramref:`.samples` or :paramref:`.densities`
        to this function, but not both. When specifying :paramref:`.samples`,
        the function will estimate the densities using either Kernel Density
        Estimation (KDE) or histogram binning. When specifying
        :paramref:`.densities`, the function will skip the density estimation
        step and use the provided densities directly. See the parameter
        descriptions below for more details.

    .. _bandwidths.py:
        https://www.statsmodels.org/stable/_modules/statsmodels/nonparametric/bandwidths.html
    .. _Plotly's built-in color-scales:
        https://plotly.com/python/builtin-colorscales/
    .. _ragged:
       https://en.wikipedia.org/wiki/Jagged_array

    Parameters
    ----------
    samples : Samples or ShallowSamples
        If ``samples`` data is specified, either Kernel Density Estimation (KDE)
        or histogram binning will be performed to estimate the underlying
        densities.

        See :paramref:`.kernel`, :paramref:`.bandwidth`, and
        :paramref:`.kde_points` for more details on the different KDE
        parameters. See :paramref:`.nbins` for more details on histogram
        binning. The :paramref:`.sample_weights` parameter can be used for both
        KDE and histogram binning.

        The ``samples`` argument should be an array of shape
        :math:`(R, T_r, S_t)`. Note that we support irregular (`ragged`_)
        arrays, where:

        - :math:`R` is the number of rows in the plot
        - :math:`T_r` is the number of traces per row, where each row
          :math:`r \in R` can have a different number of traces.
        - :math:`S_t` is the number of samples per trace, where each trace
          :math:`t \in T_r` can also have a different number of samples.

        The density estimation step will be performed over the sample values
        (:math:`S_t`) for all traces. The resulting array will be a (4D)
        :paramref:`.densities` array of shape :math:`(R, T_r, P_t, 2)`
        (see :paramref:`.densities` below for more details).

    densities : Densities or ShallowDensities
        If a ``densities`` array is specified, the density estimation step will
        be skipped and all associated arguments ignored. Each density array
        should have shape :math:`(R, T_r, P_t, 2)` (4D). Just like the
        :paramref:`.samples` argument, we also support irregular (`ragged`_)
        ``densities`` arrays, where:

        - :math:`R` is the number of rows in the plot
        - :math:`T_r` is the number of traces per row, where each row
          :math:`r \in R` can have a different number of traces.
        - :math:`P_t` is the number of points per trace, where each trace
          :math:`t \in T_r` can also have a different number of points.
        - :math:`2` is the number of coordinates per point (x and y)

        See :paramref:`.samples` above for more details.

    trace_type : TraceTypesArray or ShallowTraceTypesArray or TraceType or None
        The type of trace to display. Choices are ``'area'`` or ``'bar'``. If a
        single value is passed, it will be used for all traces. If a list of
        values is passed, it should have the same shape as the samples array.
        If not specified (default), the traces will be displayed as area plots
        (``trace_type='area'``) unless histogram binning is used, in which case
        the traces will be displayed as bar plots (``trace_type='bar'``).

        .. versionadded:: 0.3.0

    labels : LabelsArray or ShallowLabelsArray or None
        A collection of string labels for each trace. If not specified
        (default), the labels will be automatically generated as
        ``"Trace {n}"``, where ``n`` is the trace's index. If instead a
        collection of labels is specified, it should have the same shape as the
        samples array.

    row_labels : Collection[str] or None or False
        A collection of string labels for each row in the ridgeline plot. If
        specified, the length of this collection should match the number of rows
        in the plot (i.e., the :math:`R` dimension in the :paramref:`.samples`
        or :paramref:`.densities` parameter). If not specified (default), the
        row labels displayed on the y-axis will be automatically generated based
        on the :paramref:`.labels` argument. If set to ``False``, the row
        labels won't be displayed at all.

        .. versionadded:: 0.4.0
            Added support for custom row labels, and replaced the deprecated
            :paramref:`.show_yticklabels` parameter.

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
          should take exactly two arguments, i.e., ``fn(x, kern)``, and return
          a float, where:

          - ``x``: the clipped input data
          - ``kern``: the kernel instance used

    kde_points : KDEPoints
        This parameter controls the points at which KDE is computed. If an
        ``int`` value is passed (default=500), the densities will be evaluated
        at ``kde_points`` evenly spaced points between the min and max of each
        set of samples. Optionally, you can also pass a custom 1D numerical
        array, which will be used for all traces.

    nbins : int or None
        The number of bins to use when applying histogram binning. If not
        specified (default), KDE will be used instead of histogram binning.

        .. versionadded:: 0.3.0

    sample_weights : SampleWeightsArray or ShallowSampleWeightsArray or SampleWeights or None
        An (optional) array of KDE weights corresponding to each sample. The
        weights should have the same shape as the samples array. If not
        specified (default), all samples will be weighted equally.

    norm : NormalisationOption or None
        The normalisation option to use when normalising the densities. If not
        specified (default), no normalisation will be applied and the densities
        will be used *as is*. The following normalisation options are available:

        - ``"probability"`` - normalise the densities by dividing each trace by
          its sum.
        - ``"percent"`` - same as ``"probability"``, but the normalised values
          are multiplied by 100.

        .. versionadded:: 0.2.0

    colorscale : ColorScale or Collection[Color] or str or None
        A continuous color scale used to color the different traces in the
        ridgeline plot. It can be represented by a string name (e.g.,
        ``"viridis"``), a :data:`~ridgeplot._types.ColorScale` object, or a
        list of valid :data:`~ridgeplot._colors.Color` objects. If a string name
        is provided, it must be one of the built-in color scales (see
        :func:`~ridgeplot.list_all_colorscale_names()` and
        `Plotly's built-in color-scales`_). If a list of colors is provided, it
        must be a list of valid CSS colors (e.g.,
        ``["rgb(255, 0, 0)", "blue", "hsl(120, 100%, 50%)"]``). The list will
        ultimately be converted into a :data:`~ridgeplot._types.ColorScale`
        object, assuming the colors provided are evenly spaced. If not specified
        (default), the color scale will be inferred from current Plotly
        template.

    colormode : "fillgradient" or SolidColormode
        This parameter controls the logic used for the coloring of each
        ridgeline trace.

        The ``"fillgradient"`` mode (default) will fill each trace with a
        gradient using the specified :paramref:`.colorscale`. The gradient
        normalisation is done using the minimum and maximum x-values over all
        densities.

        All other modes provide different methods for calculating interpolation
        values from the specified :paramref:`.colorscale` (i.e., a float value
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

    opacity : float or None
        If None (default), this parameter will be ignored and the transparency
        values of the specified color-scale will remain untouched. Otherwise,
        if a float value is passed, it will be used to overwrite the
        opacity/transparency of the color-scale's colors.

        .. versionadded:: 0.2.0
            Replaces the deprecated :paramref:`.coloralpha` parameter.

    line_color : Color or "fill-color"
        The color of the traces' lines. Any valid CSS color is allowed
        (default: ``"black"``). If the value is set to "fill-color", the line
        color will be the same as the fill color of the traces (see
        :paramref:`.colormode`). If ``colormode='fillgradient'``, the line color
        will be the mean color of the fill gradient (i.e., equivalent to the
        fill color when ``colormode='mean-minmax'``).

        .. versionadded:: 0.2.0

    line_width : float or None
        The traces' line width (in px). If not specified (default), area plots
        will have a line width of 1.5 px, and bar plots will have a line width
        of 0.5 px.

        .. versionadded:: 0.2.0
            Replaces the deprecated :paramref:`.linewidth` parameter.

        .. versionchanged:: 0.2.0
            The default value changed from 1 to 1.5

    spacing : float
        The vertical spacing between density traces, which is defined in units
        of the highest distribution (i.e., the maximum y-value).

    xpad : float
        Specifies the extra padding to use on the x-axis. It is defined in
        units of the range between the minimum and maximum x-values from all
        distributions.

    coloralpha : float

        .. deprecated:: 0.2.0
            Use :paramref:`.opacity` instead.

    linewidth : float

        .. deprecated:: 0.2.0
            Use :paramref:`.line_width` instead.

    show_yticklabels : bool

        .. deprecated:: 0.4.0
            Use :paramref:`.row_labels` instead.

    Returns
    -------
    :class:`plotly.graph_objects.Figure`
        A Plotly :class:`~plotly.graph_objects.Figure` with a ridgeline plot.
        You can further customize this figure to your liking (e.g. using the
        :meth:`~plotly.graph_objects.Figure.update_layout()` method).

    Raises
    ------
    :exc:`ValueError`
        If both :paramref:`.samples` and :paramref:`.densities` are specified,
        or if neither of them is specified. i.e., you may only specify one of
        them.

    """
    if trace_type is None:
        trace_type = "area" if nbins is None else "bar"

    densities = _coerce_to_densities(
        samples=samples,
        densities=densities,
        kernel=kernel,
        bandwidth=bandwidth,
        kde_points=kde_points,
        nbins=nbins,
        sample_weights=sample_weights,
    )
    del samples, kernel, bandwidth, kde_points, nbins, sample_weights

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
        if line_width is not None:
            raise ValueError(
                "You may not specify both the 'linewidth' and 'line_width' arguments! "
                "HINT: Use the new 'line_width' argument instead of the deprecated 'linewidth'."
            )
        warnings.warn(
            "The 'linewidth' argument has been deprecated in favor of 'line_width'. "
            "Support for the deprecated argument will be removed in a future version.",
            DeprecationWarning,
            stacklevel=2,
        )
        line_width = linewidth

    if show_yticklabels is not MISSING:
        if row_labels is not None:
            raise ValueError(
                "You may not specify both the 'show_yticklabels' and 'row_labels' arguments! "
                "HINT: Use the new 'row_labels' argument instead of the deprecated "
                "'show_yticklabels'."
            )
        warnings.warn(
            "The 'show_yticklabels' argument has been deprecated in favor of 'row_labels'. "
            "Support for the deprecated argument will be removed in a future version.",
            DeprecationWarning,
            stacklevel=2,
        )
        row_labels = row_labels if show_yticklabels else False

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
        trace_types=trace_type,
        row_labels=row_labels,
        colorscale=colorscale,
        opacity=opacity,
        colormode=colormode,
        line_color=line_color,
        line_width=line_width,
        spacing=spacing,
        xpad=xpad,
    )
    return fig
