from __future__ import annotations

import re
from typing import TYPE_CHECKING

import numpy as np
import pytest

from ridgeplot._hist import (
    bin_samples,
    bin_trace_samples,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

NON_FINITE_VALUES = [np.inf, -np.inf, np.nan]

# ==============================================================
# ---  bin_trace_samples()
# ==============================================================


# --- Basic functionality ---


@pytest.mark.parametrize(
    ("samples", "nbins", "expected"),
    [
        # Basic case with repeated values
        # NOTE: The expected x values correspond to the centers of
        #       equally spaced bins over the range [min, max] of the
        #       samples. This can be counterintuitive for count data,
        #       as the bins do not align with the integer sample values.
        ([1, 2, 2, 3, 4], 4, [(1.375, 1), (2.125, 2), (2.875, 1), (3.625, 1)]),
        # Single bin aggregates all samples
        ([1, 2, 3], 1, [(2.0, 3)]),
        # Uniform distribution
        ([0, 1, 2, 3], 4, [(0.375, 1), (1.125, 1), (1.875, 1), (2.625, 1)]),
        # All identical samples fall in the rightmost bin
        # (NumPy pads the zero-width range by +/-0.5)
        ([3, 3, 3], 2, [(2.75, 0), (3.25, 3)]),
        # Negative values
        ([-2, -1, 0, 1], 2, [(-1.25, 2), (0.25, 2)]),
    ],
    ids=["basic", "single_bin", "uniform", "identical", "negative"],
)
def test_basic_binning(
    samples: list[float], nbins: int, expected: list[tuple[float, float]]
) -> None:
    result = bin_trace_samples(samples, nbins=nbins)
    assert result == expected


def test_float_samples_binning() -> None:
    result = bin_trace_samples([0.1, 0.5, 0.9], nbins=3)
    x_vals, y_vals = zip(*result, strict=True)
    assert x_vals == pytest.approx((7 / 30, 0.5, 23 / 30))
    assert y_vals == (1.0, 1.0, 1.0)


@pytest.mark.parametrize("nbins", [1, 2, 5, 10, 50])
def test_output_length_matches_nbins(nbins: int) -> None:
    result = bin_trace_samples([1, 2, 3, 4, 5], nbins=nbins)
    assert len(result) == nbins


@pytest.mark.parametrize(
    "input_type",
    [list, tuple, np.asarray],
    ids=["list", "tuple", "ndarray"],
)
def test_accepts_various_input_types(input_type: Callable[[list[int]], Any]) -> None:
    result = bin_trace_samples(input_type([1, 2, 3]), nbins=2)
    assert len(result) == 2
    # The output should always be normalised to built-in floats
    # (note: isinstance() checks wouldn't cut it here since
    #  np.float64 is also a subclass of the built-in float)
    assert {type(value) for xy_pair in result for value in xy_pair} == {float}


def test_counts_sum_to_sample_size() -> None:
    samples = list(range(100))
    result = bin_trace_samples(samples, nbins=7)
    total_count = sum(y for _, y in result)
    assert total_count == len(samples)


def test_bin_centers_within_data_range() -> None:
    # NOTE: This property does not hold for the degenerate case where all
    #       samples are identical, since NumPy pads the zero-width range by
    #       +/-0.5 and a bin center can then fall outside the data range
    #       (e.g., [3, 3, 3] with nbins=2 produces a center at 2.75 < 3).
    samples = [10, 20, 30, 40, 50]
    result = bin_trace_samples(samples, nbins=5)
    centers = [x for x, _ in result]
    assert all(min(samples) <= c <= max(samples) for c in centers)


def test_single_sample_falls_in_middle_bin() -> None:
    """A single sample gets NumPy's +/-0.5 range padding, placing all of the
    mass in the middle bin (unlike the all-identical case, where the mass
    falls in the rightmost bin)."""
    result = bin_trace_samples([5], nbins=3)
    x_vals, y_vals = zip(*result, strict=True)
    assert x_vals == pytest.approx((14 / 3, 5.0, 16 / 3))
    assert y_vals == (0.0, 1.0, 0.0)


# --- Weights ---


@pytest.mark.parametrize(
    ("samples", "weights", "nbins", "expected_counts"),
    [
        # Each sample falls in its own bin, so the weights become the counts
        ([1, 2, 3], [10, 1, 1], 3, [10, 1, 1]),
        # Zero weights effectively exclude samples
        ([1, 2, 3], [1, 0, 1], 3, [1, 0, 1]),
        # Fractional weights
        ([1, 2], [0.5, 1.5], 2, [0.5, 1.5]),
    ],
    ids=["heavy_first", "zero_weight", "fractional"],
)
def test_weights_affect_counts(
    samples: list[float],
    weights: list[float],
    nbins: int,
    expected_counts: list[float],
) -> None:
    result = bin_trace_samples(samples, nbins=nbins, weights=weights)
    counts = [y for _, y in result]
    assert counts == pytest.approx(expected_counts)


def test_weighted_counts_sum_to_weight_sum() -> None:
    samples = [1, 2, 3, 4, 5]
    weights = [2.0, 3.0, 1.5, 0.5, 4.0]
    result = bin_trace_samples(samples, nbins=3, weights=weights)
    assert sum(y for _, y in result) == pytest.approx(sum(weights))


# --- Error handling ---


def test_rejects_empty_samples() -> None:
    with pytest.raises(ValueError, match="samples array should not be empty"):
        bin_trace_samples([], nbins=3)


@pytest.mark.parametrize("non_finite", NON_FINITE_VALUES)
def test_rejects_non_finite_samples(non_finite: float) -> None:
    with pytest.raises(ValueError, match="samples array should not contain any infs or NaNs"):
        bin_trace_samples([1, 2, non_finite], nbins=2)


@pytest.mark.parametrize("non_finite", NON_FINITE_VALUES)
def test_rejects_non_finite_weights(non_finite: float) -> None:
    with pytest.raises(ValueError, match="weights array should not contain any infs or NaNs"):
        bin_trace_samples([1, 2, 3], nbins=2, weights=[1, non_finite, 1])


@pytest.mark.parametrize(
    ("samples", "weights"),
    [
        ([1, 2, 3], [1, 2]),
        ([1, 2], [1, 2, 3]),
        ([1], []),
    ],
    ids=["weights_short", "weights_long", "empty_weights"],
)
def test_rejects_mismatched_weights_length(samples: list[float], weights: list[float]) -> None:
    with pytest.raises(ValueError, match="weights array should have the same length"):
        bin_trace_samples(samples, nbins=2, weights=weights)


def test_rejects_negative_weights() -> None:
    with pytest.raises(ValueError, match="weights array should not contain negative values"):
        bin_trace_samples([1, 2, 3], nbins=2, weights=[-1, 1, 1])


def test_rejects_all_zero_weights() -> None:
    with pytest.raises(ValueError, match="weights array should not be all zeros"):
        bin_trace_samples([1, 2, 3], nbins=2, weights=[0, 0, 0])


# ==============================================================
# ---  bin_samples()
# ==============================================================


def test_bin_samples() -> None:
    samples = [1, 2, 2, 3, 4]
    expected_trace = [(1.375, 1.0), (2.125, 2.0), (2.875, 1.0), (3.625, 1.0)]
    densities = bin_samples(samples=[[samples], [samples]], nbins=4)
    assert densities == [[expected_trace], [expected_trace]]


def test_bin_samples_preserves_shape() -> None:
    densities = bin_samples(samples=[[[0, 1], [2, 3, 4]], [[5, 6, 7, 8]]], nbins=3)
    assert [len(row) for row in densities] == [2, 1]
    assert all(len(trace) == 3 for row in densities for trace in row)


def test_bin_samples_broadcasts_flat_weights() -> None:
    """A single flat weights vector should be applied to all traces."""
    trace_a, trace_b = [1, 2, 3], [4, 5, 6]
    weights = [1, 2, 3]
    densities = bin_samples(samples=[[trace_a, trace_b]], nbins=2, sample_weights=weights)
    assert densities == [
        [
            bin_trace_samples(trace_a, nbins=2, weights=weights),
            bin_trace_samples(trace_b, nbins=2, weights=weights),
        ]
    ]


def test_bin_samples_per_row_weights() -> None:
    """Shallow weights (one entry per row) should be matched to each row."""
    trace_a, trace_b = [1, 2, 3], [4, 5, 6, 7]
    weights_a = [1, 2, 3]
    densities = bin_samples(
        samples=[[trace_a], [trace_b]],
        nbins=2,
        sample_weights=[weights_a, None],
    )
    assert densities == [
        [bin_trace_samples(trace_a, nbins=2, weights=weights_a)],
        [bin_trace_samples(trace_b, nbins=2)],
    ]


def test_bin_samples_per_row_weights_broadcast_to_all_traces_in_row() -> None:
    """Shallow weights are per-row, *not* per-trace: each entry should be
    broadcast to all traces in the corresponding row."""
    trace_a, trace_b, trace_c = [1, 2, 3], [4, 5, 6], [7, 8, 9, 10]
    weights_row_1 = [1, 2, 3]
    densities = bin_samples(
        samples=[[trace_a, trace_b], [trace_c]],
        nbins=2,
        sample_weights=[weights_row_1, None],
    )
    assert densities == [
        [
            bin_trace_samples(trace_a, nbins=2, weights=weights_row_1),
            bin_trace_samples(trace_b, nbins=2, weights=weights_row_1),
        ],
        [bin_trace_samples(trace_c, nbins=2)],
    ]


def test_bin_samples_rejects_shallow_weights_row_count_mismatch() -> None:
    """Shallow weights should have exactly one entry per row."""
    with pytest.raises(
        ValueError,
        match=re.escape("Mismatch between number of rows in attrs (1) and samples/densities (2)."),
    ):
        bin_samples(samples=[[[1, 2]], [[3, 4]]], nbins=2, sample_weights=[[1, 2]])


def test_bin_samples_flat_weights_fail_for_ragged_traces() -> None:
    """A flat weights vector is broadcast to all traces, so it should fail
    (with a helpful error message) when traces have different lengths."""
    err_msg = (
        "The weights array should have the same length as the samples array "
        "(got 3 weights for 4 samples). Note that a single flat array of "
        "weights is broadcast to all traces in the samples array."
    )
    with pytest.raises(ValueError, match=re.escape(err_msg)):
        bin_samples(samples=[[[1, 2, 3], [4, 5, 6, 7]]], nbins=2, sample_weights=[1, 2, 3])
