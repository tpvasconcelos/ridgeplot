from typing import Any, Optional, Type, Union

import pytest
from _plotly_utils.exceptions import PlotlyError

from ridgeplot._colors import (
    _COLORSCALE_MAPPING,
    _any_to_rgb,
    _colormap_loader,
    apply_alpha,
    get_all_colorscale_names,
    get_color,
    get_colorscale,
    validate_colorscale,
)
from ridgeplot._types import ColorScaleType
from ridgeplot._utils import LazyMapping

VIRIDIS = (
    (0.0, "rgb(68, 1, 84)"),
    (0.1111111111111111, "rgb(72, 40, 120)"),
    (0.2222222222222222, "rgb(62, 73, 137)"),
    (0.3333333333333333, "rgb(49, 104, 142)"),
    (0.4444444444444444, "rgb(38, 130, 142)"),
    (0.5555555555555556, "rgb(31, 158, 137)"),
    (0.6666666666666666, "rgb(53, 183, 121)"),
    (0.7777777777777777, "rgb(110, 206, 88)"),
    (0.8888888888888888, "rgb(181, 222, 43)"),
    (1.0, "rgb(253, 231, 37)"),
)

# ==============================================================
# ---  _colormap_loader()
# ==============================================================


def test_colormap_loader() -> None:
    colorscale_mapping = _colormap_loader()
    assert colorscale_mapping["viridis"] == VIRIDIS


# ==============================================================
# ---  _PLOTLY_COLORSCALE_MAPPING
# ==============================================================


def test_plotly_colorscale_mapping() -> None:
    assert isinstance(_COLORSCALE_MAPPING, LazyMapping)
    for name, colorscale in _COLORSCALE_MAPPING.items():
        assert isinstance(name, str)
        validate_colorscale(colorscale=colorscale)


# ==============================================================
# ---  validate_colorscale()
# ==============================================================


@pytest.mark.parametrize(
    "colorscale",
    [
        # tuple of tuples of rgb colors
        (
            (0.0, "rgb(68, 1, 84)"),
            (0.4444444444444444, "rgb(38, 130, 142)"),
            (1.0, "rgb(253, 231, 37)"),
        ),
        # list of lists of hex colors
        [
            [0, "#440154"],
            [0.5019607843137255, "#21918c"],
            [1, "#fde725"],
        ],
    ],
)
def test_validate_colorscale(colorscale: ColorScaleType) -> None:
    validate_colorscale(colorscale=colorscale)


@pytest.mark.parametrize(
    ("colorscale", "expected_exception"),
    [
        # is not iterable
        (1, TypeError),
        # is not iterable of iterables
        ((1, 2, 3), TypeError),
        # inner tuples should have length 2 (for the scale and color values)
        (((1, 2, 3), (4, 5, 6)), ValueError),
        # Invalid scale values: first and last numbers
        # in the scale must be 0.0 and 1.0 respectively
        ((("a", 1), ("b", 2)), PlotlyError),
        (((1, "a"), (2, "b")), PlotlyError),
        (((1, "a"), (0, "a")), PlotlyError),
    ],
)
def test_validate_colorscale_fails_for_invalid_colorscale(
    colorscale: Any,
    expected_exception: Type[Exception],
) -> None:
    pytest.raises(expected_exception, validate_colorscale, colorscale=colorscale)


# ==============================================================
# ---  _any_to_rgb()
# ==============================================================


@pytest.mark.parametrize(
    ("color", "expected"),
    [
        ("#000000", "rgb(0, 0, 0)"),  # valid hex string
        ("rgb(1, 2, 3)", "rgb(1, 2, 3)"),  # valid rgb string
        ((4, 5, 6), "rgb(4, 5, 6)"),  # valid tuple
    ],
)
def test_any_to_rgb(color: Union[str, tuple], expected: str) -> None:
    assert _any_to_rgb(color=color) == expected


@pytest.mark.parametrize(
    ("color", "expected_exception", "exception_match"),
    [
        # invalid types
        (1, TypeError, None),
        ([1, 2, 3], TypeError, None),
        # invalid string values
        ("not a color", ValueError, None),
        # invalid hex
        ("#1234567890", PlotlyError, r"rgb colors tuples cannot exceed 255"),
        ("#ABCDEFGHIJ", ValueError, r"invalid literal for int\(\) with base 16"),
        # invalid rgb
        ("rgb(0,0,999)", PlotlyError, r"rgb colors tuples cannot exceed 255"),
        # invalid tuple
        ((1, 2), IndexError, None),
    ],
)
def test_any_to_rgb_fails_for_invalid_color(
    color: Any, expected_exception: Type[Exception], exception_match: Optional[str]
) -> None:
    pytest.raises(expected_exception, _any_to_rgb, color=color).match(exception_match or "")


@pytest.mark.xfail(reason="Incomplete implementation of RGB string validation from Plotly.")
@pytest.mark.parametrize(
    ("color", "expected_exception", "exception_match"),
    [
        # invalid rgb string
        ("rgb(1,2,3,4,5)", PlotlyError, None),
        ("rgb(0,0,-2)", PlotlyError, r"rgb colors tuples cannot exceed 255"),
        # invalid tuple
        ((1, 2, 3, 4), PlotlyError, None),
    ],
)
def test_any_to_rgb_bug_in_validation_incomplete(
    color: Any, expected_exception: Type[Exception], exception_match: Optional[str]
) -> None:
    pytest.raises(expected_exception, _any_to_rgb, color=color).match(exception_match or "")


# ==============================================================
# --- get_all_colorscale_names()
# ==============================================================


def test_get_all_colorscale_names() -> None:
    all_colorscale_names = get_all_colorscale_names()
    assert all(isinstance(name, str) for name in all_colorscale_names)
    assert "viridis" in all_colorscale_names
    for name in all_colorscale_names:
        get_colorscale(name=name)


# ==============================================================
# ---  get_colorscale()
# ==============================================================


def test_get_colorscale() -> None:
    assert get_colorscale(name="Viridis") == VIRIDIS
    # assert that `name` is case-insensitive
    assert get_colorscale(name="viridis") == VIRIDIS


def test_get_colorscale_fails_for_unknown_colorscale_name() -> None:
    with pytest.raises(ValueError, match="Unknown colorscale name"):
        get_colorscale(name="this colorscale doesnt exist")


# ==============================================================
# ---  get_color()
# ==============================================================


def test_get_color_midpoint_in_scale() -> None:
    assert get_color(colorscale=VIRIDIS, midpoint=0) == VIRIDIS[0][1]
    assert get_color(colorscale=VIRIDIS, midpoint=1) == VIRIDIS[-1][1]


def test_get_color_midpoint_not_in_scale() -> None:
    # TODO: Refactor `get_color` to make this easier to test.
    #       Currently just using a hard-coded value.
    assert get_color(colorscale=VIRIDIS, midpoint=0.5) == "rgb(34.5, 144.0, 139.5)"


@pytest.mark.parametrize("midpoint", [-10.0, -1.3, 1.9, 100.0])
def test_get_color_fails_for_midpoint_out_of_bounds(midpoint: float) -> None:
    with pytest.raises(ValueError, match="should be a float value between 0 and 1"):
        get_color(colorscale=..., midpoint=midpoint)


# ==============================================================
# ---  apply_alpha()
# ==============================================================


@pytest.mark.parametrize(
    ("color", "alpha", "expected"),
    [
        ("#000000", 0, "rgba(0, 0, 0, 0)"),
        ("rgb(1, 2, 3)", 0.2, "rgba(1, 2, 3, 0.2)"),
        ((4, 5, 6), 1.0, "rgba(4, 5, 6, 1.0)"),
    ],
)
def test_apply_alpha(color: Union[tuple, str], alpha: float, expected: str) -> None:
    assert apply_alpha(color=color, alpha=alpha) == expected
