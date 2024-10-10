from __future__ import annotations

import re
from typing import TYPE_CHECKING

import numpy as np
import pytest

from ridgeplot._kde import (
    KDEPoints,
    _validate_densities,
    estimate_densities,
    estimate_density_trace,
)

if TYPE_CHECKING:
    from typing import Any

    import numpy.typing as npt

# ==============================================================
# ---  estimate_density_trace()
# ==============================================================


def test_estimate_density_trace_simple() -> None:
    density_trace = estimate_density_trace(
        trace_samples=[0, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6],
        points=7,
        kernel="gau",
        bandwidth="normal_reference",
    )
    x, y = zip(*density_trace)
    assert x == tuple(range(7))
    assert np.argmax(y) == 3


def test_estimate_density_trace_points() -> None:
    points = [-20, -1, 1, 3, 5, 7, 8]
    density_trace = estimate_density_trace(
        trace_samples=[0, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6],
        points=points,
        kernel="gau",
        bandwidth="normal_reference",
    )
    x, y = zip(*density_trace)
    assert x == tuple(points)
    assert np.argmax(y) == 3
    assert np.argmin(y) == 0


@pytest.mark.parametrize("non_finite_value", [np.inf, np.nan, float("inf"), float("nan")])
def test_estimate_density_trace_fails_for_non_finite_values(non_finite_value: float) -> None:
    err_msg = "The samples array should not contain any infs or NaNs."
    with pytest.raises(ValueError, match=err_msg):
        estimate_density_trace(
            trace_samples=[0, 1, 2, 2, 3, 3, 3, 4, 4, 5, non_finite_value],
            points=7,
            kernel="gau",
            bandwidth="normal_reference",
        )


@pytest.mark.parametrize("points", [[[0, 1, 2, 3]], np.asarray([0, 1, 2, 3]).reshape(2, 2)])
def test_estimate_density_trace_fails_for_non_1d_points(points: KDEPoints) -> None:
    err_msg = (
        "The 'points' at which KDE is computed should be represented by a one-dimensional array"
    )
    with pytest.raises(ValueError, match=err_msg):
        estimate_density_trace(
            trace_samples=[0, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6],
            points=points,
            kernel="gau",
            bandwidth="normal_reference",
        )


# ==============================================================
# ---  _validate_densities()
# ==============================================================


def test__validate_densities() -> None:
    """Test that _validate_densities() does not raise an exception for valid
    inputs."""
    x = np.array([0, 1, 2, 3, 4, 5, 6])
    y = np.array([0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1])
    _validate_densities(x=x, y=y, kernel="doesn't matter")


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (np.array([0, 1, 2, 3]), 2),
        (np.array([0, 1, 2, 3]), np.array([0.1, 0.2, 0.3])),
        (np.array([0, 1, 2, 3]), np.array([0.1, 0.2, 0.3, np.nan])),
    ],
    ids=["wrong_type", "wrong_shape", "not_finite"],
)
def test__validate_densities_raises_runtime_error(
    x: npt.NDArray[np.floating[Any]], y: npt.NDArray[np.floating[Any]]
) -> None:
    """Test that _validate_densities() raises a RuntimeError for invalid inputs."""
    msg = (
        "statsmodels failed to evaluate densities using the 'dummy' kernel. "
        "Try setting kernel='gau' (the default kernel)."
    )
    with pytest.raises(RuntimeError, match=re.escape(msg)):
        _validate_densities(x=x, y=y, kernel="dummy")


# ==============================================================
# ---  estimate_densities()
# ==============================================================


def test_estimate_densities() -> None:
    densities = estimate_densities(
        samples=[[[0, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6]], [[0, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6]]],
        points=7,
        kernel="gau",
        bandwidth="normal_reference",
    )
    assert len(densities) == 2
    for densities_row in densities:
        assert len(densities_row) == 1
        density_trace = next(iter(densities_row))
        x, y = zip(*density_trace)
        assert x == tuple(range(7))
        assert np.argmax(y) == 3
