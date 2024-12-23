from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING

import plotly.graph_objects as go
from minify_html import minify

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


def tighten_margins(fig: go.Figure, px: int = 0) -> go.Figure:
    """Tighten the margins of a Plotly figure."""
    if fig.layout.margin != go.layout.Margin():
        # If the Figure's margins are different from the default values,
        # we'll assume that the user has set these values intentionally
        return fig
    # If the Figure does not have a title, we'll leave 40px of space at the
    # top to account for the Plotly toolbar. If the Figure does include
    # a title, we'll leave the top margin with the default value.
    margin_top = None if fig.layout.title.text else max(40, px)
    return fig.update_layout(margin=dict(l=px, r=px, t=margin_top, b=px))


def _round_sig_figs(x: float, sig_figs: int) -> float:
    """Round a float value to a fixed number of significant figures."""
    return float(f"{x:.{sig_figs}g}")


def round_fig_data(fig: go.Figure, sig_figs: int) -> go.Figure:
    """Round the float values in the data of a Plotly figure."""
    for i, trace in enumerate(fig.data):
        fig.data[i].x = [_round_sig_figs(x, sig_figs) for x in trace.x]
        fig.data[i].y = [_round_sig_figs(y, sig_figs) for y in trace.y]
    return fig


@dataclass
class Example:
    plot_id: str
    figure_factory: Callable[[], go.Figure]

    def __post_init__(self) -> None:
        self.fig = self.figure_factory()  # pyright: ignore[reportUninitializedInstanceVariable]

    def to_html(self, path: Path, minify_html: bool) -> None:
        fig = deepcopy(self.fig)

        if fig.layout.height is None:
            raise ValueError("The Figure's layout.height value must be explicitly set.")
        # Overriding the width to None results in a '100%' CSS width.
        # This is achieved by setting the `default_width` parameter
        # in `fig.to_html()` to "100%" (see below).
        fig.layout.width = None

        fig = tighten_margins(fig)

        # Plotly.js (and MathJax.js if needed) should be included HTML's <head>
        # of the Sphinx documentation. This can be done using the `html_js_files`
        # configuration option in `conf.py`. For pages with multiple Plotly charts,
        # this method is more efficient than including the Plotly.js (+ MathJax.js)
        # source code in each HTML artefact. See `include_plotlyjs` below.
        html_str = fig.to_html(
            include_plotlyjs=False,
            include_mathjax=False,
            full_html=False,
            default_width="100%",
            div_id=f"plotly-id-{self.plot_id}",
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

        if not path.exists():
            path.mkdir(parents=True)
        out_path = path / f"{self.plot_id}.html"
        out_path.write_text(html_str, "utf-8")

    def to_webp(self, path: Path) -> None:
        fig = deepcopy(self.fig)
        fig = tighten_margins(fig, px=40)
        if not path.exists():
            path.mkdir(parents=True)
        out_image = path / f"{self.plot_id}.webp"
        fig.write_image(
            out_image,
            format="webp",
            width=fig.layout.width,
            height=fig.layout.height,
            scale=3,
            engine="kaleido",
        )

    def to_jpeg(self, path: Path) -> None:
        fig = deepcopy(self.fig)
        fig = tighten_margins(fig, px=40)
        if not path.exists():
            path.mkdir(parents=True)
        out_image = path / f"{self.plot_id}.jpeg"
        fig.write_image(
            out_image,
            format="jpeg",
            width=fig.layout.width,
            height=fig.layout.height,
            scale=1,
            engine="kaleido",
        )

    def to_json(self, path: Path, sig_figs: int) -> None:
        # We'll round the float values in the JSON to a fixed number of
        # significant figures to make the regression tests more robust.
        round_fig_data(self.fig, sig_figs=sig_figs)
        if not path.exists():
            path.mkdir(parents=True)
        out_path = path / f"{self.plot_id}.json"
        out_path.write_text(self.fig.to_json(), "utf-8")
