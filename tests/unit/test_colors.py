from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from _plotly_utils.exceptions import PlotlyError

from ridgeplot._colors import (
    Color,
    ColorScale,
    apply_alpha,
    interpolate_color,
    list_all_colorscale_names,
    round_color,
    to_rgb,
    validate_and_coerce_colorscale,
)

if TYPE_CHECKING:
    from collections.abc import Collection


# ==============================================================
# ---  to_rgb()
# ==============================================================


@pytest.mark.parametrize(
    ("color", "expected"),
    [
        ("#000000", "rgb(0, 0, 0)"),  # valid hex string
        ("rgb(1, 2, 3)", "rgb(1, 2, 3)"),  # valid rgb string
        ("rgba(1, 2, 3)", "rgba(1, 2, 3)"),  # valid rgba string
        ((4, 5, 6), "rgb(4, 5, 6)"),  # valid tuple
        ("forestgreen", "rgb(34, 139, 34)"),  # valid CSS named color
    ],
)
def test_to_rgb(color: Color, expected: str) -> None:
    assert to_rgb(color=color) == expected


@pytest.mark.parametrize(
    ("color", "expected_exception", "exception_match"),
    [
        # invalid types
        (1, TypeError, None),
        ([1, 2, 3], TypeError, None),
        # invalid CSS named color
        ("not-a-color", ValueError, None),
        # invalid hex
        ("#1234567890", ValueError, r"too many values to unpack \(expected 3\)"),
        ("#ABCDEFGHIJ", ValueError, r"invalid literal for int\(\) with base 16"),
        # invalid rgb
        ("rgb(0,0,999)", PlotlyError, r"rgb colors tuples cannot exceed 255"),
        # invalid tuple
        ((1, 2), ValueError, r"not enough values to unpack \(expected 3, got 2\)"),
        ((1, 2, 3, 4), ValueError, r"too many values to unpack \(expected 3\)"),
    ],
)
def test_to_rgb_fails_for_invalid_color(
    color: Any,
    expected_exception: type[Exception],
    exception_match: str | None,
) -> None:
    with pytest.raises(expected_exception, match=exception_match or ""):
        to_rgb(color)


@pytest.mark.xfail(reason="Incomplete implementation of RGB string validation from Plotly.")
@pytest.mark.parametrize(
    ("color", "expected_exception", "exception_match"),
    [
        ("rgb(1,2,3,4,5)", PlotlyError, None),
        ("rgb(0,0,-2)", PlotlyError, r"rgb colors tuples cannot exceed 255"),
    ],
)
def test_to_rgb_bug_in_validation_incomplete(
    color: Any,
    expected_exception: type[Exception],
    exception_match: str | None,
) -> None:
    with pytest.raises(expected_exception, match=exception_match or ""):
        to_rgb(color=color)


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
# ---  interpolate_color()
# ==============================================================


def test_interpolate_color_p_in_scale(viridis_colorscale: ColorScale) -> None:
    viridis_colorscale = list(viridis_colorscale)
    assert interpolate_color(colorscale=viridis_colorscale, p=0) == viridis_colorscale[0][1]
    assert interpolate_color(colorscale=viridis_colorscale, p=1) == viridis_colorscale[-1][1]


def test_interpolate_color_p_not_in_scale(viridis_colorscale: ColorScale) -> None:
    # Hard-coded test case.
    assert interpolate_color(colorscale=viridis_colorscale, p=0.5) == "rgb(34.5, 144.0, 139.5)"


@pytest.mark.parametrize("p", [-10.0, -1.3, 1.9, 100.0])
def test_interpolate_color_fails_for_p_out_of_bounds(p: float) -> None:
    with pytest.raises(ValueError, match="should be a float value between 0 and 1"):
        interpolate_color(colorscale=..., p=p)  # type: ignore[arg-type]


# ==============================================================
# ---  apply_alpha()
# ==============================================================


@pytest.mark.parametrize(
    ("color", "alpha", "expected"),
    [
        ("#000000", 0, "rgba(0, 0, 0, 0)"),
        ("rgb(1, 2, 3)", 0.2, "rgba(1, 2, 3, 0.2)"),
        ("rgba(1, 2, 3, 0.2)", 0.5, "rgba(1, 2, 3, 0.5)"),
        ((4, 5, 6), 1.0, "rgba(4, 5, 6, 1.0)"),
    ],
)
def test_apply_alpha(color: Color, alpha: float, expected: str) -> None:
    assert apply_alpha(color=color, alpha=alpha) == expected


# ==============================================================
# ---  round_color()
# ==============================================================


@pytest.mark.parametrize(
    ("color", "expected"),
    [
        # no change
        ("#000000", "rgb(0, 0, 0)"),
        ("rgb(1, 2, 3)", "rgb(1, 2, 3)"),
        ("rgba(1, 2, 3, 0.2)", "rgba(1, 2, 3, 0.2)"),
        ((4, 5, 6), "rgb(4, 5, 6)"),
        # round
        ("rgb(1.19, 2.21, 3.99)", "rgb(1.2, 2.2, 4.0)"),
        ("rgba(1.19,  2.21, 3.99,0.29)", "rgba(1.2, 2.2, 4.0, 0.3)"),
    ],
)
def test_round_color(color: Color, expected: Color) -> None:
    assert round_color(color=color, ndigits=1) == expected
