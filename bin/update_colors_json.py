#!/usr/bin/env python
from __future__ import annotations

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

from ridgeplot._colors import _PATH_TO_COLORS_JSON


def main() -> None:
    # Start off by getting all named color-scales defined in PLOTLY_SCALES
    all_colorscales_raw = PLOTLY_SCALES.copy()

    # Turn plotly's default colors into the default color-scale
    all_colorscales_raw["default"] = make_colorscale(DEFAULT_PLOTLY_COLORS)

    # Add all sequential color-scales
    for name, color_list in vars(sequential).items():
        if name.startswith(("_", "swatches")):
            continue
        all_colorscales_raw[name] = make_colorscale(color_list)

    all_colorscales_rgb = {}
    for name, colorscale in all_colorscales_raw.items():
        # Convert all color-scales to 'rgb(r, g, b)' format
        if colorscale[0][1].startswith("#"):
            colorscale_rgb = [[s, label_rgb(hex_to_rgb(c))] for s, c in colorscale]
        else:
            colorscale_rgb = colorscale
        validate_colorscale(colorscale_rgb)
        all_colorscales_rgb[name.lower()] = colorscale_rgb

    with _PATH_TO_COLORS_JSON.open(mode="w") as _colors_json:
        json.dump(all_colorscales_rgb, _colors_json, indent=2, sort_keys=True)
        _colors_json.write("\n")


if __name__ == "__main__":
    main()
