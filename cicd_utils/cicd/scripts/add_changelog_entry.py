#!/usr/bin/env python
"""Add a changelog entry for a given pull request.

Inserts a ``- <title> ({gh-pr}`<number>`)`` entry into the ``### CI/CD``
subsection of the ``Unreleased changes`` section of the changelog, creating
the subsection (or the whole section) if it doesn't exist yet.

This script is idempotent: if the changelog already references the given
PR number, the file is left unchanged.

Used by the ``.github/workflows/bot-prs.yml`` workflow to automatically add
changelog entries to pull requests opened by trusted bots (e.g., dependabot
and pre-commit.ci).

Usage:
    python cicd_utils/cicd/scripts/add_changelog_entry.py <pr-number> <pr-title>
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PATH_ROOT_DIR = Path(__file__).parents[3]
PATH_TO_CHANGELOG = PATH_ROOT_DIR.joinpath("docs/reference/changelog.md")

UNRELEASED_HEADING = "Unreleased changes"
CICD_HEADING = "### CI/CD"

# Known bot prefixes that should be stripped from PR titles to
# match the changelog's entry conventions (e.g., the convention
# for pre-commit.ci PRs is simply "pre-commit autoupdate").
STRIP_TITLE_PREFIXES = ("[pre-commit.ci] ",)


def format_entry(pr_number: int, pr_title: str) -> str:
    """Format a changelog entry for the given PR number and title."""
    title = pr_title.strip()
    for prefix in STRIP_TITLE_PREFIXES:
        title = title.removeprefix(prefix)
    return f"- {title} ({{gh-pr}}`{pr_number}`)"


def _is_setext_underline(lines: list[str], i: int) -> bool:
    """Whether ``lines[i]`` is a setext heading underline (e.g., ``-----``).

    A dash-only line is a setext underline if it directly follows a
    non-blank line. Otherwise, it is a thematic break (e.g., ``---``).
    """
    if not re.fullmatch(r"-{2,}", lines[i].strip()):
        return False
    return i > 0 and bool(lines[i - 1].strip())


def _is_thematic_break(lines: list[str], i: int) -> bool:
    """Whether ``lines[i]`` is a thematic break (e.g., ``---``)."""
    return bool(re.fullmatch(r"-{3,}", lines[i].strip())) and not _is_setext_underline(lines, i)


def _find_unreleased_section(lines: list[str]) -> tuple[int, int] | None:
    """Find the (start, end) line indices of the 'Unreleased changes' section.

    ``start`` points at the section's heading text line and ``end`` at the
    heading text line of the next section (or one past the last line).
    Returns :data:`None` if the section doesn't exist.
    """
    start = None
    for i in range(len(lines) - 1):
        if lines[i].strip() == UNRELEASED_HEADING and _is_setext_underline(lines, i + 1):
            start = i
            break
    if start is None:
        return None
    for j in range(start + 2, len(lines)):
        if _is_setext_underline(lines, j):
            return start, j - 1
    return start, len(lines)


def _new_unreleased_section(entry: str) -> list[str]:
    return [
        UNRELEASED_HEADING,
        "-" * len(UNRELEASED_HEADING),
        "",
        CICD_HEADING,
        "",
        entry,
        "",
        "---",
        "",
    ]


def _insert_unreleased_section(lines: list[str], entry: str) -> list[str]:
    """Insert a whole new 'Unreleased changes' section before the first section."""
    for i in range(len(lines)):
        if _is_setext_underline(lines, i):
            first_heading = i - 1
            return [
                *lines[:first_heading],
                *_new_unreleased_section(entry),
                *lines[first_heading:],
            ]
    # No sections yet (e.g., an empty changelog): append at the end, making
    # sure that the new section's heading is preceded by a blank line
    # (otherwise the preceding paragraph would absorb the setext heading)
    if lines and lines[-1].strip():
        lines = [*lines, ""]
    return [*lines, *_new_unreleased_section(entry)]


def _insert_cicd_subsection(lines: list[str], start: int, end: int, entry: str) -> list[str]:
    """Insert a new '### CI/CD' subsection at the end of the 'Unreleased changes' section."""
    # Insert before the section's trailing thematic break (if any)
    insert_at = end
    for i in range(start + 2, end):
        if _is_thematic_break(lines, i):
            insert_at = i
            break
    # Walk back over any blank lines
    while insert_at > start + 2 and not lines[insert_at - 1].strip():
        insert_at -= 1
    return [*lines[:insert_at], "", CICD_HEADING, "", entry, *lines[insert_at:]]


def _append_to_cicd_subsection(lines: list[str], cicd_at: int, end: int, entry: str) -> list[str]:
    """Append an entry at the end of an existing '### CI/CD' subsection."""
    # The subsection ends at the next subsection heading, the section's
    # trailing thematic break, or the end of the section (whichever
    # comes first).
    insert_at = end
    for i in range(cicd_at + 1, end):
        if lines[i].startswith("### ") or _is_thematic_break(lines, i):
            insert_at = i
            break
    # Walk back over any blank lines
    while insert_at > cicd_at + 1 and not lines[insert_at - 1].strip():
        insert_at -= 1
    return [*lines[:insert_at], entry, *lines[insert_at:]]


def add_changelog_entry(changelog: Path, pr_number: int, pr_title: str) -> bool:
    """Add a changelog entry for the given PR. Returns whether the file was changed."""
    text = changelog.read_text()
    if f"{{gh-pr}}`{pr_number}`" in text:
        print(f"Changelog already references PR #{pr_number}; nothing to do.")
        return False

    entry = format_entry(pr_number, pr_title)
    lines = text.splitlines()

    section = _find_unreleased_section(lines)
    if section is None:
        lines = _insert_unreleased_section(lines, entry)
    else:
        start, end = section
        cicd_at = next(
            (i for i in range(start + 2, end) if lines[i].strip() == CICD_HEADING),
            None,
        )
        if cicd_at is None:
            lines = _insert_cicd_subsection(lines, start, end, entry)
        else:
            lines = _append_to_cicd_subsection(lines, cicd_at, end, entry)

    while lines and not lines[-1].strip():
        lines.pop()
    changelog.write_text("\n".join(lines) + "\n")
    print(f"Added changelog entry: {entry}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pr_number", type=int, help="The pull request number.")
    parser.add_argument("pr_title", type=str, help="The pull request title.")
    parser.add_argument(
        "--changelog",
        type=Path,
        default=PATH_TO_CHANGELOG,
        help="Path to the changelog file.",
    )
    args = parser.parse_args()
    add_changelog_entry(
        changelog=args.changelog,
        pr_number=args.pr_number,
        pr_title=args.pr_title,
    )


if __name__ == "__main__":
    main()
