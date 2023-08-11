from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Dict, List, Tuple, Union, cast

from _plotly_utils.colors import validate_colors, validate_scale_values
from plotly.colors import find_intermediate_color, hex_to_rgb, label_rgb

from ridgeplot._types import ColorScaleT
from ridgeplot._utils import LazyMapping, normalise_min_max

_PATH_TO_COLORS_JSON = Path(__file__).parent.joinpath("colors.json")


def _colormap_loader() -> Dict[str, ColorScaleT]:
    colors: dict = json.loads(_PATH_TO_COLORS_JSON.read_text())
    for name, colorscale in colors.items():
        colors[name] = tuple(tuple(entry) for entry in colorscale)
    return colors


_COLORSCALE_MAPPING: LazyMapping[str, ColorScaleT] = LazyMapping(loader=_colormap_loader)


def validate_colorscale(colorscale: ColorScaleT) -> None:
    """Validate the structure, scale values, and colors of a colorscale.

    Adapted from :func:`_plotly_utils.colors.validate_colorscale`.
    """
    scale, colors = zip(*colorscale)
    validate_scale_values(scale=scale)
    validate_colors(colors=colors)


def _any_to_rgb(color: Union[str, tuple]) -> str:
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
        rgb = cast(str, label_rgb(color))
    elif color.startswith("#"):
        rgb = cast(str, label_rgb(hex_to_rgb(color)))
    elif color.startswith("rgb("):
        # Already an rgb string
        rgb = color
    else:
        raise ValueError(
            f"color should be a tuple or a str representation "
            f"of a hex or rgb color, got {color!r} instead."
        )
    validate_colors(rgb)
    return rgb


def list_all_colorscale_names() -> List[str]:
    """Get a list with all available colorscale names.

    .. versionadded:: 0.1.21
        Replaces the deprecated :func:`get_all_colorscale_names()`.

    Returns
    -------
    list[str]
        A list with all available colorscale names.
    """
    return sorted(_COLORSCALE_MAPPING.keys())


def get_all_colorscale_names() -> Tuple[str, ...]:
    """Get a tuple with all available colorscale names.

    .. deprecated:: 0.1.21
        Use :func:`list_all_colorscale_names()` instead.

    Returns
    -------
    tuple[str, ...]
        A tuple with all available colorscale names.
    """
    warnings.warn(
        "get_all_colorscale_names() is deprecated in favor of list_all_colorscale_names().",
        DeprecationWarning,
        stacklevel=2,
    )
    return tuple(list_all_colorscale_names())


def get_colorscale(name: str) -> ColorScaleT:
    """Get a colorscale by name.

    Parameters
    ----------
    name
        The colorscale name. This argument is case-insensitive. For instance,
        ``"YlOrRd"`` and ``"ylorrd"`` map to the same colorscale. Colorscale
        names ending in ``_r`` represent a *reversed* colorscale.

    Returns
    -------
    ColorScaleT
        A colorscale.

    Raises
    ------
    :exc:`ValueError`
        If an unknown name is provided
    """
    name = name.lower()
    if name not in _COLORSCALE_MAPPING:
        raise ValueError(
            f"Unknown colorscale name: '{name}'. The available colorscale"
            f" names are {tuple(_COLORSCALE_MAPPING.keys())}."
        )
    return _COLORSCALE_MAPPING[name]


def get_color(colorscale: ColorScaleT, midpoint: float) -> str:
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
    color = cast(
        str,
        find_intermediate_color(
            lowcolor=colors[scale.index(floor)],
            highcolor=colors[scale.index(ceil)],
            intermed=midpoint_normalised,
            colortype="rgb",
        ),
    )
    return color


def apply_alpha(color: Union[tuple, str], alpha: float) -> str:
    color = _any_to_rgb(color)
    return f"rgba({color[4:-1]}, {alpha})"
