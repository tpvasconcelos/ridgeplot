from __future__ import annotations

import numpy as np
import pytest

from ridgeplot._hist import (
    bin_samples,
    bin_trace_samples,
)

# Example data

SAMPLES_IN = [1, 2, 2, 3, 4]
NBINS = 4
DENSITIES_OUT = [(1.0, 1.0), (1.75, 2.0), (2.5, 1.0), (3.25, 1.0)]
X_OUT, Y_OUT = zip(*DENSITIES_OUT)

WEIGHTS = [1, 1, 1, 1, 9]

# ==============================================================
# ---  estimate_density_trace()
# ==============================================================


def test_bin_trace_samples_simple() -> None:
    density_trace = bin_trace_samples(trace_samples=SAMPLES_IN, nbins=NBINS)
    x, y = zip(*density_trace)
    assert x == X_OUT
    assert y == Y_OUT


@pytest.mark.parametrize("nbins", [2, 5, 8, 11])
def test_bin_trace_samples_nbins(nbins: int) -> None:
    density_trace = bin_trace_samples(trace_samples=SAMPLES_IN, nbins=nbins)
    assert len(density_trace) == nbins


@pytest.mark.parametrize("non_finite_value", [np.inf, np.nan, float("inf"), float("nan")])
def test_bin_trace_samples_fails_for_non_finite_values(non_finite_value: float) -> None:
    err_msg = "The samples array should not contain any infs or NaNs."
    with pytest.raises(ValueError, match=err_msg):
        bin_trace_samples(trace_samples=[*SAMPLES_IN[:-1], non_finite_value], nbins=NBINS)


def test_bin_trace_samples_weights() -> None:
    density_trace = bin_trace_samples(
        trace_samples=SAMPLES_IN,
        nbins=NBINS,
        weights=WEIGHTS,
    )
    x, y = zip(*density_trace)
    assert x == X_OUT
    assert np.argmax(y) == len(y) - 1


def test_bin_trace_samples_weights_not_same_length() -> None:
    with pytest.raises(
        ValueError, match="The weights array should have the same length as the samples array"
    ):
        bin_trace_samples(trace_samples=SAMPLES_IN, nbins=NBINS, weights=[1, 1, 1])


@pytest.mark.parametrize("non_finite_value", [np.inf, np.nan, float("inf"), float("nan")])
def test_bin_trace_samples_weights_fails_for_non_finite_values(
    non_finite_value: float,
) -> None:
    err_msg = "The weights array should not contain any infs or NaNs."
    with pytest.raises(ValueError, match=err_msg):
        bin_trace_samples(
            trace_samples=SAMPLES_IN,
            nbins=NBINS,
            weights=[*WEIGHTS[:-1], non_finite_value],
        )


# ==============================================================
# ---  estimate_densities()
# ==============================================================


def test_bin_samples() -> None:
    densities = bin_samples(
        samples=[[SAMPLES_IN], [SAMPLES_IN]],
        nbins=NBINS,
    )
    assert len(densities) == 2
    for densities_row in densities:
        assert len(densities_row) == 1
        density_trace = next(iter(densities_row))
        x, y = zip(*density_trace)
        assert x == X_OUT
        assert y == Y_OUT
