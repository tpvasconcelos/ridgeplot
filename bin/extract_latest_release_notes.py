#!/usr/bin/env python
"""Extract the latest release notes

Execution steps:
- Extracts the latest release notes from docs/reference/changelog.md
- The output is written to the `LATEST_RELEASE_NOTES.md` file.
- The body of this file is then used as the body of the GitHub release.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Sequence, cast

from markdown_it import MarkdownIt
from mdformat.renderer import MDRenderer

if TYPE_CHECKING:
    from markdown_it.token import Token

PATH_TO_TOP_LEVEL = Path(__file__).parent.parent
PATH_TO_CHANGES = PATH_TO_TOP_LEVEL.joinpath("docs/reference/changelog.md")
PATH_TO_LATEST_RELEASE_NOTES = PATH_TO_TOP_LEVEL.joinpath("LATEST_RELEASE_NOTES.md")


def _remove_heading(tokens: list[Token]) -> list[Token]:
    if tokens[0].type != "heading_open":
        raise ValueError("Expected first token to be a 'heading_open'")
    if tokens[2].type != "heading_close":
        raise ValueError("Expected third token to be a 'heading_close'")
    return tokens[3:]


def get_tokens_latest_release() -> list[Token]:
    md_parser = MarkdownIt()
    tokens = md_parser.parse(src=PATH_TO_CHANGES.read_text())

    count_h2 = 0
    tokens_latest_release: list[Token] = []
    for token in tokens:
        is_h2 = token.type == "heading_open" and token.tag == "h2"
        count_h2 += is_h2
        if count_h2 == 2:
            tokens_latest_release.append(token)
        elif count_h2 > 2:
            break

    return _remove_heading(tokens_latest_release)


def render_md_tokens(tokens: Sequence[Token]) -> str:
    md_renderer = MDRenderer()
    text = md_renderer.render(tokens=tokens, options={}, env={})
    return cast(str, text)


def log_release_text(text: str) -> None:
    print("EXTRACTED RELEASE NOTES:")
    print("⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇")
    print(text)
    print("⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆")


def main() -> None:
    release_md_tokens = get_tokens_latest_release()
    release_text = render_md_tokens(release_md_tokens)
    log_release_text(release_text)
    PATH_TO_LATEST_RELEASE_NOTES.write_text(release_text)


if __name__ == "__main__":
    main()
