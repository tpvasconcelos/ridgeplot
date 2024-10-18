from __future__ import annotations

from typing import TYPE_CHECKING, cast

from plotly import express as px

from ridgeplot._color.css_colors import CSS_NAMED_COLORS, CssNamedColor

if TYPE_CHECKING:
    from ridgeplot._types import Color


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


def unpack_rgb(rgb: str) -> tuple[float, float, float, float] | tuple[float, float, float]:
    prefix = rgb.split("(")[0] + "("
    values_str = map(str.strip, rgb.removeprefix(prefix).removesuffix(")").split(","))
    values_num = tuple(int(v) if v.isdecimal() else float(v) for v in values_str)
    return values_num  # type: ignore[return-value]


def apply_alpha(color: Color, alpha: float) -> str:
    values = unpack_rgb(to_rgb(color))
    return f"rgba({', '.join(map(str, values[:3]))}, {alpha})"


def round_color(color: Color, ndigits: int) -> str:
    color = to_rgb(color)
    prefix = color.split("(")[0] + "("
    values_round = tuple(v if isinstance(v, int) else round(v, ndigits) for v in unpack_rgb(color))
    return f"{prefix}{', '.join(map(str, values_round))})"
