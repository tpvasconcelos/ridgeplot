"""ridgeplot: beautiful ridgeline plots in Python

The ridgeplot python library aims at providing a simple API for plotting
beautiful ridgeline plots within the extensive Plotly interactive graphing
environment.


  Simple example:

  from numpy.random import normal
  from ridgeplot import ridgeplot

  # Put your real samples here...
  synthetic_samples = [normal(n / 1.2, size=600) for n in reversed(range(9))]

  # The `ridgeplot()` helper comes packed with sensible defaults
  fig = ridgeplot(samples=synthetic_samples)

  # and the returned Plotly figure is still fully customizable
  fig.update_layout(height=500, width=800)

  # show us the work!!
  fig.show()

"""
from ridgeplot._colors import named_colorscales
from ridgeplot._ridgeplot import ridgeplot
from ridgeplot._version import __version__

__all__ = ["ridgeplot", "named_colorscales", "__version__"]
