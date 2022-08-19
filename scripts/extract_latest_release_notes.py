from pathlib import Path
from typing import List, Sequence

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdformat.renderer import MDRenderer

PATH_TO_TOP_LEVEL = Path(__file__).parent.parent
PATH_TO_CHANGES = PATH_TO_TOP_LEVEL.joinpath("CHANGES.md")
PATH_TO_CHANGES_LATEST = PATH_TO_TOP_LEVEL.joinpath("CHANGES-latest.md")


def get_tokens_latest_release() -> List[Token]:
    md_parser = MarkdownIt()
    tokens = md_parser.parse(src=PATH_TO_CHANGES.read_text())

    count_h2 = 0
    tokens_latest_release: List[Token] = []

    for token in tokens:
        if token.type == "heading_open" and token.tag == "h2":
            count_h2 += 1
        if count_h2 > 2:
            break
        elif count_h2 == 2:
            tokens_latest_release.append(token)

    return tokens_latest_release


def render_release_text(tokens: Sequence[Token]) -> str:
    md_renderer = MDRenderer()
    return md_renderer.render(tokens=tokens, options={}, env={})


def main() -> None:
    latest_release_tokens = get_tokens_latest_release()
    md_renderer = MDRenderer()
    release_text = md_renderer.render(tokens=latest_release_tokens, options={}, env={})
    PATH_TO_CHANGES_LATEST.write_text(data=release_text)


if __name__ == "__main__":
    main()
