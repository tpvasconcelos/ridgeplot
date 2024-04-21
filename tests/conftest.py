from __future__ import annotations

from typing import Generator

import pytest

from ci_pkg.test_helpers import patch_plotly_show


@pytest.fixture(autouse=True, scope="session")
def _patch_plotly_show() -> Generator[None, None, None]:
    with patch_plotly_show():
        yield
