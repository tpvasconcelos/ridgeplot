import json

from plotly.colors import (
    DEFAULT_PLOTLY_COLORS,
    PLOTLY_SCALES,
    hex_to_rgb,
    label_rgb,
    make_colorscale,
    validate_colorscale,
)
from plotly.express.colors import sequential

# noinspection PyProtectedMember
from ridgeplot._colors import _PATH_TO_COLORS_JSON

# start off by getting all named color-scales defined in PLOTLY_SCALES
all_colorscales_raw = PLOTLY_SCALES.copy()

# turn plotly's default colors into the default color-scale
all_colorscales_raw["default"] = make_colorscale(DEFAULT_PLOTLY_COLORS)

# add all sequential color-scales
for name, color_list in vars(sequential).items():
    if name.startswith("_") or name.startswith("swatches"):
        continue
    all_colorscales_raw[name] = make_colorscale(color_list)

all_colorscales_clean = {}
for name, colorscale in all_colorscales_raw.items():
    # convert all color-scales to 'rgb(r, g, b)' format
    if colorscale[0][1].startswith("#"):
        colorscale = [[s, label_rgb(hex_to_rgb(c))] for s, c in colorscale]
    # validate the color-scale as a sanity check and
    # use lower-case convention for all color-scales
    validate_colorscale(colorscale)
    all_colorscales_clean[name.lower()] = colorscale

with _PATH_TO_COLORS_JSON.open(mode="w") as _colors_json:
    json.dump(all_colorscales_clean, _colors_json, indent=2)
