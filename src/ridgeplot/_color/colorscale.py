from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, cast

import plotly.express as px
from _plotly_utils.basevalidators import ColorscaleValidator as _ColorscaleValidator

from ridgeplot._color.utils import default_plotly_template
from ridgeplot._types import Color, ColorScale

if TYPE_CHECKING:
    from collections.abc import Collection


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
        # This helps us avoid floating point errors when making
        # comparisons in our test suite. The user should not
        # be able to notice *any* difference in the output
        coerced = tuple((v if isinstance(v, int) else round(v, ndigits=12), c) for v, c in coerced)
        return cast(ColorScale, coerced)


def infer_default_colorscale() -> ColorScale | Collection[Color] | str:
    return validate_and_coerce_colorscale(
        default_plotly_template().layout.colorscale.sequential or px.colors.sequential.Viridis
    )


def validate_and_coerce_colorscale(
    colorscale: ColorScale | Collection[Color] | str | None,
) -> ColorScale:
    """Convert mixed colorscale representations to the canonical
    :data:`ColorScale` format."""
    if colorscale is None:
        colorscale = infer_default_colorscale()
    return ColorscaleValidator().validate_coerce(colorscale)


def list_all_colorscale_names() -> list[str]:
    """Get a list of all available continuous colorscale names.

    .. deprecated:: 0.2.0
       This function is deprecated and will be removed in a future version.
       Please use :func:`px.colors.named_colorscales() <plotly.express.colors.named_colorscales>`
       from Plotly Express for the same functionality. For more details, visit:
       https://plotly.com/python/builtin-colorscales/#named-builtin-continuous-color-scales

    """
    warnings.warn(
        "list_all_colorscale_names() is deprecated and will be removed in a future version. "
        "Please use px.colors.named_colorscales() from Plotly Express for the same functionality. "
        "For more details, visit: "
        "https://plotly.com/python/builtin-colorscales/#named-builtin-continuous-color-scales",
        DeprecationWarning,
        stacklevel=2,
    )
    return sorted(ColorscaleValidator().named_colorscales)
