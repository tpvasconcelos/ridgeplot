import numpy as np

from ridgeplot._kde import estimate_densities, estimate_density_trace

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


#


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
        density_trace = tuple(densities_row)[0]
        x, y = zip(*density_trace)
        assert x == tuple(range(7))
        assert np.argmax(y) == 3
