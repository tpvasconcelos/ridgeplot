# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import importlib_metadata
import sphinx_material

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

metadata = importlib_metadata.metadata("ridgeplot")

project = metadata["name"]
author = metadata["author"]
version = metadata["version"]
copyright = "2021, Tomas Pereira de Vasconcelos"

master_doc = "index"
language = "en"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "nbsphinx",
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
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
#
extensions.append("sphinx_material")
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = "sphinx_material"
html_title = project
html_short_title = project

project_urls = [(n[:-1], url) for n, url in map(str.split, metadata.get_all("project-url"))]
repo_url = [url for n, url in project_urls if n == "Source"][0]
docs_url = [url for n, url in project_urls if n == "Documentation"][0]

html_theme_options = {
    "nav_title": f"{project} {version}",
    "base_url": docs_url,
    "repo_name": project,
    "repo_url": repo_url,
    # 'google_analytics_account': 'UA-XXXXX',
    "color_primary": "indigo",
    "color_accent": "blue",
    "globaltoc_depth": 3,
    "globaltoc_collapse": False,
    "globaltoc_includehidden": False,
    "html_minify": False,
    "html_prettify": True,
    "css_minify": True,
    "repo_type": "github",
    "master_doc": False,
    "nav_links": [],
    "version_dropdown": True,
}

# Custom sidebar templates, maps document names to template names.
html_sidebars = {"**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Logos
html_favicon = "_static/favicon.ico"  # 32x32 pixel .ico file
# html_logo = "_static/images/logo.svg"

# imgmath options
imgmath_image_format = "png"
imgmath_latex_preamble = r"\usepackage[active]{preview}"
imgmath_use_preview = True

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "python": ("https://docs.python.org/3/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
}

# ghissue config
github_project_url = repo_url


# Misc
html_last_updated_fmt = ""
html_domain_indices = True
