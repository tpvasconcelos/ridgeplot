from __future__ import annotations

from collections.abc import Collection
from typing import Any, Union, cast

import plotly.express as px
from _plotly_utils.basevalidators import ColorscaleValidator as _ColorscaleValidator

from ridgeplot._coloring.css_colors import CSS_NAMED_COLORS, CssNamedColor
from ridgeplot._utils import normalise_min_max

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


def list_all_colorscale_names() -> list[str]:
    """Get a list with all available colorscale names.

    .. versionadded:: 0.1.21
        Replaced the deprecated function ``get_all_colorscale_names()``.

    Returns
    -------
    list[str]
        A list with all available colorscale names.
    """
    # Add 'default' for backwards compatibility
    px_colorscales = px.colors.named_colorscales()
    return sorted({"default", *px_colorscales, *(f"{name}_r" for name in px_colorscales)})


class ColorscaleValidator(_ColorscaleValidator):  # type: ignore[misc]
    def __init__(self) -> None:
        super().__init__("colorscale", "ridgeplot")

    @property
    def named_colorscales(self) -> dict[str, list[str]]:
        named_colorscales = cast(dict[str, list[str]], super().named_colorscales)
        if "default" not in named_colorscales:
            # Add 'default' for backwards compatibility
            named_colorscales["default"] = px.colors.DEFAULT_PLOTLY_COLORS
        return named_colorscales

    def validate_coerce(self, v: Any) -> ColorScale:
        coerced = super().validate_coerce(v)
        if coerced is None:
            self.raise_invalid_val(coerced)
        return cast(ColorScale, [tuple(c) for c in coerced])


def validate_and_coerce_colorscale(colorscale: ColorScale | Collection[Color] | str) -> ColorScale:
    """Convert mixed colorscale representations to the canonical
    :data:`ColorScale` format."""
    return ColorscaleValidator().validate_coerce(colorscale)


def to_rgb(color: Color) -> str:
    if not isinstance(color, (str, tuple)):
        raise TypeError(f"Expected str or tuple for color, got {type(color)} instead.")
    if isinstance(color, tuple):
        r, g, b = color
        rgb = f"rgb({r}, {g}, {b})"
    elif color.startswith("#"):
        return to_rgb(cast(str, px.colors.hex_to_rgb(color)))
    elif color.startswith(("rgb(", "rgba(")):
        rgb = color
    elif color in CSS_NAMED_COLORS:
        color = cast(CssNamedColor, color)
        return to_rgb(CSS_NAMED_COLORS[color])
    else:
        raise ValueError(
            f"color should be a tuple or a str representation "
            f"of a hex or rgb color, got {color!r} instead."
        )
    px.colors.validate_colors(rgb)
    return rgb


def interpolate_color(colorscale: ColorScale, p: float) -> Color:
    """Get a color from a colorscale at a given interpolation point ``p``."""
    if not (0 <= p <= 1):
        raise ValueError(
            f"The interpolation point 'p' should be a float value between 0 and 1, not {p}."
        )
    scale = [s for s, _ in colorscale]
    colors = [c for _, c in colorscale]
    del colorscale
    if p in scale:
        return colors[scale.index(p)]
    colors = [to_rgb(c) for c in colors]
    ceil = min(filter(lambda s: s > p, scale))
    floor = max(filter(lambda s: s < p, scale))
    p_normalised = normalise_min_max(p, min_=floor, max_=ceil)
    return cast(
        str,
        px.colors.find_intermediate_color(
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
    values = _unpack_rgb(to_rgb(color))
    return f"rgba({', '.join(map(str, values[:3]))}, {alpha})"


def round_color(color: Color, ndigits: int) -> str:
    color = to_rgb(color)
    prefix = color.split("(")[0] + "("
    values_round = tuple(v if isinstance(v, int) else round(v, ndigits) for v in _unpack_rgb(color))
    return f"{prefix}{', '.join(map(str, values_round))})"
