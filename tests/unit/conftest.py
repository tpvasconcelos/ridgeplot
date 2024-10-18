from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Collection

    from ridgeplot._colors import Color, ColorScale

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


@pytest.fixture(scope="session")
def viridis_colorscale() -> ColorScale:
    return VIRIDIS


VALID_COLOR_SCALES = [
    (VIRIDIS, VIRIDIS),
    ("viridis", VIRIDIS),
    (list(zip(*VIRIDIS))[-1], VIRIDIS),
    # List of colors
    (["red", "green"], [[0, "red"], [1, "green"]]),
    # List of lists
    tuple([[[0, "red"], [1, "green"]]] * 2),
    # Tuple of tuples
    tuple([((0, "red"), (1, "green"))] * 2),
    # List of tuples
    tuple([[(0, "red"), (0.5, "blue"), (1, "green")]] * 2),
]


@pytest.fixture(scope="session", params=VALID_COLOR_SCALES)
def valid_colorscale(
    request: pytest.FixtureRequest,
) -> tuple[ColorScale | Collection[Color] | str, ColorScale]:
    return request.param  # type: ignore[no-any-return]


INVALID_COLOR_SCALES = [
    None,
    1,
    (1, 2, 3),
    VIRIDIS[0],
    ((1, 2, 3), (4, 5, 6)),
    (("a", 1), ("b", 2)),
    [(0, "red"), (1.2, "green")],
    [(0, "red"), (1, "green", "blue")],
    ["red", "invalid"],
    [[0, "red"], [1, "whodis"]],
]


@pytest.fixture(scope="session", params=INVALID_COLOR_SCALES)
def invalid_colorscale(request: pytest.FixtureRequest) -> ColorScale | Collection[Color] | str:
    return request.param  # type: ignore[no-any-return]
