from __future__ import annotations

import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata  # type: ignore[no-redef]

try:
    from cicd.compile_plotly_charts import compile_plotly_charts
except ImportError:
    # When this script is run from the readthedocs build server,
    # the `cicd` package will not be available because
    # the `cicd_utils` dir is not in the PYTHONPATH.
    sys.path.append((Path(__file__).parents[1] / "cicd_utils").resolve().as_posix())
    from cicd.compile_plotly_charts import compile_plotly_charts

if TYPE_CHECKING:
    from collections.abc import Generator

    from sphinx.application import Sphinx

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# For more on MyST (Markedly Structured Text), see the documentation:
# https://myst-parser.readthedocs.io/en/latest/index.html


# -- Project information ---------------------------------------------------------------------------

metadata = importlib_metadata.metadata("ridgeplot")

project = project_name = name = metadata["name"]
author = metadata["author"]
release = metadata["version"]
version = ".".join(release.split(".")[:2])
copyright = project_copyright = f"2021 - {datetime.today().year}, {author}"  # noqa: DTZ002, A001

master_doc = "index"
language = "en"


# -- General configuration -------------------------------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "notfound.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    # NOTE: 'sphinx_autodoc_typehints' should be loaded after
    #       'sphinx.ext.autodoc' and 'sphinx.ext.napoleon'
    # "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
    "sphinx_paramlinks",
    "sphinx_remove_toctrees",
    "sphinx_sitemap",
    "sphinx_thebe",
    "sphinx_togglebutton",
    "sphinx_toolbox.collapse",
    "sphinx_toolbox.more_autodoc.autoprotocol",
    "sphinx_toolbox.more_autodoc.generic_bases",
    "sphinxext.opengraph",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

html_extra_path = ["robots.txt"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "**.ipynb_checkpoints",
    "*/autosummary/*.rst",
    "Thumbs.db",
    ".DS_Store",
]

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {"**": ["html_sidebars.html"]}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "css/misc_overrides.css",
    "css/versionmodified_admonitions.css",
    # FontAwesome CSS for footer icons
    # https://fontawesome.com/search
    # "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/brands.min.css",
]

# NOTE: When using the 'furo' theme, the `html_js_files` will be placed at
#       the bottom of the page.
#       See: https://github.com/pradyunsg/furo/blob/01887051504bbec32e241af9cebcf5cd10f656d1/src/furo/theme/furo/base.html#L91-L96
#       If you want to place the JS files at the top of the page, you can use
#       extend the `_templates/base.html` file and place the JS files in the
#       `extrahead` block (which should be included in the <head> tab).
# html_js_files = []

# nitpicky mode options
nitpicky = True
nitpick_ignore: list[tuple[str, str]] = []

# -- Options for HTML output -----------------------------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "furo"
html_title = f"{project_name} docs ({release})"
html_short_title = project_name

html_favicon = "_static/favicon.ico"  # 32x32 pixel .ico file
html_logo = "_static/img/logo-wide.png"
html_sourcelink_suffix = ""
html_last_updated_fmt = "%B %d, %Y"

meta_project_urls = metadata.get_all("project-url")
if meta_project_urls is None:
    raise ValueError("No 'project_urls' metadata found in 'pyproject.toml'")
project_urls = dict(url.split(", ") for url in meta_project_urls)
repo_url = project_urls["Source code"]
docs_url = project_urls["Documentation"]

html_theme_options = {
    "sidebar_hide_name": True,
    "source_repository": repo_url,
    "source_branch": "main",
    "source_directory": "docs/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": repo_url,
            "html": "",
            "class": "fa-brands fa-github fa-2x",
        },
    ],
}
# html_theme_options for the 'sphinx_book_theme' theme:
# html_theme_options = {
#     "repository_url": repo_url,
#     "path_to_docs": "docs",
#     "use_edit_page_button": True,
#     "use_issues_button": True,
#     "use_repository_button": True,
#     "use_download_button": True,
#     "show_toc_level": 2,
#     "logo_only": True,
#     # "launch_buttons": {
#     #     "binderhub_url": "https://mybinder.org",
#     #     "colab_url": "https://colab.research.google.com/",
#     #     "deepnote_url": "https://deepnote.com/",
#     #     "notebook_interface": "jupyterlab",
#     #     "thebe": True,
#     # },
#     # "announcement": (
#     #     "⚠️The latest release refactored our HTML, "
#     #     "so double-check your custom CSS rules!⚠️"
#     # ),
# }

# If true, figures, tables and code-blocks are automatically numbered if they have a caption
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-numfig
numfig = True

# A string of reStructuredText that will be included at the end of every source file that is
# read. This is a possible place to add substitutions that should be available in every file
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-rst_epilog
rst_epilog = """
.. |go.Figure| replace:: :class:`plotly.graph_objects.Figure`
.. |~go.Figure| replace:: :class:`~plotly.graph_objects.Figure`
"""


# -- ghissue  --------------------------------------------------------------------------------------
github_project_url = repo_url

# -- imgmath  --------------------------------------------------------------------------------------
# imgmath_image_format = "png"
# imgmath_latex_preamble = r"\usepackage[active]{preview}"
# imgmath_use_preview = True


# -- extlinks  -------------------------------------------------------------------------------------
extlinks = {
    "gh-issue": (f"{repo_url}/issues/%s", "#%s"),
    "gh-pr": (f"{repo_url}/pull/%s", "#%s"),
    "gh-discussion": (f"{repo_url}/discussions/%s", "#%s"),
    "gh-user": ("https://github.com/%s", "@%s"),
    "repo-file": (f"{repo_url}/blob/main/%s", "%s"),
    "repo-dir": (f"{repo_url}/tree/main/%s", "%s"),
}
extlinks_detect_hardcoded_links = True


# -- intersphinx  ----------------------------------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "packaging": ("https://packaging.pypa.io/en/latest", None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "statsmodels": ("https://www.statsmodels.org/stable/", None),
    "plotly": ("https://plotly.com/python-api-reference/", None),
}


# -- sphinx-sitemap --------------------------------------------------------------------------------
html_baseurl = docs_url
sitemap_url_scheme = "{link}"


# -- autodoc, napoleon, and autodoc-typehints ------------------------------------------------------

# autosectionlabel
autosectionlabel_prefix_document = True


# autodoc config
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
    "show-inheritance": True,
}
autodoc_typehints_description_target = "documented"


# autodoc-typehints config
# https://github.com/tox-dev/sphinx-autodoc-typehints
# typehints_use_rtype = True  # use w/ `napoleon_use_rtype` to avoid duplication
# typehints_defaults = "comma"
# always_document_param_types = True
# simplify_optional_unions = False


# Napoleon config
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = False
napoleon_use_param = False
# napoleon_use_rtype = False
napoleon_preprocess_types = True
napoleon_attr_annotations = True


# Type aliases
_TYPE_ALIASES_FULLY_QUALIFIED = {
    # ------- ._colormodes -------------------------
    "ridgeplot._color.interpolation.Colormode",
    "ridgeplot._color.interpolation.ColorscaleInterpolants",
    # ------- ._figure_factory ---------------------
    "ridgeplot._figure_factory.LabelsArray",
    "ridgeplot._figure_factory.ShallowLabelsArray",
    # ------- ._kde --------------------------------
    "ridgeplot._kde.KDEPoints",
    "ridgeplot._kde.KDEBandwidth",
    # ------- ._missing ----------------------------
    "ridgeplot._missing.MISSING",
    "ridgeplot._missing.MissingType",
    # ------- ._types ------------------------------
    "ridgeplot._colors.Color",
    "ridgeplot._colors.ColorScale",
    "ridgeplot._types.CollectionL1",
    "ridgeplot._types.CollectionL2",
    "ridgeplot._types.CollectionL3",
    "ridgeplot._types.Float",
    "ridgeplot._types.Int",
    "ridgeplot._types.Numeric",
    "ridgeplot._types.NumericT",
    "ridgeplot._types.XYCoordinate",
    "ridgeplot._types.DensityTrace",
    "ridgeplot._types.DensitiesRow",
    "ridgeplot._types.Densities",
    "ridgeplot._types.ShallowDensities",
    "ridgeplot._types.SamplesTrace",
    "ridgeplot._types.SamplesRow",
    "ridgeplot._types.Samples",
    "ridgeplot._types.ShallowSamples",
}
_TYPE_ALIASES = {fq.split(".")[-1]: fq for fq in _TYPE_ALIASES_FULLY_QUALIFIED}
autodoc_type_aliases = {
    **{a: a for a in _TYPE_ALIASES.values()},
    **{fq: fq for fq in _TYPE_ALIASES.values()},
}
napoleon_type_aliases = {a: f":data:`~{fq}`" for a, fq in _TYPE_ALIASES.items()}


# -- sphinx_remove_toctrees ------------------------------------------------------------------------
# Use the `sphinx_remove_toctrees` extension to remove auto-generated
# toctrees (generated by `autosummary`) from the main sidebar.
remove_from_toctrees = ["api/internal/*"]


# -- sphinx-paramlinks -----------------------------------------------------------------------------
paramlinks_hyperlink_param = "name"


# -- myst config -----------------------------------------------------------------------------------
myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "attrs_block",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "substitution",
    "strikethrough",
    "tasklist",
]
myst_dmath_double_inline = True
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#auto-generated-header-anchors
myst_heading_anchors = 2
myst_substitutions: dict[str, str] = {
    # "some_jinja2_key": "value",
}
suppress_warnings = [
    "myst.strikethrough",
]


# -- custom setup steps ------------------------------------------------------------


@contextmanager
def reset_sys_argv() -> Generator[None]:
    original_sys_argv = sys.argv
    sys.argv = original_sys_argv[:1]
    try:
        yield
    finally:
        sys.argv = original_sys_argv


def _fix_generated_public_api_rst() -> None:
    from pre_commit_hooks.end_of_file_fixer import main as end_of_file_fixer
    from pre_commit_hooks.fix_byte_order_marker import main as fix_byte_order_marker

    files = [file.resolve().as_posix() for file in Path("api/public/").glob("*.rst")]
    if not files:
        raise RuntimeError("No RST files found. Check that the path above is correct.")
    with reset_sys_argv():
        end_of_file_fixer(files)
        fix_byte_order_marker(files)


def _fix_html_charts() -> None:
    from pre_commit_hooks.end_of_file_fixer import main as end_of_file_fixer

    files = [file.resolve().as_posix() for file in Path("_static/charts/").glob("*.html")]
    if not files:
        raise RuntimeError("No HTML files found. Check that the path above is correct.")
    with reset_sys_argv():
        end_of_file_fixer(files)


def setup(app: Sphinx) -> None:
    compile_plotly_charts()
    # app.connect("html-page-context", register_jinja_functions)

    app.connect("build-finished", lambda *_: _fix_generated_public_api_rst())
    app.connect("build-finished", lambda *_: _fix_html_charts())
