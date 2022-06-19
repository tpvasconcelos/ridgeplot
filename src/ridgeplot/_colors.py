import json
from pathlib import Path
from typing import Dict, Iterable, Tuple, Union

from _plotly_utils.colors import validate_colors, validate_scale_values
from plotly.colors import find_intermediate_color, hex_to_rgb, label_rgb

from ridgeplot._utils import LazyMapping, normalise_min_max

# A colorscale is an iterable (usually a list or tuple) of tuples of two
# elements:
#   - the first element (a _scale value_) is a float bounded to the
#     interval [0, 1]
#   - the second element (a _color_) is a string representation of a
#     color parsable by Plotly
#
# For instance, The Viridis colorscale would be defined as
# >>> get_colorscale("viridis")
# ... ((0.0, 'rgb(68, 1, 84)'),
# ...  (0.1111111111111111, 'rgb(72, 40, 120)'),
# ...  (0.2222222222222222, 'rgb(62, 73, 137)'),
# ...  (0.3333333333333333, 'rgb(49, 104, 142)'),
# ...  (0.4444444444444444, 'rgb(38, 130, 142)'),
# ...  (0.5555555555555556, 'rgb(31, 158, 137)'),
# ...  (0.6666666666666666, 'rgb(53, 183, 121)'),
# ...  (0.7777777777777777, 'rgb(110, 206, 88)'),
# ...  (0.8888888888888888, 'rgb(181, 222, 43)'),
# ...  (1.0, 'rgb(253, 231, 37)'))
ColorScaleType = Iterable[Tuple[float, str]]
ColorScaleMappingType = Dict[str, ColorScaleType]

_PATH_TO_COLORS_JSON = Path(__file__).parent.joinpath("colors.json")


def _colormap_loader() -> ColorScaleMappingType:
    colors: dict = json.loads(_PATH_TO_COLORS_JSON.read_text())
    for name, colorscale in colors.items():
        colors[name] = tuple(tuple(entry) for entry in colorscale)
    return colors


_COLORSCALE_MAPPING = LazyMapping(loader=_colormap_loader)


def validate_colorscale(colorscale: ColorScaleType) -> None:
    """Validate the structure, scale values, and colors of colorscale.

    Adapted from ``_plotly_utils.colors.validate_colorscale``.
    """
    scale, colors = zip(*colorscale)
    validate_scale_values(scale=scale)
    validate_colors(colors=colors)


def _any_to_rgb(color: Union[str, tuple]) -> str:
    if not isinstance(color, (str, tuple)):
        raise TypeError(f"Expected str or tuple for color, got {type(color)} instead.")
    if isinstance(color, tuple):
        rgb = label_rgb(color)
    elif color.startswith("#"):
        rgb = label_rgb(hex_to_rgb(color))
    elif color.startswith("rgb("):
        rgb = str(color)
    else:
        raise ValueError(
            f"color should be a tuple or a str representation of a hex or rgb color, got {color!r} instead."
        )
    validate_colors(rgb)
    return rgb


def get_colorscale(name: str) -> ColorScaleType:
    """Helper to get a known colorscale.

    Parameters
    ----------
    name
        The colorscale name. This argument is case insensitive. For  instance,
        "YlOrRd" and "ylorrd" map to the same colorscale. Colorscale names
        ending in '*_r' represent to a _reversed_ colorscale.

    Raises
    ------
    ValueError
        If an unknown name is provided

    """
    name = name.lower()
    if name not in _COLORSCALE_MAPPING:
        raise ValueError(
            f"Could not find colorscale '{name}'. The available colorscale"
            f" names are {tuple(_COLORSCALE_MAPPING.keys())}."
        )
    return _COLORSCALE_MAPPING[name]


def get_color(colorscale: ColorScaleType, midpoint: float) -> str:
    """Given a colorscale, it interpolates the expected color at a given
    midpoint, on a scale from 0 to 1."""
    if not (0 <= midpoint <= 1):
        raise ValueError(f"The 'midpoint' should be a float value between 0 and 1, not {midpoint}.")
    scale = [s for s, _ in colorscale]
    colors = [_any_to_rgb(c) for _, c in colorscale]
    del colorscale
    if midpoint in scale:
        return colors[scale.index(midpoint)]
    ceil = min(filter(lambda s: s > midpoint, scale))
    floor = max(filter(lambda s: s < midpoint, scale))
    midpoint_normalised = normalise_min_max(midpoint, min_=floor, max_=ceil)
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
