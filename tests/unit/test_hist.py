from __future__ import annotations

import numpy as np
import pytest

from ridgeplot._hist import (
    bin_samples,
    bin_trace_samples,
)

# ==============================================================
# ---  bin_trace_samples()
# ==============================================================


# --- Basic functionality ---


@pytest.mark.parametrize(
    ("samples", "nbins", "expected"),
    [
        # Basic case with repeated values
        ([1, 2, 2, 3, 4], 4, [(1.375, 1), (2.125, 2), (2.875, 1), (3.625, 1)]),
        # Single bin aggregates all samples
        ([1, 2, 3], 1, [(2.0, 3)]),
        # Uniform distribution
        ([0, 1, 2, 3], 4, [(0.375, 1), (1.125, 1), (1.875, 1), (2.625, 1)]),
        # All identical samples go to rightmost bin
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
    assert x_vals == pytest.approx((0.233, 0.5, 0.767), rel=1e-2)
    assert y_vals == (1.0, 1.0, 1.0)


@pytest.mark.parametrize("nbins", [1, 2, 5, 10, 50])
def test_output_length_matches_nbins(nbins: int) -> None:
    result = bin_trace_samples([1, 2, 3, 4, 5], nbins=nbins)
    assert len(result) == nbins


@pytest.mark.parametrize(
    "input_type",
    [list, tuple, np.array],
    ids=["list", "tuple", "ndarray"],
)
def test_accepts_various_input_types(input_type: type) -> None:
    samples = input_type([1, 2, 3])
    result = bin_trace_samples(samples, nbins=2)
    assert len(result) == 2
    assert all(isinstance(x, float) and isinstance(y, float) for x, y in result)


def test_counts_sum_to_sample_size() -> None:
    samples = list(range(100))
    result = bin_trace_samples(samples, nbins=7)
    total_count = sum(y for _, y in result)
    assert total_count == len(samples)


def test_bin_centers_within_data_range() -> None:
    samples = [10, 20, 30, 40, 50]
    result = bin_trace_samples(samples, nbins=5)
    centers = [x for x, _ in result]
    assert all(min(samples) <= c <= max(samples) for c in centers)


# --- Weights ---


@pytest.mark.parametrize(
    ("samples", "weights", "nbins", "expected_counts"),
    [
        # Weights shift distribution
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


@pytest.mark.parametrize(
    "non_finite",
    [np.inf, -np.inf, np.nan, float("inf"), float("nan")],
    ids=["inf", "neg_inf", "nan", "float_inf", "float_nan"],
)
def test_rejects_non_finite_samples(non_finite: float) -> None:
    with pytest.raises(ValueError, match="samples array should not contain any infs or NaNs"):
        bin_trace_samples([1, 2, non_finite], nbins=2)


@pytest.mark.parametrize(
    "non_finite",
    [np.inf, -np.inf, np.nan, float("inf"), float("nan")],
    ids=["inf", "neg_inf", "nan", "float_inf", "float_nan"],
)
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


# ==============================================================
# ---  bin_samples()
# ==============================================================


def test_bin_samples() -> None:
    samples = [1, 2, 2, 3, 4]
    nbins = 4
    expected = [(1.375, 1), (2.125, 2), (2.875, 1), (3.625, 1)]
    x_out, y_out = zip(*expected, strict=True)
    densities = bin_samples(samples=[[samples], [samples]], nbins=nbins)
    assert len(densities) == 2
    for densities_row in densities:
        assert len(densities_row) == 1
        density_trace = next(iter(densities_row))
        x, y = zip(*density_trace, strict=True)
        assert x == x_out
        assert y == y_out
