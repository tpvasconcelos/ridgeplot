from typing import List, Tuple

import numpy as np


def get_extrema_2d(arr) -> Tuple[float, float]:
    """Calculates and returns the extrema (min, max) of a 2D (N, M) array."""
    arr = np.asarray(arr).flat
    return np.min(arr), np.max(arr)


def get_extrema_3d(arr: List[np.ndarray]) -> Tuple[float, float, float, float]:
    """Calculates and returns the x-y extrema (x_min, x_max, y_min, y_max) of
    a 3D (N, 2, M) array."""
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    for x in arr:
        x_min = min(x_min, np.min(x[0]))
        x_max = max(x_max, np.max(x[0]))
        y_min = min(y_min, np.min(x[1]))
        y_max = max(y_max, np.max(x[1]))
    return x_min, x_max, y_min, y_max


def normalise(val: float, min_: float, max_: float) -> float:
    assert max_ > min_
    return (val - min_) / (max_ - min_)
