#!/usr/bin/env python
from importlib import import_module
from pathlib import Path
from typing import cast

import plotly.graph_objects as go
from bs4 import BeautifulSoup
from minify_html import minify
from plotly.offline import get_plotlyjs

from ridgeplot._testing import patch_plotly_show

PATH_DOCS = Path(__file__).parent
assert PATH_DOCS.exists()
assert PATH_DOCS.is_dir()
assert PATH_DOCS.name == "docs"
PATH_EXAMPLES = PATH_DOCS / "_examples"
PATH_CHARTS = PATH_DOCS / "_static/charts"


def _compile_plotly_fig(example_script: Path, minify_html: bool = True) -> None:
    plot_id = example_script.stem

    print(f"Getting the Plotly Figure from: {example_script}...")
    example_module = import_module(f"_examples.{plot_id}")
    main_func = example_module.main
    fig = cast(go.Figure, main_func())

    width = fig.layout.width
    height = fig.layout.height
    assert isinstance(width, int)
    assert isinstance(height, int)

    # Reduce the figure's margins to more tightly fit the chart
    # (only if the user hasn't already customized the margins!)
    if fig.layout.margin == go.layout.Margin():
        t = None if fig.layout.title.text else 40
        fig = fig.update_layout(margin=dict(l=0, r=0, t=t, b=40))

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

    out_path = PATH_CHARTS / f"{plot_id}.html"
    print(f"Writing HTML artefact to {out_path}...")
    out_path.write_text(html_str, "utf-8")

    out_image = PATH_CHARTS / f"{plot_id}.webp"
    print(f"Writing WebP artefact to {out_image}...")
    fig.write_image(
        out_image,
        format="webp",
        width=width,
        height=height,
        scale=3,
        engine="kaleido",
    )


def _write_plotlyjs_bundle() -> None:
    bundle_path = PATH_DOCS / "_static/js/plotly.min.js"
    plotlyjs = get_plotlyjs()
    bundle_path.write_text(plotlyjs, encoding="utf-8")


def compile_plotly_charts() -> None:
    # print("Writing Plotly.js bundle...")
    # _write_plotlyjs_bundle()
    print("Patching `plotly.show()`...")
    patch_plotly_show()
    for example_script in PATH_EXAMPLES.glob("*.py"):
        _compile_plotly_fig(example_script)


def main() -> None:
    compile_plotly_charts()


if __name__ == "__main__":
    main()
