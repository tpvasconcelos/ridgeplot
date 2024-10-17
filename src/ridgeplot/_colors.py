from __future__ import annotations

import json
import sys
from collections.abc import Collection
from pathlib import Path
from typing import Union, cast

from _plotly_utils.colors import validate_colors, validate_scale_values
from plotly.colors import find_intermediate_color, hex_to_rgb

if sys.version_info >= (3, 13):
    from typing import TypeIs
else:
    from typing_extensions import TypeIs

from ridgeplot._css_colors import CSS_NAMED_COLORS, CssNamedColor
from ridgeplot._utils import LazyMapping, get_collection_array_shape, normalise_min_max

_PATH_TO_COLORS_JSON = Path(__file__).parent.joinpath("colors.json")


Color = Union[str, tuple[float, float, float]]
"""A color can be represented by a tuple of ``(r, g, b)`` values or any valid
CSS color string - including hex, rgb/a, hsl/a, hsv/a, and named CSS colors."""

ColorScale = Collection[tuple[float, Color]]
"""The canonical form for a color scale represented by a collection of tuples of
two elements:

0. the first element (a *scale value*) is a float bounded to the
   interval ``[0, 1]``
1. the second element should be a valid :data:`Color` representation.

For instance, the Viridis color scale can be represented as:

>>> get_colorscale("Viridis")
((0.0, 'rgb(68, 1, 84)'),
 (0.1111111111111111, 'rgb(72, 40, 120)'),
 (0.2222222222222222, 'rgb(62, 73, 137)'),
 (0.3333333333333333, 'rgb(49, 104, 142)'),
 (0.4444444444444444, 'rgb(38, 130, 142)'),
 (0.5555555555555556, 'rgb(31, 158, 137)'),
 (0.6666666666666666, 'rgb(53, 183, 121)'),
 (0.7777777777777777, 'rgb(110, 206, 88)'),
 (0.8888888888888888, 'rgb(181, 222, 43)'),
 (1.0, 'rgb(253, 231, 37)'))
"""


def _colormap_loader() -> dict[str, ColorScale]:
    colors: dict[str, ColorScale] = json.loads(_PATH_TO_COLORS_JSON.read_text())
    for name, colorscale in colors.items():
        colors[name] = tuple((s, c) for s, c in colorscale)
    return colors


_COLORSCALE_MAPPING: LazyMapping[str, ColorScale] = LazyMapping(loader=_colormap_loader)


def is_canonical_colorscale(
    colorscale: ColorScale | Collection[Color] | str,
) -> TypeIs[ColorScale]:
    if isinstance(colorscale, str) or not isinstance(colorscale, Collection):
        return False
    shape = get_collection_array_shape(colorscale)
    if not (len(shape) == 2 and shape[1] == 2):
        return False
    scale, colors = zip(*colorscale)
    return (
        all(isinstance(s, (int, float)) for s in scale) and
        all(isinstance(c, (str, tuple)) for c in colors)
    )  # fmt: skip


def validate_canonical_colorscale(colorscale: ColorScale) -> None:
    """Validate the structure, scale values, and colors of a colorscale in the
    canonical format."""
    if not is_canonical_colorscale(colorscale):
        raise TypeError(
            "The colorscale should be a collection of tuples of two elements: "
            "a scale value and a color."
        )
    scale, colors = zip(*colorscale)
    validate_scale_values(scale=scale)
    validate_colors(colors=colors)


def _any_to_rgb(color: Color) -> str:
    """Convert any color to an rgb string.

    Parameters
    ----------
    color
        A color. This can be a tuple of ``(r, g, b)`` values, a hex string,
        or an rgb string.

    Returns
    -------
    str
        An rgb string.

    Raises
    ------
    TypeError
        If ``color`` is not a tuple or a string.
    ValueError
        If ``color`` is a string that does not represent a hex or rgb color.
    """
    if not isinstance(color, (str, tuple)):
        raise TypeError(f"Expected str or tuple for color, got {type(color)} instead.")
    if isinstance(color, tuple):
        r, g, b = color
        rgb = f"rgb({r}, {g}, {b})"
    elif color.startswith("#"):
        return _any_to_rgb(cast(str, hex_to_rgb(color)))
    elif color.startswith("rgb("):
        rgb = color
    elif color in CSS_NAMED_COLORS:
        color = cast(CssNamedColor, color)
        return _any_to_rgb(CSS_NAMED_COLORS[color])
    else:
        raise ValueError(
            f"color should be a tuple or a str representation "
            f"of a hex or rgb color, got {color!r} instead."
        )
    validate_colors(rgb)
    return rgb


def list_all_colorscale_names() -> list[str]:
    """Get a list with all available colorscale names.

    .. versionadded:: 0.1.21
        Replaced the deprecated function ``get_all_colorscale_names()``.

    Returns
    -------
    list[str]
        A list with all available colorscale names.
    """
    return sorted(_COLORSCALE_MAPPING.keys())


def get_colorscale(name: str) -> ColorScale:
    """Get a colorscale by name.

    Parameters
    ----------
    name
        The colorscale name. This argument is case-insensitive. For instance,
        ``"YlOrRd"`` and ``"ylorrd"`` map to the same colorscale. Colorscale
        names ending in ``_r`` represent a *reversed* colorscale.

    Returns
    -------
    ColorScale
        A colorscale.

    Raises
    ------
    :exc:`ValueError`
        If an unknown name is provided
    """
    name = name.lower()
    if name not in _COLORSCALE_MAPPING:
        raise ValueError(
            f"Unknown color scale name: '{name}'. The available color scale "
            f"names are {tuple(_COLORSCALE_MAPPING.keys())}."
        )
    return _COLORSCALE_MAPPING[name]


def canonical_colorscale_from_list(colors: Collection[Color]) -> ColorScale:
    """Infer a colorscale from a list of colors.

    Parameters
    ----------
    colors
        An collection of :data:`Color` values.

    Returns
    -------
    ColorScale
        A colorscale with the same colors as the input list, but with
        scale values evenly spaced between 0 and 1.
    """
    colors = list(colors)
    n_colors = len(colors)
    scale = [i / (n_colors - 1) for i in range(n_colors)]
    scale[-1] = 1.0  # Avoid floating point errors
    return tuple(zip(scale, colors))


def normalise_colorscale(colorscale: ColorScale | Collection[Color] | str) -> ColorScale:
    """Convert mixed colorscale representations to the canonical
    :data:`ColorScale` format."""
    if isinstance(colorscale, str):
        return get_colorscale(name=colorscale)
    if is_canonical_colorscale(colorscale):
        validate_canonical_colorscale(colorscale)
        return colorscale
    # There is a bug in mypy that results in the type narrowing not working
    # properly here. See https://github.com/python/mypy/issues/17181
    colorscale = canonical_colorscale_from_list(colors=colorscale)  # type: ignore[unreachable]
    return colorscale


def interpolate_color(colorscale: ColorScale, midpoint: float) -> str:
    """Get a color from a colorscale at a given midpoint.

    Given a colorscale, it interpolates the expected color at a given midpoint,
    on a scale from 0 to 1.
    """
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
    return cast(
        str,
        find_intermediate_color(
            lowcolor=colors[scale.index(floor)],
            highcolor=colors[scale.index(ceil)],
            intermed=midpoint_normalised,
            colortype="rgb",
        ),
    )


def apply_alpha(color: Color, alpha: float) -> str:
    color = _any_to_rgb(color)
    return f"rgba({color[4:-1]}, {alpha})"
