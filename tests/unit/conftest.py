from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.express as px
import pytest

if TYPE_CHECKING:
    from collections.abc import Collection

    from ridgeplot._types import Color, ColorScale

VIRIDIS = (
    (0.0, "#440154"),
    (0.1111111111111111, "#482878"),
    (0.2222222222222222, "#3e4989"),
    (0.3333333333333333, "#31688e"),
    (0.4444444444444444, "#26828e"),
    (0.5555555555555556, "#1f9e89"),
    (0.6666666666666666, "#35b779"),
    (0.7777777777777777, "#6ece58"),
    (0.8888888888888888, "#b5de2b"),
    (1.0, "#fde725"),
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
    # Use Plotly colorscales directly
    (px.colors.sequential.Viridis, VIRIDIS),
]


@pytest.fixture(scope="session", params=VALID_COLOR_SCALES)
def valid_colorscale(
    request: pytest.FixtureRequest,
) -> tuple[ColorScale | Collection[Color] | str, ColorScale]:
    return request.param  # type: ignore[no-any-return]


INVALID_COLOR_SCALES = [
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
