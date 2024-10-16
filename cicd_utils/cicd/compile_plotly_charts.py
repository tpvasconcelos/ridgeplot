#!/usr/bin/env python
"""Compile Plotly charts to HTML and WebP artefacts.

This script is used by `conf.py::setup(app)` to (re-)compile the Plotly charts
used in the docs. It saves the HTML and WebP artefacts to the
`docs/_static/charts` directory.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from minify_html import minify
from plotly.offline import get_plotlyjs

from ridgeplot_examples import ALL_EXAMPLES, tighten_margins

if TYPE_CHECKING:
    import plotly.graph_objects as go


PATH_ROOT_DIR = Path(__file__).parents[2]
PATH_DOCS = PATH_ROOT_DIR / "docs"
PATH_STATIC_CHARTS = PATH_DOCS / "_static/charts"
PATH_STATIC_JS = PATH_DOCS / "_static/js"


def _to_html(fig: go.Figure, plot_id: str, minify_html: bool) -> None:
    fig = deepcopy(fig)

    if fig.layout.height is None:
        raise ValueError("The Figure's layout.height value must be explicitly set.")
    # Overriding the width to None results in a '100%' CSS width.
    # This is achieved by setting the `default_width` parameter
    # in `fig.to_html()` to "100%" (see below).
    fig.layout.width = None

    fig = tighten_margins(fig)

    # Plotly.js (and MathJax.jsm if needed) should be included HTML's <head>
    # of the Sphinx documentation. This can be done using the `html_js_files`
    # configuration option in `conf.py`. For pages with multiple Plotly charts,
    # this method is more efficient than including the Plotly.js (+ MathJax.js)
    # source code in each HTML artefact. See `include_plotlyjs` below.
    html_str = fig.to_html(
        include_plotlyjs=False,
        include_mathjax=False,
        full_html=False,
        default_width="100%",
        div_id=f"plotly-id-{plot_id}",
    )

    # Wrap the chart's HTML in a <div> tag with a custom class name
    # to allow for custom styling in the Sphinx documentation.
    # See: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_css_files
    wrapper_div_class = "plotly-graph-wrapper"
    html_str = f'<div class="{wrapper_div_class}">{html_str}</div>'
    if minify_html:
        # Need to set `minify_js` to False to avoid breaking
        # the inner HTML set in the `hovertemplate` attribute
        # TODO: Investigate if this is still necessary or find a workaround
        #       (reason: minify_js seems to make a significant difference)
        html_str = minify(html_str, minify_js=False)

    out_path = PATH_STATIC_CHARTS / f"{plot_id}.html"
    print(f"Writing HTML artefact to {out_path}...")
    out_path.write_text(html_str, "utf-8")


def _to_webp(fig: go.Figure, plot_id: str) -> None:
    out_image = PATH_STATIC_CHARTS / f"{plot_id}.webp"
    print(f"Writing WebP artefact to {out_image}...")
    fig.write_image(
        out_image,
        format="webp",
        width=fig.layout.width,
        height=fig.layout.height,
        scale=3,
        engine="kaleido",
    )


def _compile_plotly_fig(
    plot_id: str,
    example_loader: Callable[[], go.Figure],
    minify_html: bool = True,
) -> None:
    fig = example_loader()
    _to_html(fig, plot_id=plot_id, minify_html=minify_html)
    _to_webp(fig, plot_id=plot_id)


def _write_plotlyjs_bundle() -> None:
    plotlyjs = get_plotlyjs()
    bundle_path = PATH_STATIC_JS / "plotly.min.js"
    print(f"Writing Plotly.js bundle to: {bundle_path}")
    if not bundle_path.parent.exists():
        bundle_path.parent.mkdir(parents=True)
    bundle_path.write_text(plotlyjs, encoding="utf-8")


def compile_plotly_charts() -> None:
    # Setup logic ---
    # _write_plotlyjs_bundle()

    # Compile all charts ---
    if not PATH_STATIC_CHARTS.exists():
        PATH_STATIC_CHARTS.mkdir(parents=True)
    for plot_id, example_loader in ALL_EXAMPLES:
        _compile_plotly_fig(plot_id=plot_id, example_loader=example_loader)


if __name__ == "__main__":
    compile_plotly_charts()
