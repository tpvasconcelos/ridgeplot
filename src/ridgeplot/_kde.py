from __future__ import annotations

import sys
from collections.abc import Collection
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Optional, Union, cast

import numpy as np
import statsmodels.api as sm
from statsmodels.sandbox.nonparametric.kernels import CustomKernel as StatsmodelsKernel

if sys.version_info >= (3, 13):
    from typing import TypeIs
else:
    from typing_extensions import TypeIs

from ridgeplot._types import (
    CollectionL1,
    CollectionL2,
    Float,
    Numeric,
    is_flat_numeric_collection,
    nest_shallow_collection,
)
from ridgeplot._utils import normalise_row_attrs
from ridgeplot._vendor.more_itertools import zip_strict

if TYPE_CHECKING:
    import numpy.typing as npt

    from ridgeplot._types import Densities, Samples, SamplesTrace, XYCoordinate


KDEPoints = Union[int, CollectionL1[Numeric]]
"""The :paramref:`ridgeplot.ridgeplot.kde_points` parameter."""

KDEBandwidth = Union[str, float, Callable[[CollectionL1[Numeric], StatsmodelsKernel], float]]
"""The :paramref:`ridgeplot.ridgeplot.bandwidth` parameter."""

SampleWeights = Optional[CollectionL1[Numeric]]
"""An array of KDE weights corresponding to each sample."""

SampleWeightsArray = CollectionL2[SampleWeights]
"""A :data:`SampleWeightsArray` represents the weights of the datapoints in a
:data:`Samples` array. The shape of the :data:`SampleWeightsArray` array should
match the shape of the corresponding :data:`Samples` array."""

ShallowSampleWeightsArray = CollectionL1[SampleWeights]
"""Shallow type for :data:`SampleWeightsArray`."""


def _is_sample_weights(obj: Any) -> TypeIs[SampleWeights]:
    """Type guard for :data:`SampleWeights`.

    Examples
    --------
    >>> _is_sample_weights("definitely not")
    False
    >>> _is_sample_weights([1, 2, 3.14])
    True
    >>> _is_sample_weights([1, 2, "3"])
    False
    >>> _is_sample_weights(None)
    True
    """
    return obj is None or is_flat_numeric_collection(obj)


def _is_shallow_sample_weights(obj: Any) -> TypeIs[ShallowSampleWeightsArray]:
    """Type guard for :data:`ShallowSampleWeightsArray`.

    Examples
    --------
    >>> _is_shallow_sample_weights("definitely not")
    False
    >>> _is_shallow_sample_weights([1, 2, 3])
    False
    >>> _is_shallow_sample_weights([[1, 2, 3], [4, 5, 6]])
    True
    >>> _is_shallow_sample_weights([[1, 2, "3"], [4, 5, None]])
    False
    >>> _is_shallow_sample_weights([[1, 2, 3], None])
    True
    """
    return isinstance(obj, Collection) and all(map(_is_sample_weights, obj))


def normalize_sample_weights(
    sample_weights: SampleWeightsArray | ShallowSampleWeightsArray | SampleWeights,
    samples: Samples,
) -> SampleWeightsArray:
    """Normalize the sample weights to the correct shape.

    Examples
    --------
    >>> samples = [[[1, 2], [3, 4]], [[5, 6]]]
    >>> normalize_sample_weights(None, samples)
    [[None, None], [None]]
    >>> normalize_sample_weights([8, 9], samples)
    [[[8, 9], [8, 9]], [[8, 9]]]
    >>> weights = [[[0, 1], None], [[2, 3]]]
    >>> normalize_sample_weights(weights, samples) == weights
    True
    >>> normalize_sample_weights([None, [0, 1]], samples)
    [[None, None], [[0, 1]]]
    """
    if _is_sample_weights(sample_weights):
        return [[sample_weights] * len(row) for row in samples]
    # TODO: Investigate this issue with mypy's type narrowing...
    sample_weights = cast(  # type: ignore[unreachable]
        Union[SampleWeightsArray, ShallowSampleWeightsArray],
        sample_weights,
    )
    if _is_shallow_sample_weights(sample_weights):
        sample_weights = nest_shallow_collection(sample_weights)
    sample_weights = normalise_row_attrs(sample_weights, l2_target=samples)
    return sample_weights


def estimate_density_trace(
    trace_samples: SamplesTrace,
    points: KDEPoints,
    kernel: str,
    bandwidth: KDEBandwidth,
    weights: SampleWeights = None,
) -> list[XYCoordinate[Float]]:
    """Estimates a density trace from a set of samples.

    For a given set of sample values, computes the kernel densities (KDE) at
    the given points.
    """
    trace_samples = np.asarray(trace_samples, dtype=float)
    if not np.isfinite(trace_samples).all():
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
    if weights is not None:
        weights = np.asarray(weights, dtype=float)
        if len(weights) != len(trace_samples):
            raise ValueError("The weights array should have the same length as the samples array.")
        if not np.isfinite(weights).all():
            raise ValueError("The weights array should not contain any infs or NaNs.")

    # ref: https://github.com/tpvasconcelos/ridgeplot/issues/116
    dens = sm.nonparametric.KDEUnivariate(trace_samples)

    # I'm hard-coding `fft=kernel == "gau" and weights is not None`
    # to avoid exposing yet another KDE parameter in ridgeplot()
    # If we ever find any issues with this heuristic, I would
    # prefer just leaving `fft=False` here and *not* expose
    # this parameter to the user. If the user wants more
    # control over the KDE estimation, they can always
    # implement their own logic and pass `densities`
    # directly to the ridgeplot() figure factory.
    dens.fit(
        kernel=kernel,
        fft=kernel == "gau" and weights is None,
        bw=bandwidth,
        weights=weights,
    )
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
    sample_weights: SampleWeightsArray | ShallowSampleWeightsArray | SampleWeights = None,
) -> Densities:
    """Perform KDE for a set of samples."""
    normalised_weights = normalize_sample_weights(sample_weights=sample_weights, samples=samples)
    kde = partial(estimate_density_trace, points=points, kernel=kernel, bandwidth=bandwidth)
    return [
        [
            kde(samples_trace, weights=weights)
            for samples_trace, weights in zip_strict(samples_row, weights_row)
        ]
        for samples_row, weights_row in zip_strict(samples, normalised_weights)
    ]
