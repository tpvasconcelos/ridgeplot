#!/usr/bin/env python
"""Extract the latest release notes

Execution steps:
- Extracts the latest release notes from docs/reference/changelog.md
- The output is written to the `LATEST_RELEASE_NOTES.md` file.
- The body of this file is then used as the body of the GitHub release.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdformat.renderer import MDRenderer
from mdit_py_plugins.myst_role import myst_role_plugin

if TYPE_CHECKING:
    from collections.abc import Sequence


PATH_ROOT_DIR = Path(__file__).parents[3]
PATH_TO_CHANGELOG = PATH_ROOT_DIR.joinpath("docs/reference/changelog.md")
PATH_TO_LATEST_RELEASE_NOTES = PATH_ROOT_DIR.joinpath("LATEST_RELEASE_NOTES.md")


def parse_markdown_tokens(text: str) -> list[Token]:
    """Parse markdown text and return `markdown_it` tokens."""
    md_parser = MarkdownIt().use(myst_role_plugin)
    tokens = md_parser.parse(src=text)
    return tokens


def get_link_tokens(text: str, href: str) -> list[Token]:
    return [
        Token(type="link_open", tag="a", nesting=1, attrs={"href": href}),
        Token(type="text", tag="", nesting=0, level=1, content=text),
        Token(type="link_close", tag="a", nesting=-1),
    ]


def replace_pr_links(tokens: list[Token]) -> list[Token]:
    tokens_new = []
    for token in tokens:
        if token.children:
            token.children = replace_pr_links(token.children)
        if token.type == "myst_role" and token.meta.get("name", "") in ("gh-pr", "gh-issue"):
            gh_number = int(token.content)
            gh_type = "pull" if token.meta["name"] == "gh-pr" else "issues"
            link_tokens = get_link_tokens(
                text=f"#{gh_number}",
                href=f"https://github.com/tpvasconcelos/ridgeplot/{gh_type}/{gh_number}",
            )
            tokens_new.extend(link_tokens)
            continue
        tokens_new.append(token)
    return tokens_new


def get_latest_release_section(tokens: list[Token]) -> list[Token]:
    # Get the tokens pertaining to the latest release section,
    # which should be the second h2 section in the changelog.
    count_h2 = 0
    tokens_lr: list[Token] = []
    for token in tokens:
        is_h2 = token.type == "heading_open" and token.tag == "h2"
        count_h2 += is_h2
        if count_h2 == 2:
            tokens_lr.append(token)
        elif count_h2 > 2:
            break
    # Remove h2 heading tokens
    tokens_lr = tokens_lr[3:]
    return tokens_lr


def render_md_tokens(tokens: Sequence[Token]) -> str:
    """Render markdown tokens as text."""
    md_renderer = MDRenderer()
    text = md_renderer.render(tokens=tokens, options={}, env={})
    return text


def extract_latest_release_notes(changelog: Path) -> str:
    if not changelog.exists():
        raise FileNotFoundError(f"File not found: {changelog}")
    tokens = parse_markdown_tokens(text=changelog.read_text())
    release_md_tokens = get_latest_release_section(tokens=tokens)
    release_md_tokens = replace_pr_links(release_md_tokens)
    text = render_md_tokens(release_md_tokens)
    return text


def log_release_text(text: str) -> None:
    print("EXTRACTED RELEASE NOTES:")
    print("⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇")
    print(text)
    print("⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆")


def main() -> None:
    text = extract_latest_release_notes(changelog=PATH_TO_CHANGELOG)
    log_release_text(text)
    PATH_TO_LATEST_RELEASE_NOTES.write_text(text)


if __name__ == "__main__":
    main()
