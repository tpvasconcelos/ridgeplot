from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ridgeplot._figure_factory import create_ridgeplot

if TYPE_CHECKING:
    from ridgeplot._types import Densities


class TestCreateRidgeplot:
    @pytest.mark.parametrize(
        "densities",
        [
            [],
            [1, 2, 3],
            [[1, 2, 3]],
            [(1, 2)],
            [[(1, 2)]],
        ],
    )
    def test_densities_must_be_4d(self, densities: Densities) -> None:
        with pytest.raises(ValueError, match="Expected a 4D array of densities"):
            create_ridgeplot(
                densities=densities,
                trace_types=...,  # pyright: ignore[reportArgumentType]
                colorscale=...,  # pyright: ignore[reportArgumentType]
                opacity=...,  # pyright: ignore[reportArgumentType]
                colormode=...,  # pyright: ignore[reportArgumentType]
                trace_labels=...,  # pyright: ignore[reportArgumentType]
                line_color=...,  # pyright: ignore[reportArgumentType]
                line_width=...,  # pyright: ignore[reportArgumentType]
                spacing=...,  # pyright: ignore[reportArgumentType]
                show_yticklabels=...,  # pyright: ignore[reportArgumentType]
                xpad=...,  # pyright: ignore[reportArgumentType]
            )
