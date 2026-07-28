#!/usr/bin/env python
"""Add a changelog entry for a given pull request.

Inserts a ``- <title> ({gh-pr}`<number>`)`` entry into the ``### Dependencies``
subsection of the ``Unreleased changes`` section of the changelog, creating
the subsection (or the whole section) if it doesn't exist yet. The
subsection's entries are kept sorted alphabetically: the whole list is
re-sorted on every insertion, which also repairs any pre-existing ordering
violations (e.g., from manual edits).

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
DEPS_HEADING = "Dependencies"

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
        f"### {DEPS_HEADING}",
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


def _find_deps_subsection(tokens: list[Token], start: int, end: int) -> tuple[int, int] | None:
    """Find the (start, end) token index range of the '### Dependencies' subsection.

    ``start`` points at the subsection's ``heading_open`` token and ``end``
    at the next subsection's ``heading_open`` token, the section's trailing
    thematic break, or the end of the section. Returns :data:`None` if the
    subsection doesn't exist.
    """
    sub_start = None
    for i in range(start, end):
        token = tokens[i]
        if token.type == "heading_open":
            if sub_start is not None:
                return sub_start, i
            if _is_heading(tokens, i, tag="h3", text=DEPS_HEADING):
                sub_start = i
        elif sub_start is not None and token.type == "hr":
            return sub_start, i
    if sub_start is None:
        return None
    return sub_start, end


def _insert_entry_into_subsection(
    lines: list[str], tokens: list[Token], sub_start: int, sub_end: int, entry: str
) -> list[str]:
    """Insert the entry into the subsection's bullet list, keeping it sorted.

    All of the subsection's list items are re-sorted alphabetically as a
    whole, which also repairs any pre-existing ordering violations. Each
    item's source lines are moved as one block, so that multi-line entries
    (continuation lines, nested lists, etc.) are preserved intact.
    """
    blocks: list[list[str]] = []
    span_start = span_end = None
    for i in range(sub_start, sub_end):
        token = tokens[i]
        if token.type != "list_item_open" or token.level != 1:
            continue  # only consider items of top-level bullet lists
        item_start, item_end = _token_lines(token)
        block = lines[item_start:item_end]
        # An item's line map may extend over trailing blank lines
        # (e.g., in loose lists); strip them so that the re-assembled
        # list is a tight, contiguous block of entries
        while block and not block[-1].strip():
            block.pop()
        blocks.append(block)
        if span_start is None:
            span_start = item_start
        span_end = item_end
    if span_start is None or span_end is None:
        # No bullet list yet: insert right after the subsection's heading,
        # keeping a blank line between the heading and the first entry
        insert_at = _token_lines(tokens[sub_start])[1]
        return [*lines[:insert_at], "", entry, *lines[insert_at:]]
    # Walk back over any trailing blank lines covered by the last item's map
    while span_end > span_start and not lines[span_end - 1].strip():
        span_end -= 1
    blocks.append([entry])
    blocks.sort(key=lambda block: block[0].casefold())
    sorted_lines = [line for block in blocks for line in block]
    return [*lines[:span_start], *sorted_lines, *lines[span_end:]]


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
        subsection = _find_deps_subsection(tokens, start, end)
        if subsection is None:
            insert_at = _find_subsection_insertion(tokens, start, end, len(lines))
            # Walk back over any blank lines
            while insert_at > 0 and not lines[insert_at - 1].strip():
                insert_at -= 1
            lines[insert_at:insert_at] = ["", f"### {DEPS_HEADING}", "", entry]
        else:
            sub_start, sub_end = subsection
            lines = _insert_entry_into_subsection(lines, tokens, sub_start, sub_end, entry)

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
