from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import plotly.express as px
from _plotly_utils.basevalidators import ColorscaleValidator as _ColorscaleValidator

from ridgeplot._color.utils import default_plotly_template
from ridgeplot._types import Color, ColorScale

if TYPE_CHECKING:
    from collections.abc import Collection


def infer_default_colorscale() -> ColorScale | Collection[Color] | str:
    return default_plotly_template().layout.colorscale.sequential or px.colors.sequential.Viridis  # type: ignore[no-any-return]


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
        if coerced is None:  # pragma: no cover
            self.raise_invalid_val(coerced)
        return cast(ColorScale, tuple(tuple(c) for c in coerced))


def validate_and_coerce_colorscale(
    colorscale: ColorScale | Collection[Color] | str | None,
) -> ColorScale:
    """Convert mixed colorscale representations to the canonical
    :data:`ColorScale` format."""
    if colorscale is None:
        colorscale = infer_default_colorscale()
    return ColorscaleValidator().validate_coerce(colorscale)


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
    return sorted(ColorscaleValidator().named_colorscales)
