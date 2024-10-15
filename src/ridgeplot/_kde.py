from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Union

import numpy as np
import statsmodels.api as sm
from statsmodels.sandbox.nonparametric.kernels import CustomKernel as StatsmodelsKernel

from ridgeplot._types import CollectionL1, Float, Numeric

if TYPE_CHECKING:
    import numpy.typing as npt

    from ridgeplot._types import Densities, Samples, SamplesTrace, XYCoordinate


KDEPoints = Union[int, CollectionL1[Numeric]]
"""The :paramref:`ridgeplot.ridgeplot.kde_points` parameter."""

KDEBandwidth = Union[str, float, Callable[[CollectionL1[Numeric], StatsmodelsKernel], float]]
"""The :paramref:`ridgeplot.ridgeplot.bandwidth` parameter."""


def estimate_density_trace(
    trace_samples: SamplesTrace,
    points: KDEPoints,
    kernel: str,
    bandwidth: KDEBandwidth,
) -> list[XYCoordinate[Float]]:
    """Estimates a density trace from a set of samples.

    For a given set of sample values, computes the kernel densities (KDE) at
    the given points.
    """
    if not np.isfinite(trace_samples).all():  # type: ignore[call-overload]
        raise ValueError("The samples array should not contain any infs or NaNs.")
    if isinstance(points, int):
        # By default, we'll use a 'hard' KDE span. That is, we'll
        # evaluate the densities and N equally spaced points
        # over the range [min(samples), max(samples)]
        density_x = np.linspace(
            start=min(trace_samples),
            stop=max(trace_samples),
            num=points,
        )
    else:
        # Unless a specific range is specified...
        density_x = np.asarray(points)
        if density_x.ndim > 1:
            raise ValueError(
                f"The 'points' at which KDE is computed should be represented by a "
                f"one-dimensional array, got an array of shape {density_x.shape} instead."
            )

    # I decided to use statsmodels' KDEUnivariate for KDE. There are many
    # other supported alternatives in the python scientific computing
    # ecosystem. See, for instance, scipy's alternative - on which
    # statsmodels relies - `from scipy.stats import gaussian_kde`
    dens = sm.nonparametric.KDEUnivariate(trace_samples)

    # I'm hard-coding the `fft=self.kernel == "gau"` for convenience here.
    # This avoids the need to expose yet another __init__ argument (fft)
    # to this class. The drawback is that, if and when statsmodels
    # implements another kernel with fft, this will fall back to
    # using the unoptimised version (with fft = False).
    dens.fit(kernel=kernel, fft=kernel == "gau", bw=bandwidth)
    density_y = dens.evaluate(density_x)
    _validate_densities(x=density_x, y=density_y, kernel=kernel)

    return list(zip(density_x, density_y))


def _validate_densities(
    x: npt.NDArray[np.floating[Any]], y: npt.NDArray[np.floating[Any]], kernel: str
) -> None:
    # I haven't investigated the root of this issue yet
    # but statsmodels' KDEUnivariate implementation
    # can return a float('NaN') if something goes
    # wrong internally. As to avoid confusion
    # further down the pipeline, I decided
    # to check whether the correct object
    # (and shape) are being returned.
    msg = (
        f"statsmodels failed to evaluate densities using the {kernel!r} kernel. "
        "Try setting kernel='gau' (the default kernel)."
        if kernel != "gau"
        else ""
    )
    if not isinstance(y, np.ndarray):
        # Fail early if the return type is incorrect
        # Otherwise, the remaining checks will fail
        raise RuntimeError(msg)  # noqa: TRY004
    wrong_shape = y.shape != x.shape
    not_finite = ~np.isfinite(y).all()
    if wrong_shape or not_finite:
        raise RuntimeError(msg)


def estimate_densities(
    samples: Samples,
    points: KDEPoints,
    kernel: str,
    bandwidth: KDEBandwidth,
) -> Densities:
    """Perform KDE for a set of samples."""
    kde = partial(estimate_density_trace, points=points, kernel=kernel, bandwidth=bandwidth)
    return [[kde(trace_samples) for trace_samples in row] for row in samples]
