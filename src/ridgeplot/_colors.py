from __future__ import annotations

import json
from collections.abc import Collection
from pathlib import Path
from typing import Any, Union, cast

from _plotly_utils.basevalidators import ColorscaleValidator as _ColorscaleValidator
from _plotly_utils.colors import validate_colors
from plotly.colors import find_intermediate_color, hex_to_rgb

from ridgeplot._css_colors import CSS_NAMED_COLORS, CssNamedColor
from ridgeplot._utils import LazyMapping, normalise_min_max

_PATH_TO_COLORS_JSON = Path(__file__).parent.joinpath("colors.json")


Color = Union[str, tuple[float, float, float]]
"""A color can be represented by a tuple of ``(r, g, b)`` values or any valid
CSS color string - including hex, rgb/a, hsl/a, hsv/a, and named CSS colors."""

ColorScale = Collection[tuple[float, Color]]
"""The canonical form for a color scale is represented by a list of tuples of
two elements:

0. the first element (a *scale value*) is a float bounded to the
   interval ``[0, 1]``
1. the second element should be a valid :data:`Color` representation.

For instance, the Viridis color scale can be represented as:

>>> viridis: ColorScale = [
  (0.0, 'rgb(68, 1, 84)'),
  (0.1111111111111111, 'rgb(72, 40, 120)'),
  (0.2222222222222222, 'rgb(62, 73, 137)'),
  (0.3333333333333333, 'rgb(49, 104, 142)'),
  (0.4444444444444444, 'rgb(38, 130, 142)'),
  (0.5555555555555556, 'rgb(31, 158, 137)'),
  (0.6666666666666666, 'rgb(53, 183, 121)'),
  (0.7777777777777777, 'rgb(110, 206, 88)'),
  (0.8888888888888888, 'rgb(181, 222, 43)'),
  (1.0, 'rgb(253, 231, 37)')
]
"""


def _colormap_loader() -> dict[str, ColorScale]:
    colors: dict[str, ColorScale] = json.loads(_PATH_TO_COLORS_JSON.read_text())
    for name, colorscale in colors.items():
        colors[name] = tuple((s, c) for s, c in colorscale)
    return colors


_COLORSCALE_MAPPING: LazyMapping[str, ColorScale] = LazyMapping(loader=_colormap_loader)


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


class ColorscaleValidator(_ColorscaleValidator):  # type: ignore[misc]
    def __init__(self) -> None:
        super().__init__("colorscale", "ridgeplot")

    @property
    def named_colorscales(self) -> dict[str, list[Color]]:
        return {
            name: [c for _, c in colorscale] for name, colorscale in _COLORSCALE_MAPPING.items()
        }

    def validate_coerce(self, v: Any) -> ColorScale:
        coerced = super().validate_coerce(v)
        if coerced is None:
            self.raise_invalid_val(coerced)
        return cast(ColorScale, [tuple(c) for c in coerced])


def validate_and_coerce_colorscale(colorscale: ColorScale | Collection[Color] | str) -> ColorScale:
    """Convert mixed colorscale representations to the canonical
    :data:`ColorScale` format."""
    return ColorscaleValidator().validate_coerce(colorscale)


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
    elif color.startswith(("rgb(", "rgba(")):
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


def interpolate_color(colorscale: ColorScale, p: float) -> str:
    """Get a color from a colorscale at a given interpolation point ``p``."""
    if not (0 <= p <= 1):
        raise ValueError(
            f"The interpolation point 'p' should be a float value between 0 and 1, not {p}."
        )
    scale = [s for s, _ in colorscale]
    colors = [_any_to_rgb(c) for _, c in colorscale]
    del colorscale
    if p in scale:
        return colors[scale.index(p)]
    ceil = min(filter(lambda s: s > p, scale))
    floor = max(filter(lambda s: s < p, scale))
    p_normalised = normalise_min_max(p, min_=floor, max_=ceil)
    return cast(
        str,
        find_intermediate_color(
            lowcolor=colors[scale.index(floor)],
            highcolor=colors[scale.index(ceil)],
            intermed=p_normalised,
            colortype="rgb",
        ),
    )


def _unpack_rgb(rgb: str) -> tuple[float, float, float, float] | tuple[float, float, float]:
    prefix = rgb.split("(")[0] + "("
    values_str = map(str.strip, rgb.removeprefix(prefix).removesuffix(")").split(","))
    values_num = tuple(int(v) if v.isdecimal() else float(v) for v in values_str)
    return values_num  # type: ignore[return-value]


def apply_alpha(color: Color, alpha: float) -> str:
    values = _unpack_rgb(_any_to_rgb(color))
    return f"rgba({', '.join(map(str, values[:3]))}, {alpha})"


def round_color(color: Color, ndigits: int) -> str:
    color = _any_to_rgb(color)
    prefix = color.split("(")[0] + "("
    values_round = tuple(v if isinstance(v, int) else round(v, ndigits) for v in _unpack_rgb(color))
    return f"{prefix}{', '.join(map(str, values_round))})"
