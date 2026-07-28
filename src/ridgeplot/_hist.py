"""Utilities for binning samples into histograms."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ridgeplot._kde import normalize_sample_weights, validate_trace_samples_and_weights

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
    samples_array, weights_array = validate_trace_samples_and_weights(trace_samples, weights)
    hist_counts, hist_edges = np.histogram(samples_array, bins=nbins, weights=weights_array)
    bin_centers = 0.5 * (hist_edges[:-1] + hist_edges[1:])
    return [(float(x), float(y)) for x, y in zip(bin_centers, hist_counts, strict=True)]


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
