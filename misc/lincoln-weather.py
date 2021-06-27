import numpy as np
import pandas as pd

from ridgeplot import ridgeplot

# ---
df = pd.read_csv(
    "https://raw.githubusercontent.com/wilkelab/ggridges/master/data-raw/lincoln-weather.csv",
    index_col="CST",
    parse_dates=True,
)
series = df["Mean Temperature [F]"]
series.index = series.index.month_name()

# ---

months = list(series.index.unique())
samples = [series[month].values for month in months]

# ---


# ---
kde_points = np.linspace(-12.5, 95, 400)

# ---
fig = ridgeplot(
    samples=samples,
    labels=months,
    colorscale="inferno",
    colormode="mean-minmax",
    coloralpha=None,
    bandwidth=3.5,
    kde_points=kde_points,
    spacing=0.33,
    linewidth=1.8,
)

# ---
fig.update_layout(
    title="Temperatures in Lincoln NU in 2016",
    height=600,
    width=1000,
    plot_bgcolor="rgba(255, 255, 255, 0.0)",
    xaxis_gridcolor="rgba(0, 0, 0, 0.1)",
    yaxis_gridcolor="rgba(0, 0, 0, 0.1)",
    yaxis_title="Month",
    xaxis_title="Mean Temperature [F]",
)

# ---
fig.show()
