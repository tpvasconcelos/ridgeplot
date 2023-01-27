<p align="center">
    <img src="docs/_static/img/logo-wide.png" alt="ridgeplot - beautiful ridgeline plots in Python">
</p>

<h1 id="ridgeplot" align="center">
    ridgeplot: beautiful ridgeline plots in Python
</h1>

<p align="center">
  <!-- TODO: https://bestpractices.coreinfrastructure.org/en -->
  <!-- TODO: https://www.gitpod.io/docs/getting-started -->
  <a href="https://pypi.org/project/ridgeplot/"><img src="https://img.shields.io/pypi/v/ridgeplot" alt="PyPI - Latest Release"></a>
  <a href="https://github.com/tpvasconcelos/ridgeplot/"><img src="https://img.shields.io/pypi/pyversions/ridgeplot" alt="PyPI - Python Versions"></a>
  <a href="https://pypi.org/project/ridgeplot/"><img src="https://img.shields.io/pypi/status/ridgeplot.svg" alt="PyPI - Package Status"></a>
  <a href="https://github.com/tpvasconcelos/ridgeplot/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/ridgeplot" alt="PyPI - License"></a>
  <br>
  <a href="https://github.com/tpvasconcelos/ridgeplot/actions/workflows/ci.yaml/"><img src="https://github.com/tpvasconcelos/ridgeplot/actions/workflows/ci.yaml/badge.svg" alt="GitHub CI"></a>
  <a href="https://ridgeplot.readthedocs.io/en/latest/"><img src="https://readthedocs.org/projects/ridgeplot/badge/?version=latest&style=flat" alt="Docs"></a>
  <a href="https://codecov.io/gh/tpvasconcelos/ridgeplot"><img src="https://codecov.io/gh/tpvasconcelos/ridgeplot/branch/main/graph/badge.svg" alt="codecov"></a>
  <a href="https://www.codefactor.io/repository/github/tpvasconcelos/ridgeplot"><img src="https://www.codefactor.io/repository/github/tpvasconcelos/ridgeplot/badge" alt="CodeFactor"></a>
  <a href="https://www.codacy.com/gh/tpvasconcelos/ridgeplot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tpvasconcelos/ridgeplot&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/e21652ac49874b6f94ed3c9b7ac77021" alt="Codacy code quality"/></a>
</p>

<!-- <p align="center"><i>Beautiful ridgeline plots in python</i></p> -->

______________________________________________________________________

The `ridgeplot` python library aims at providing a simple API for plotting beautiful
[ridgeline plots](https://www.data-to-viz.com/graph/ridgeline.html) within the extensive
[Plotly](https://plotly.com/python/) interactive graphing environment.

Bumper stickers:

- Do one thing, and do it well!
- Use sensible defaults, but allow for extensive configuration!

## How to get it?

The source code is currently hosted on GitHub at: <https://github.com/tpvasconcelos/ridgeplot>

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```shell
pip install -U ridgeplot
```

### Dependencies

- [plotly](https://plotly.com/) - the interactive graphing backend that powers `ridgeplot`
- [statsmodels](https://www.statsmodels.org/) - Used for Kernel Density Estimation (KDE)
- [numpy](https://numpy.org/) - Supporting library for multi-dimensional array manipulations

## How to use it?

The official docs can be found at: https://ridgeplot.readthedocs.io/en/stable/

### Sensible defaults

```python
import numpy as np

from ridgeplot import ridgeplot

# Put your real samples here...
np.random.seed(0)
synthetic_samples = [np.random.normal(n / 1.2, size=600) for n in range(9, 0, -1)]

# Call the `ridgeplot()` helper, packed with sensible defaults
fig = ridgeplot(samples=synthetic_samples)

# The returned Plotly `Figure` is still fully customizable
fig.update_layout(height=500, width=800)

# show us the work!
fig.show()
```

![ridgeline plot example using the ridgeplot Python library](docs/_static/img/example_simple.png)

### Fully configurable

In this example, we will be replicating the first ridgeline plot example in
[this _from Data to Viz_ post](https://www.data-to-viz.com/graph/ridgeline.html), which uses the
_probly_ dataset. You can find the _plobly_ dataset on multiple sources like in the
[bokeh](https://raw.githubusercontent.com/bokeh/bokeh/17a0b288052afac80ebcf0aa74e3915452fce3ca/src/bokeh/sampledata/_data/probly.csv)
python interactive visualization library. I'll be using the
[same source](https://raw.githubusercontent.com/zonination/perceptions/51207062aa173777264d3acce0131e1e2456d966/probly.csv)
used in the original post.

```python
import numpy as np
from ridgeplot import ridgeplot
from ridgeplot.datasets import load_probly

# Load the probly dataset
df = load_probly()

# Let's grab only the subset of columns displayed in the example
column_names = [
    "Almost Certainly", "Very Good Chance", "We Believe", "Likely",
    "About Even", "Little Chance", "Chances Are Slight", "Almost No Chance",
]  # fmt: skip
df = df[column_names]

# Not only does 'ridgeplot(...)' come configured with sensible defaults
# but is also fully configurable to your own style and preference!
fig = ridgeplot(
    samples=df.values.T,
    bandwidth=4,
    kde_points=np.linspace(-12.5, 112.5, 400),
    colorscale="viridis",
    colormode="index",
    coloralpha=0.6,
    labels=column_names,
    spacing=5 / 9,
)

# Again, update the figure layout to your liking here
fig.update_layout(
    title="What probability would you assign to the phrase <i>“Highly likely”</i>?",
    height=650,
    width=800,
    plot_bgcolor="rgba(255, 255, 255, 0.0)",
    xaxis_gridcolor="rgba(0, 0, 0, 0.1)",
    yaxis_gridcolor="rgba(0, 0, 0, 0.1)",
    yaxis_title="Assigned Probability (%)",
)
fig.show()
```

![ridgeline plot of the probly dataset using the ridgeplot Python library](docs/_static/img/example_probly.png)
