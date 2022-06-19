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
version = metadata["version"]
copyright = f"2021 - {datetime.today().year}, {author}"

master_doc = "index"
language = "en"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "numpydoc",
    "sphinxext.opengraph",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
    "sphinx_thebe",
    "sphinx_togglebutton",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "**.ipynb_checkpoints", "*/autosummary/*.rst", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "sphinx_book_theme"
html_title = project_name
html_short_title = project_name

html_favicon = "_static/favicon.ico"  # 32x32 pixel .ico file
# html_logo = "_static/images/logo.svg"
html_sourcelink_suffix = ""
html_last_updated_fmt = ""

project_urls = [(n[:-1], url) for n, url in map(str.split, metadata.get_all("project-url"))]
repo_url = [url for n, url in project_urls if n == "Source"][0]
docs_url = [url for n, url in project_urls if n == "Documentation"][0]

html_theme_options = {
    "repository_url": docs_url,
    "path_to_docs": "docs",
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "colab_url": "https://colab.research.google.com/",
        "deepnote_url": "https://deepnote.com/",
        "notebook_interface": "jupyterlab",
        "thebe": True,
    },
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "use_download_button": True,
    # "logo_only": True,
    "show_toc_level": 2,
    # "announcement": (
    #     "⚠️The latest release refactored our HTML, "
    #     "so double-check your custom CSS rules!⚠️"
    # ),
}

# ghissue config
# github_project_url = repo_url

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {"**": ["html_sidebars.html"]}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

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

# myst
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "colon_fence",
    "tasklist",
    "deflist",
    "substitution",
]
myst_dmath_double_inline = True
myst_heading_anchors = (
    2  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#auto-generated-header-anchors
)
myst_substitutions = {"some_jinja2_key": "value"}

from jinja2.defaults import DEFAULT_NAMESPACE  # noqa: E402

DEFAULT_NAMESPACE.update(
    {
        "repo_file": lambda file_name: f"[{file_name}]({repo_url}/blob/master/{file_name})",
        "repo_dir": lambda dir_name: f"[{dir_name}]({repo_url}/tree/master/{dir_name})",
    },
)
