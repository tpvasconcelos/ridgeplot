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
                trace_types=...,  # type: ignore[reportArgumentType]
                row_labels=...,  # type: ignore[reportArgumentType]
                colorscale=...,  # type: ignore[reportArgumentType]
                opacity=...,  # type: ignore[reportArgumentType]
                colormode=...,  # type: ignore[reportArgumentType]
                trace_labels=...,  # type: ignore[reportArgumentType]
                line_color=...,  # type: ignore[reportArgumentType]
                line_width=...,  # type: ignore[reportArgumentType]
                spacing=...,  # type: ignore[reportArgumentType]
                xpad=...,  # type: ignore[reportArgumentType]
            )
