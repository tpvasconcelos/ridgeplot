from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cicd.scripts.add_changelog_entry import (
    PATH_TO_CHANGELOG,
    add_changelog_entry,
    format_entry,
    main,
)

if TYPE_CHECKING:
    from pathlib import Path


def test_path_to_changelog_exists() -> None:
    assert PATH_TO_CHANGELOG.exists()
    assert PATH_TO_CHANGELOG.is_file()


@pytest.mark.parametrize(
    ("pr_number", "pr_title", "expected"),
    [
        (
            383,
            "Bump actions/checkout from 6 to 7",
            "- Bump actions/checkout from 6 to 7 ({gh-pr}`383`)",
        ),
        (379, "[pre-commit.ci] pre-commit autoupdate", "- pre-commit autoupdate ({gh-pr}`379`)"),
        (42, "  Padded title  ", "- Padded title ({gh-pr}`42`)"),
    ],
)
def test_format_entry(pr_number: int, pr_title: str, expected: str) -> None:
    assert format_entry(pr_number, pr_title) == expected


CHANGELOG_WITH_CICD_SUBSECTION = """\
# Release Notes

Intro paragraph...

Unreleased changes
------------------

### CI/CD

- Old entry ({gh-pr}`100`)

---

0.1.0
-----

- Old release change ({gh-pr}`99`)
"""

EXPECTED_WITH_CICD_SUBSECTION = """\
# Release Notes

Intro paragraph...

Unreleased changes
------------------

### CI/CD

- Old entry ({gh-pr}`100`)
- Bump foo from 1 to 2 ({gh-pr}`123`)

---

0.1.0
-----

- Old release change ({gh-pr}`99`)
"""

CHANGELOG_WITHOUT_CICD_SUBSECTION = """\
# Release Notes

Unreleased changes
------------------

### Bug fixes

- Fix something ({gh-pr}`101`)

---

0.1.0
-----

- Old release change ({gh-pr}`99`)
"""

EXPECTED_WITHOUT_CICD_SUBSECTION = """\
# Release Notes

Unreleased changes
------------------

### Bug fixes

- Fix something ({gh-pr}`101`)

### CI/CD

- Bump foo from 1 to 2 ({gh-pr}`123`)

---

0.1.0
-----

- Old release change ({gh-pr}`99`)
"""

CHANGELOG_WITHOUT_UNRELEASED_SECTION = """\
# Release Notes

Intro paragraph...

0.1.0
-----

- Old release change ({gh-pr}`99`)
"""

EXPECTED_WITHOUT_UNRELEASED_SECTION = """\
# Release Notes

Intro paragraph...

Unreleased changes
------------------

### CI/CD

- Bump foo from 1 to 2 ({gh-pr}`123`)

---

0.1.0
-----

- Old release change ({gh-pr}`99`)
"""

CHANGELOG_WITHOUT_ANY_SECTIONS = """\
# Release Notes

Intro paragraph...
"""

EXPECTED_WITHOUT_ANY_SECTIONS = """\
# Release Notes

Intro paragraph...

Unreleased changes
------------------

### CI/CD

- Bump foo from 1 to 2 ({gh-pr}`123`)

---
"""

CHANGELOG_WITH_TRAILING_SUBSECTION = """\
# Release Notes

Unreleased changes
------------------

### CI/CD

- Old entry ({gh-pr}`100`)

### Documentation

- Documentation change ({gh-pr}`101`)
"""

EXPECTED_WITH_TRAILING_SUBSECTION = """\
# Release Notes

Unreleased changes
------------------

### CI/CD

- Old entry ({gh-pr}`100`)
- Bump foo from 1 to 2 ({gh-pr}`123`)

### Documentation

- Documentation change ({gh-pr}`101`)
"""

CHANGELOG_WITH_LOOSE_ENTRIES = """\
# Release Notes

Unreleased changes
------------------

- Loose entry ({gh-pr}`100`)
"""

EXPECTED_WITH_LOOSE_ENTRIES = """\
# Release Notes

Unreleased changes
------------------

- Loose entry ({gh-pr}`100`)

### CI/CD

- Bump foo from 1 to 2 ({gh-pr}`123`)
"""

CHANGELOG_WITH_ATX_HEADINGS = """\
# Release Notes

## Unreleased changes

### CI/CD

- Old entry ({gh-pr}`100`)

---

## 0.1.0

- Old release change ({gh-pr}`99`)
"""

EXPECTED_WITH_ATX_HEADINGS = """\
# Release Notes

## Unreleased changes

### CI/CD

- Old entry ({gh-pr}`100`)
- Bump foo from 1 to 2 ({gh-pr}`123`)

---

## 0.1.0

- Old release change ({gh-pr}`99`)
"""

CHANGELOG_WITH_EMPTY_CICD_SUBSECTION = """\
# Release Notes

Unreleased changes
------------------

### CI/CD

---

0.1.0
-----

- Old release change ({gh-pr}`99`)
"""

EXPECTED_WITH_EMPTY_CICD_SUBSECTION = """\
# Release Notes

Unreleased changes
------------------

### CI/CD

- Bump foo from 1 to 2 ({gh-pr}`123`)

---

0.1.0
-----

- Old release change ({gh-pr}`99`)
"""

CHANGELOG_WITHOUT_THEMATIC_BREAK = """\
# Release Notes

Unreleased changes
------------------

### Bug fixes

- Fix something ({gh-pr}`101`)

0.1.0
-----

- Old release change ({gh-pr}`99`)
"""

EXPECTED_WITHOUT_THEMATIC_BREAK = """\
# Release Notes

Unreleased changes
------------------

### Bug fixes

- Fix something ({gh-pr}`101`)

### CI/CD

- Bump foo from 1 to 2 ({gh-pr}`123`)

0.1.0
-----

- Old release change ({gh-pr}`99`)
"""


@pytest.mark.parametrize(
    ("changelog_content", "expected_content"),
    [
        (CHANGELOG_WITH_CICD_SUBSECTION, EXPECTED_WITH_CICD_SUBSECTION),
        (CHANGELOG_WITHOUT_CICD_SUBSECTION, EXPECTED_WITHOUT_CICD_SUBSECTION),
        (CHANGELOG_WITHOUT_UNRELEASED_SECTION, EXPECTED_WITHOUT_UNRELEASED_SECTION),
        (CHANGELOG_WITHOUT_ANY_SECTIONS, EXPECTED_WITHOUT_ANY_SECTIONS),
        (CHANGELOG_WITH_TRAILING_SUBSECTION, EXPECTED_WITH_TRAILING_SUBSECTION),
        (CHANGELOG_WITH_LOOSE_ENTRIES, EXPECTED_WITH_LOOSE_ENTRIES),
        (CHANGELOG_WITH_ATX_HEADINGS, EXPECTED_WITH_ATX_HEADINGS),
        (CHANGELOG_WITH_EMPTY_CICD_SUBSECTION, EXPECTED_WITH_EMPTY_CICD_SUBSECTION),
        (CHANGELOG_WITHOUT_THEMATIC_BREAK, EXPECTED_WITHOUT_THEMATIC_BREAK),
    ],
    ids=[
        "existing-cicd-subsection",
        "missing-cicd-subsection",
        "missing-unreleased-section",
        "missing-any-sections",
        "trailing-subsection",
        "loose-entries",
        "atx-headings",
        "empty-cicd-subsection",
        "missing-thematic-break",
    ],
)
def test_add_changelog_entry(changelog_content: str, expected_content: str, tmp_path: Path) -> None:
    changelog_path = tmp_path / "changelog.md"
    changelog_path.write_text(changelog_content)
    changed = add_changelog_entry(
        changelog=changelog_path, pr_number=123, pr_title="Bump foo from 1 to 2"
    )
    assert changed is True
    assert changelog_path.read_text() == expected_content


def test_add_changelog_entry_to_real_changelog(tmp_path: Path) -> None:
    changelog_path = tmp_path / "changelog.md"
    changelog_path.write_text(PATH_TO_CHANGELOG.read_text())
    changed = add_changelog_entry(
        changelog=changelog_path, pr_number=999999, pr_title="Bump foo from 1 to 2"
    )
    assert changed is True
    text = changelog_path.read_text()
    entry = "- Bump foo from 1 to 2 ({gh-pr}`999999`)"
    assert entry in text
    # The new entry should land in the unreleased section (i.e., before
    # the first released version's section)
    first_release_at = text.index("\n0.")
    assert text.index(entry) < first_release_at


def test_add_changelog_entry_is_idempotent(tmp_path: Path) -> None:
    changelog_path = tmp_path / "changelog.md"
    changelog_path.write_text(CHANGELOG_WITH_CICD_SUBSECTION)
    changed = add_changelog_entry(
        changelog=changelog_path, pr_number=100, pr_title="Some already mentioned PR"
    )
    assert changed is False
    assert changelog_path.read_text() == CHANGELOG_WITH_CICD_SUBSECTION


def test_main(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    changelog_path = tmp_path / "changelog.md"
    changelog_path.write_text(CHANGELOG_WITH_CICD_SUBSECTION)
    monkeypatch.setattr(
        "sys.argv",
        [
            "add_changelog_entry.py",
            "123",
            "Bump foo from 1 to 2",
            "--changelog",
            str(changelog_path),
        ],
    )
    main()
    assert changelog_path.read_text() == EXPECTED_WITH_CICD_SUBSECTION
