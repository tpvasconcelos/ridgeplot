from numbers import Number
from typing import List, Union

from plotly.colors import find_intermediate_color, hex_to_rgb, label_rgb

from ridgeplot._all_colors_dict import ALL_PLOTLY_COLORS_SCALES

# Ideally: ColorScaleType = List[Tuple[Number, str]]
from ridgeplot._utils import normalise

ColorScaleType = List[List[Union[Number, str]]]


def any_to_rgb(color: Union[tuple, str]) -> str:
    if isinstance(color, tuple):
        color = label_rgb(color)
    if color.startswith("#"):
        color = label_rgb(hex_to_rgb(color))
    if not color.startswith("rgb("):
        raise RuntimeError("Something went wrong with the logic above!")
    return color


def get_plotly_colorscale(name: str) -> ColorScaleType:
    """Helper to get a known Plotly colorscale, raising a ValueError if an
    invalid name is provided."""
    if name not in ALL_PLOTLY_COLORS_SCALES:
        raise ValueError(
            f"Could not find colorscale '{name}'. The available colorscale"
            f" names are {tuple(ALL_PLOTLY_COLORS_SCALES.keys())}."
        )
    return ALL_PLOTLY_COLORS_SCALES[name]


def get_color(colorscale: ColorScaleType, midpoint: float) -> str:
    """Given a colorscale, it interpolates the expected color at a given
    midpoint, on a scale from 0 to 1."""
    if 0 > midpoint > 1:
        raise ValueError(f"The 'midpoint' should be a float value between 0 and 1, not {midpoint}.")
    scale = [s for s, _ in colorscale]
    colors = [any_to_rgb(c) for _, c in colorscale]
    del colorscale
    if midpoint in scale:
        return colors[scale.index(midpoint)]
    ceil = min(filter(lambda s: s > midpoint, scale))
    floor = max(filter(lambda s: s < midpoint, scale))
    midpoint_normalised = normalise(midpoint, min_=floor, max_=ceil)
    color = find_intermediate_color(
        lowcolor=colors[scale.index(floor)],
        highcolor=colors[scale.index(ceil)],
        intermed=midpoint_normalised,
        colortype="rgb",
    )
    return color


def apply_alpha(color: Union[tuple, str], alpha) -> str:
    color = any_to_rgb(color)
    return f"rgba({color[4:-1]}, {alpha})"
