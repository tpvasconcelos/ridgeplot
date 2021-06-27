from typing import Tuple

import numpy as np
import statsmodels.api as sm


def evaluate_density(samples, points, kernel, bandwidth) -> Tuple[np.ndarray, np.ndarray]:
    """For a given dataset, computes the kernel densities at the given points,
    and returns back the points and density arrays."""

    # By default, we'll use a 'hard' KDE span. That is, we'll
    # evaluate the densities and N equally spaced points
    # over the range [min(samples), max(samples)]
    if isinstance(points, int):
        points = np.linspace(np.min(samples), np.max(samples), points)

    # Unless a specific range is specified...
    else:
        points = np.asarray(points)

    if points.ndim > 1:
        raise ValueError(
            f"The 'points' at which KDE is computed should be represented by a "
            f"one-dimensional array, got an array of shape {points.shape} instead."
        )

    # I decided to use statsmodels' KDEUnivariate for KDE. There are many
    # other supported alternatives in the python scientific computing
    # ecosystem. See, for instance, scipy's alternative - on which
    # statsmodels relies - `from scipy.stats import gaussian_kde`
    dens = sm.nonparametric.KDEUnivariate(samples)

    # I'm hard-coding the `fft=self.kernel == "gau"` for convenience here.
    # This avoids the need to expose yet another __init__ argument (fft)
    # to this class. The drawback is that, if and when statsmodels
    # implements another kernel with fft, this will fallback to
    # using the unoptimised version (with fft = False).
    dens.fit(kernel=kernel, fft=kernel == "gau", bw=bandwidth)
    densities = dens.evaluate(points)

    # I haven't investigated the root of this issue yet
    # but statsmodels' KDEUnivariate implementation
    # can return a nan float if something goes
    # wrong internally. As to avoid confusion
    # further down the pipeline, I decided
    # to check whether the correct object
    # (and shape) are being returned.
    if not isinstance(densities, np.ndarray) or densities.shape != points.shape:
        raise RuntimeError(
            f"Could now evaluate densities using the {repr(kernel)} kernel! " f"Try using kernel='gau' (default)."
        )

    return points, densities


def get_densities(samples, points, kernel, bandwidth) -> np.ndarray:
    return np.asarray([evaluate_density(samples=s, points=points, kernel=kernel, bandwidth=bandwidth) for s in samples])
