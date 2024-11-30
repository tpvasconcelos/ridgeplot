from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ridgeplot._kde import normalize_sample_weights
from ridgeplot._vendor.more_itertools import zip_strict

if TYPE_CHECKING:

    from ridgeplot._types import (
        Densities,
        Float,
        Samples,
        SamplesTrace,
        SampleWeights,
        SampleWeightsArray,
        ShallowSampleWeightsArray,
        XYCoordinate,
    )


def bin_trace_samples(
    trace_samples: SamplesTrace,
    nbins: int,
    weights: SampleWeights,
) -> list[XYCoordinate[Float]]:
    hist, bins = np.histogram(
        np.asarray(trace_samples, dtype=float),
        bins=nbins,
        weights=np.asarray(weights, dtype=float) if weights is not None else None,
    )
    return list(zip(bins[:-1], hist))


def bin_samples(
    samples: Samples,
    nbins: int,
    sample_weights: SampleWeightsArray | ShallowSampleWeightsArray | SampleWeights = None,
) -> Densities:
    normalised_weights = normalize_sample_weights(sample_weights=sample_weights, samples=samples)
    return [
        [
            bin_trace_samples(trace_samples, nbins=nbins, weights=weights)
            for trace_samples, weights in zip_strict(samples_row, weights_row)
        ]
        for samples_row, weights_row in zip_strict(samples, normalised_weights)
    ]
