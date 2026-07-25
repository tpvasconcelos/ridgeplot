#!/usr/bin/env python
"""Add a changelog entry for a given pull request.

Inserts a ``- <title> ({gh-pr}`<number>`)`` entry into the ``### CI/CD``
subsection of the ``Unreleased changes`` section of the changelog, creating
the subsection (or the whole section) if it doesn't exist yet.

The changelog's structure is discovered with ``markdown-it-py`` (using the
tokens' source line maps), while the actual edit is a surgical line splice.
This keeps the rest of the file byte-for-byte untouched (as opposed to,
e.g., re-rendering the whole document with ``mdformat``, which would
restyle it).

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
from pathlib import Path
from typing import TYPE_CHECKING

from markdown_it import MarkdownIt

if TYPE_CHECKING:
    from markdown_it.token import Token

PATH_ROOT_DIR = Path(__file__).parents[3]
PATH_TO_CHANGELOG = PATH_ROOT_DIR.joinpath("docs/reference/changelog.md")

UNRELEASED_HEADING = "Unreleased changes"
CICD_HEADING = "CI/CD"

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


def _token_lines(token: Token) -> tuple[int, int]:
    """Return a block token's source line range as an ``(start, end)`` tuple."""
    if token.map is None:
        raise AssertionError("Block-level tokens always carry a source line map")
    return token.map[0], token.map[1]


def _is_heading(tokens: list[Token], i: int, tag: str, text: str | None = None) -> bool:
    """Whether ``tokens[i]`` opens a heading with the given tag (and text)."""
    token = tokens[i]
    if token.type != "heading_open" or token.tag != tag:
        return False
    return text is None or tokens[i + 1].content == text


def _find_unreleased_section(tokens: list[Token]) -> tuple[int, int] | None:
    """Find the (start, end) token index range of the 'Unreleased changes' section.

    ``start`` points at the first token after the section's heading and
    ``end`` at the next section's ``heading_open`` token (or one past the
    last token). Returns :data:`None` if the section doesn't exist.
    """
    start = None
    for i in range(len(tokens)):
        if not _is_heading(tokens, i, tag="h2"):
            continue
        if start is not None:
            return start, i
        if _is_heading(tokens, i, tag="h2", text=UNRELEASED_HEADING):
            start = i + 3  # skip the heading_open, inline, and heading_close tokens
    if start is None:
        return None
    return start, len(tokens)


def _new_unreleased_section(entry: str) -> list[str]:
    return [
        UNRELEASED_HEADING,
        "-" * len(UNRELEASED_HEADING),
        "",
        f"### {CICD_HEADING}",
        "",
        entry,
        "",
        "---",
        "",
    ]


def _insert_unreleased_section(lines: list[str], tokens: list[Token], entry: str) -> list[str]:
    """Insert a whole new 'Unreleased changes' section before the first section."""
    for i in range(len(tokens)):
        if _is_heading(tokens, i, tag="h2"):
            at = _token_lines(tokens[i])[0]
            return [*lines[:at], *_new_unreleased_section(entry), *lines[at:]]
    # No sections yet (e.g., an empty changelog): append at the end, making
    # sure that the new section's heading is preceded by a blank line
    # (otherwise the preceding paragraph would absorb the setext heading)
    if lines and lines[-1].strip():
        lines = [*lines, ""]
    return [*lines, *_new_unreleased_section(entry)]


def _find_cicd_insertion(tokens: list[Token], start: int, end: int) -> int | None:
    """Find the source line at which to insert an entry into the '### CI/CD' subsection.

    Returns the line right after the subsection's last bullet list (or right
    after its heading, if it contains no list yet), or :data:`None` if the
    subsection doesn't exist.
    """
    insert_at = None
    for i in range(start, end):
        token = tokens[i]
        if token.type == "heading_open":
            if insert_at is not None:
                break  # reached the next subsection
            if _is_heading(tokens, i, tag="h3", text=CICD_HEADING):
                insert_at = _token_lines(token)[1]
        elif insert_at is not None and token.type == "hr":
            break  # reached the section's trailing thematic break
        elif insert_at is not None and token.type == "bullet_list_open" and token.level == 0:
            insert_at = _token_lines(token)[1]
    return insert_at


def _find_subsection_insertion(tokens: list[Token], start: int, end: int, n_lines: int) -> int:
    """Find the source line at which to insert a new subsection at the end of the section."""
    # Insert before the section's trailing thematic break (if any)
    for i in range(start, end):
        if tokens[i].type == "hr":
            return _token_lines(tokens[i])[0]
    if end < len(tokens):
        return _token_lines(tokens[end])[0]
    return n_lines


def add_changelog_entry(changelog: Path, pr_number: int, pr_title: str) -> bool:
    """Add a changelog entry for the given PR. Returns whether the file was changed."""
    text = changelog.read_text()
    if f"{{gh-pr}}`{pr_number}`" in text:
        print(f"Changelog already references PR #{pr_number}; nothing to do.")
        return False

    entry = format_entry(pr_number, pr_title)
    lines = text.splitlines()
    tokens = MarkdownIt().parse(text)

    section = _find_unreleased_section(tokens)
    if section is None:
        lines = _insert_unreleased_section(lines, tokens, entry)
    else:
        start, end = section
        insert_at = _find_cicd_insertion(tokens, start, end)
        if insert_at is None:
            insert_at = _find_subsection_insertion(tokens, start, end, len(lines))
            new_lines = ["", f"### {CICD_HEADING}", "", entry]
        else:
            new_lines = [entry]
        # Walk back over any blank lines
        while insert_at > 0 and not lines[insert_at - 1].strip():
            insert_at -= 1
        if new_lines == [entry] and lines[insert_at - 1].lstrip().startswith("#"):
            # Keep a blank line between a heading and the first entry
            new_lines = ["", entry]
        lines[insert_at:insert_at] = new_lines

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
