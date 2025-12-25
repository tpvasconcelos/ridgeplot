"""ridgeplot: beautiful ridgeline plots in Python

ridgeplot is a Python package that provides a simple interface for plotting
beautiful and interactive ridgeline plots within the extensive Plotly ecosystem.

Take a look at the getting started guide, which provides a quick introduction
to the ridgeplot library: https://ridgeplot.readthedocs.io/en/stable/getting_started/getting_started.html

The full official documentation can be found at: https://ridgeplot.readthedocs.io/en/stable/

For those in a hurry, here's a very basic example on how to quickly get started
with the `ridgeplot()` function.

    import numpy as np
    from ridgeplot import ridgeplot

    my_samples = [np.random.normal(n, size=900) for n in range(6, 0, -2)]
    fig = ridgeplot(samples=my_samples)
    fig.show()

"""

from __future__ import annotations

from ridgeplot._color.colorscale import list_all_colorscale_names
from ridgeplot._ridgeplot import ridgeplot
from ridgeplot._version import __version__

__all__ = [
    "__version__",
    "list_all_colorscale_names",
    "ridgeplot",
]
