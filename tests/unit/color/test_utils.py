from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from _plotly_utils.exceptions import PlotlyError

from ridgeplot._color.utils import apply_alpha, default_plotly_template, round_color, to_rgb

if TYPE_CHECKING:

    from ridgeplot._types import Color


# ==============================================================
# ---  default_plotly_template()
# ==============================================================


def test_default_plotly_template() -> None:
    template = default_plotly_template()
    assert template.layout.colorscale.sequential is not None
    assert template.layout.colorway is not None


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
