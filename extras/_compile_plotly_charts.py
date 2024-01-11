#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable

from bs4 import BeautifulSoup
from minify_html import minify
from plotly.offline import get_plotlyjs

from _ridgeplot_examples import ALL_EXAMPLES, normalize

if TYPE_CHECKING:
    import plotly.graph_objects as go


PATH_DOCS = Path(__file__).parent.parent / "docs"


def _compile_plotly_fig(
    plot_id: str,
    example_loader: Callable[[], go.Figure],
    minify_html: bool = True,
) -> None:
    fig = example_loader()
    fig = normalize(fig)

    html_str = fig.to_html(
        include_plotlyjs="/_static/js/plotly.min.js",
        full_html=False,
        div_id=f"plotly-id-{plot_id}",
    )

    # Wrap the Plotly HTML in a <div> tag with a .plotly-graph-wrapper class
    soup = BeautifulSoup(html_str, "html.parser")
    soup.div["class"] = "plotly-graph-wrapper"  # type: ignore[index]
    html_str = str(soup)

    if minify_html:
        html_str = minify(html_str, minify_js=True)

    out_path = PATH_DOCS / f"_static/charts/{plot_id}.html"
    print(f"Writing HTML artefact to {out_path}...")
    out_path.write_text(html_str, "utf-8")

    out_image = PATH_DOCS / f"_static/charts/{plot_id}.webp"
    print(f"Writing WebP artefact to {out_image}...")
    fig.write_image(
        out_image,
        format="webp",
        width=fig.layout.width,
        height=fig.layout.height,
        scale=3,
        engine="kaleido",
    )


def _write_plotlyjs_bundle() -> None:
    plotlyjs = get_plotlyjs()
    bundle_path = PATH_DOCS / "_static/js/plotly.min.js"
    bundle_path.write_text(plotlyjs, encoding="utf-8")


def compile_plotly_charts() -> None:
    print("Writing Plotly.js bundle...")
    _write_plotlyjs_bundle()
    for plot_id, example_loader in ALL_EXAMPLES:
        _compile_plotly_fig(plot_id=plot_id, example_loader=example_loader)


if __name__ == "__main__":
    compile_plotly_charts()
