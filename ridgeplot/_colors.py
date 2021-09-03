import json
from pathlib import Path
from typing import Dict, List, Tuple, Union

from _plotly_utils.colors import validate_colors, validate_scale_values
from plotly.colors import find_intermediate_color, hex_to_rgb, label_rgb

from ridgeplot._utils import LazyMapping, normalise
from ridgeplot.exceptions import InvalidColorscaleError

ColorScaleType = List[Tuple[float, str]]
ColorScaleMappingType = Dict[str, ColorScaleType]

_path_to_colors_dict = Path(__file__).parent.joinpath("colors.json")


def _colormap_loader() -> ColorScaleMappingType:
    colors: dict = json.loads(_path_to_colors_dict.read_text())
    for name, colorscale in colors.items():
        colors[name] = [tuple(entry) for entry in colorscale]
    return colors


PLOTLY_COLORSCALES = LazyMapping(loader=_colormap_loader)


def validate_colorscale(colorscale: ColorScaleType) -> None:
    """Validate the structure, scale values, and colors of colorscale.

    Adapted from ``_plotly_utils.colors.validate_colorscale``, changing the
    requirement that a colorscale must be a list of tuples instead of a list of
    lists.
    """
    if not isinstance(colorscale, list):
        raise InvalidColorscaleError("A valid colorscale must be a list.")
    if not all(isinstance(inner_tuple, tuple) for inner_tuple in colorscale):
        raise InvalidColorscaleError("A valid colorscale must be a list.")
    scale, colors = zip(*colorscale)
    validate_scale_values(scale=scale)
    validate_colors(colors=colors)


def _any_to_rgb(color: Union[tuple, str]) -> str:
    c: str = label_rgb(color) if isinstance(color, tuple) else color
    if c.startswith("#"):
        c = label_rgb(hex_to_rgb(c))
    if not c.startswith("rgb("):
        raise RuntimeError("Something went wrong with the logic above!")
    return c


def get_plotly_colorscale(name: str) -> ColorScaleType:
    """Helper to get a known Plotly colorscale, raising a ValueError if an
    invalid name is provided."""
    if name not in PLOTLY_COLORSCALES:
        raise ValueError(
            f"Could not find colorscale '{name}'. The available colorscale"
            f" names are {tuple(PLOTLY_COLORSCALES.keys())}."
        )
    return PLOTLY_COLORSCALES[name]


def get_color(colorscale: ColorScaleType, midpoint: float) -> str:
    """Given a colorscale, it interpolates the expected color at a given
    midpoint, on a scale from 0 to 1."""
    if 0 > midpoint > 1:
        raise ValueError(f"The 'midpoint' should be a float value between 0 and 1, not {midpoint}.")
    scale = [s for s, _ in colorscale]
    colors = [_any_to_rgb(c) for _, c in colorscale]
    del colorscale
    if midpoint in scale:
        return colors[scale.index(midpoint)]
    ceil = min(filter(lambda s: s > midpoint, scale))
    floor = max(filter(lambda s: s < midpoint, scale))
    midpoint_normalised = normalise(midpoint, min_=floor, max_=ceil)
    color: str = find_intermediate_color(
        lowcolor=colors[scale.index(floor)],
        highcolor=colors[scale.index(ceil)],
        intermed=midpoint_normalised,
        colortype="rgb",
    )
    return color


def apply_alpha(color: Union[tuple, str], alpha: float) -> str:
    color = _any_to_rgb(color)
    return f"rgba({color[4:-1]}, {alpha})"
