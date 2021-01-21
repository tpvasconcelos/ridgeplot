# Ridgeplot

Simple API for plotting beautiful [ridgeline plots](https://www.data-to-viz.com/graph/ridgeline.html) in
Python using the [Plotly](https://plotly.com/python/) interactive graphing library.

```python
from numpy.random import normal
from ridgeplot import ridgeplot

fig = ridgeplot(samples=[normal(l, size=99) for l in range(5)])
fig.show()
```

## Alternatives

- [`plotly` - from examples/galery](https://plotly.com/python/violin/#ridgeline-plot)
- [`seaborn` - from examples/galery](https://seaborn.pydata.org/examples/kde_ridgeplot)
- [`bokeh` - from examples/galery](https://docs.bokeh.org/en/latest/docs/gallery/ridgeplot.html)
- [`matplotlib` - from blogpost](https://matplotlib.org/matplotblog/posts/create-ridgeplots-in-matplotlib/)
- [`joypy` - Ridgeplot library using a `matplotlib` backend](https://github.com/sbebo/joypy)

