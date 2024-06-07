from __future__ import annotations

from pathlib import Path

import pytest

from cicd.scripts.extract_latest_release_notes import get_tokens_latest_release


def test_get_tokens_latest_release_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        get_tokens_latest_release(changelog=Path("non_existent_file.md"))
