from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ridgeplot._color.colorscale import (
    infer_default_colorscale,
    list_all_colorscale_names,
    validate_and_coerce_colorscale,
)

if TYPE_CHECKING:
    from collections.abc import Collection

    from ridgeplot._types import Color, ColorScale


# ==============================================================
# ---  infer_default_colorscale()
# ==============================================================


def test_infer_default_colorscale() -> None:
    assert infer_default_colorscale() == validate_and_coerce_colorscale("plasma")


# ==============================================================
# ---  validate_and_coerce_colorscale()
# ==============================================================


def test_validate_and_coerce_colorscale(
    valid_colorscale: tuple[ColorScale | Collection[Color] | str, ColorScale]
) -> None:
    colorscale, expected = valid_colorscale
    coerced = validate_and_coerce_colorscale(colorscale=colorscale)
    values, colors = zip(*coerced)
    values_expected, colors_expected = zip(*expected)
    assert values == pytest.approx(values_expected)
    assert colors == colors_expected


def test_validate_and_coerce_colorscale_fails(
    invalid_colorscale: ColorScale | Collection[Color] | str,
) -> None:
    with pytest.raises(
        ValueError, match=r"Invalid value .* received for the 'colorscale' property"
    ):
        validate_and_coerce_colorscale(invalid_colorscale)


# ==============================================================
# --- list_all_colorscale_names()
# ==============================================================


def test_list_all_colorscale_names() -> None:
    all_colorscale_names = list_all_colorscale_names()
    assert all(isinstance(name, str) for name in all_colorscale_names)
    assert "viridis" in all_colorscale_names
    assert "default" in all_colorscale_names
    for name in all_colorscale_names:
        validate_and_coerce_colorscale(name)
