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
                colorscale=...,  # type: ignore[arg-type]
                coloralpha=...,  # type: ignore[arg-type]
                colormode=...,  # type: ignore[arg-type]
                trace_labels=...,  # type: ignore[arg-type]
                linewidth=...,  # type: ignore[arg-type]
                spacing=...,  # type: ignore[arg-type]
                show_yticklabels=...,  # type: ignore[arg-type]
                xpad=...,  # type: ignore[arg-type]
            )
