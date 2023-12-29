from __future__ import annotations

from typing import Generator

import pytest

from ridgeplot._testing import patch_plotly_show


@pytest.fixture(autouse=True)
def _patch_plotly_show() -> Generator[None, None, None]:
    with patch_plotly_show():
        yield
