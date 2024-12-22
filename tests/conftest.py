from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import pytest

from cicd.test_helpers import patch_plotly_show


@pytest.fixture(autouse=True, scope="session")
def _patch_plotly_show() -> Generator[None]:  # pyright: ignore[reportUnusedFunction]
    with patch_plotly_show():
        yield
