from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from cicd.scripts.extract_latest_release_notes import (
    PATH_TO_CHANGELOG,
    extract_latest_release_notes,
    parse_markdown_tokens,
)

if TYPE_CHECKING:
    from markdown_it.token import Token


def test_path_to_changelog_exists() -> None:
    assert PATH_TO_CHANGELOG.exists()
    assert PATH_TO_CHANGELOG.is_file()


def test_extract_latest_release_notes_file_not_found() -> None:
    with pytest.raises(FileNotFoundError, match="File not found: non_existent_file.md"):
        extract_latest_release_notes(changelog=Path("non_existent_file.md"))


CHANGELOG_CONTENT_01 = """\
# Release Notes

Ipsum lorem...

Unreleased changes
------------------

Unreleased changes notes...

- Unreleased change 1 ({gh-pr}`4`)

0.1.2
-----

Notes for version 0.1.2...

- Change 3 ({gh-pr}`3`)
- Change 2 ([#2](example.com))

0.1.1
-----

Notes for version 0.1.1...

- Change 1 ({gh-pr}`1`)
"""

LATEST_NOTES_01 = """\
Notes for version 0.1.2...

- Change 3 ([#3](https://github.com/tpvasconcelos/ridgeplot/pull/3))
- Change 2 ([#2](example.com))
"""


@pytest.mark.parametrize(
    ("changelog_content", "expected_latest_notes"),
    [(CHANGELOG_CONTENT_01, LATEST_NOTES_01)],
    ids=["01"],
)
def test_extract_latest_release_notes(
    changelog_content: str, expected_latest_notes: str, tmp_path: Path
) -> None:
    changelog_path = tmp_path / "changelog.md"
    changelog_path.write_text(changelog_content)
    text = extract_latest_release_notes(changelog=changelog_path)
    assert text == expected_latest_notes


def test_myst_roles() -> None:
    whitelisted_roles = {"gh-pr", "gh-issue"}

    def validate_tokens(tkns: list[Token]) -> None:
        for token in tkns:
            if token.children:
                validate_tokens(token.children)
            if token.type == "myst_role" and token.meta.get("name", "") not in whitelisted_roles:
                raise ValueError(f"Unexpected myst role: {token.meta}")

    tokens = parse_markdown_tokens(PATH_TO_CHANGELOG.read_text())
    validate_tokens(tokens)
