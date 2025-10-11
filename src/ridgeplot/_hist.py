"""Utilities for binning samples into histograms."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ridgeplot._kde import normalize_sample_weights

if TYPE_CHECKING:
    from ridgeplot._types import (
        Densities,
        DensityTrace,
        Samples,
        SamplesTrace,
        SampleWeights,
        SampleWeightsArray,
        ShallowSampleWeightsArray,
    )


def bin_trace_samples(
    trace_samples: SamplesTrace,
    nbins: int,
    weights: SampleWeights = None,
) -> DensityTrace:
    trace_samples = np.asarray(trace_samples, dtype=float)
    if not np.isfinite(trace_samples).all():
        raise ValueError("The samples array should not contain any infs or NaNs.")
    if weights is not None:
        weights = np.asarray(weights, dtype=float)
        if len(weights) != len(trace_samples):
            raise ValueError("The weights array should have the same length as the samples array.")
        if not np.isfinite(weights).all():
            raise ValueError("The weights array should not contain any infs or NaNs.")
    hist, bins = np.histogram(trace_samples, bins=nbins, weights=weights)
    return [(float(x), float(y)) for x, y in zip(bins, hist)]


def bin_samples(
    samples: Samples,
    nbins: int,
    sample_weights: SampleWeightsArray | ShallowSampleWeightsArray | SampleWeights = None,
) -> Densities:
    normalised_weights = normalize_sample_weights(sample_weights=sample_weights, samples=samples)
    return [
        [
            bin_trace_samples(trace_samples, nbins=nbins, weights=weights)
            for trace_samples, weights in zip(samples_row, weights_row, strict=True)
        ]
        for samples_row, weights_row in zip(samples, normalised_weights, strict=True)
    ]
