# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# For more on MyST (Markedly Structured Text), see the documentation:
# https://myst-parser.readthedocs.io/en/latest/index.html


# -- Project information -----------------------------------------------------
from datetime import datetime

import importlib_metadata

metadata = importlib_metadata.metadata("ridgeplot")

project = project_name = metadata["name"]
author = metadata["author"]
release = metadata["version"]
version = ".".join(release.split(".")[:2])
project_copyright = f"2021 - {datetime.today().year}, {author}"

master_doc = "index"
language = "en"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "notfound.extension",
    "sphinxext.opengraph",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    # "sphinx_autodoc_typehints",
    # "sphinx_toolbox.more_autodoc.typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
    "sphinx_thebe",
    "sphinx_togglebutton",
    "sphinx_toolbox.more_autodoc.autoprotocol",
    "sphinx_toolbox.more_autodoc.generic_bases",
    "sphinx_sitemap",
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

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "furo"
# html_title = project_name
html_short_title = project_name

html_favicon = "_static/favicon.ico"  # 32x32 pixel .ico file
html_logo = "_static/img/logo-wide.png"
html_sourcelink_suffix = ""
html_last_updated_fmt = ""

project_urls = [(n[:-1], url) for n, url in map(str.split, metadata.get_all("project-url"))]
repo_url = [url for n, url in project_urls if n == "Source"][0]
docs_url = [url for n, url in project_urls if n == "Documentation"][0]

html_css_files = [
    # FontAwesome CSS for footer icons
    # https://fontawesome.com/search
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/brands.min.css",
]

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

# ghissue config
github_project_url = repo_url

# imgmath options
# imgmath_image_format = "png"
# imgmath_latex_preamble = r"\usepackage[active]{preview}"
# imgmath_use_preview = True

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "statsmodels": ("https://www.statsmodels.org/stable/", None),
    "plotly": ("https://plotly.com/python-api-reference/", None),
}

# If true, figures, tables and code-blocks are automatically numbered if they have a caption
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-numfig
numfig = True

# sphinx-sitemap config
html_baseurl = docs_url
sitemap_url_scheme = "{link}"

# autodoc config
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_type_aliases = {
    "Numeric": "Numeric",
    "NumericT": "NumericT",
    "NestedNumericSequence": "NestedNumericSequence",
    "NestedNumericSequenceT": "NestedNumericSequenceT",
    "ColorScaleType": "ColorScaleType",
}

# autodoc-typehints config
# https://github.com/tox-dev/sphinx-autodoc-typehints
# typehints_document_rtype = False
# typehints_use_rtype = False
# typehints_defaults = "braces"

# Napoleon config
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_preprocess_types = True
napoleon_type_aliases = {
    "Numeric": ":data:`Numeric`",
    "NumericT": ":data:`NumericT`",
    "NestedNumericSequence": ":data:`NestedNumericSequence`",
    "NestedNumericSequenceT": ":data:`NestedNumericSequenceT`",
    "ColorScaleType": ":data:`ColorScaleType`",
}

# myst config
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "colon_fence",
    "tasklist",
    "deflist",
    "substitution",
]
myst_dmath_double_inline = True
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#auto-generated-header-anchors
myst_heading_anchors = 2
myst_substitutions = {"some_jinja2_key": "value"}

from jinja2.defaults import DEFAULT_NAMESPACE  # noqa: E402

DEFAULT_NAMESPACE.update(
    {
        "repo_file": lambda file_name: f"[{file_name}]({repo_url}/blob/main/{file_name})",
        "repo_dir": lambda dir_name: f"[{dir_name}]({repo_url}/tree/main/{dir_name})",
    },
)

rst_epilog = """
.. |go.Figure| replace:: :class:`plotly.graph_objects.Figure`
.. |~go.Figure| replace:: :class:`~plotly.graph_objects.Figure`
"""
