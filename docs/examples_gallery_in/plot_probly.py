"""
probly dataset
=================

In this example, we will be replicating the first ridgeline plot example in
`this _from Data to Viz_ post <https://www.data-to-viz.com/graph/ridgeline.html>`_
, which uses the _probly_ dataset. You can find the _plobly_ dataset on
multiple sources like in the
`bokeh <https://raw.githubusercontent.com/bokeh/bokeh/main/bokeh/sampledata/_data/probly.csv>`_
python interactive visualization library. I'll be using the
`same source <https://raw.githubusercontent.com/zonination/perceptions/master/probly.csv>`_
used in the original post.
"""

from __future__ import annotations

import numpy as np
import plotly.io as pio

from ridgeplot import ridgeplot
from ridgeplot.datasets import load_probly

# Load the probly dataset
df = load_probly()

# %%
# Let's grab only the subset of columns displayed in the example
column_names = [
    "Almost Certainly",
    "Very Good Chance",
    "We Believe",
    "Likely",
    "About Even",
    "Little Chance",
    "Chances Are Slight",
    "Almost No Chance",
]
df = df[column_names]

# %%
# Not only does 'ridgeplot(...)' come configured with sensible defaults
# but is also fully configurable to your own style and preference!

fig = ridgeplot(
    # Get your samples in the correct format
    samples=df.to_numpy().T,
    # We can specify the bandwidth used for KDE
    bandwidth=4,
    # and the range of points for which the KDE is evaluated
    kde_points=np.linspace(-12.5, 112.5, 400),
    # You can pass any plotly color scale here
    colorscale="viridis",
    # In the example, the distributions seem to be colored
    # by 'index'. Have a look at the other available options!
    colormode="index",
    # Set the transparency level
    coloralpha=0.6,
    # Always label your plots! Don't be evil...
    labels=column_names,
    # Adjust the vertical spacing between the distributions
    spacing=5 / 9,
)

# %%
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

# Or, simply: fig.show()
pio.show(fig)
