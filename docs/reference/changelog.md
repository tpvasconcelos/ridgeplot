# Release Notes

This document outlines the list of changes to ridgeplot between each release. For full details, see the [commit logs](https://github.com/tpvasconcelos/ridgeplot/commits/).

Unreleased changes
------------------

- ...

---

0.1.30
------

### Features

- Add support for named CSS colors ({gh-pr}`229`)
- Allow users to define color scales as a collection of colors (`Collection[Color]`) ({gh-pr}`231`)
- Dynamically infer the default colorscale from the active Plotly template ({gh-pr}`237`)


### Documentation

- Improve the documentation for the `colormode` parameter ({gh-pr}`232`)

### Internal

- Refactor `_figure_factory.py` to use a functional approach ({gh-pr}`228`)
- Stop using the term "midpoints" to refer to the "interpolation values" when dealing with continuous color scales ({gh-pr}`232`)
- Refactor color validation logic to use helpers provided by Plotly ({gh-pr}`233`)
- Drop `colors.json` and use Plotly's `ColorscaleValidator` and `named_colorscales` directly ({gh-pr}`234`)
- Refactor color utilities into `ridgeplot._color` ({gh-pr}`235`)

---

0.1.29
------

### Features

- Add new `"trace-index-row-wise"` colormode ({gh-pr}`224`)

### Improvements

- Remove duplicated labels when plotting multiple traces on the same y-axis row ({gh-pr}`223`)

### Documentation

- Update and improve the "Contributing" guide ({gh-pr}`218` and {gh-pr}`221`)

### Internal

- Eagerly validate input shapes in `RidgeplotFigureFactory` ({gh-pr}`222`)
- Vendor `_zip_equal()` from [more-itertools](https://github.com/more-itertools/more-itertools/) ({gh-pr}`222`)
- Improve overall test coverage ({gh-pr}`222`)

### Bug fixes

- Support edge case in `get_collection_array_shape` where the input array is empty or contains nested empty arrays ({gh-pr}`222`)

### CI/CD

- Add new `"Greet new users"` workflow to welcome new contributors to the project ({gh-pr}`210`)
- Add `concurrency` entries to relevant GitHub workflows ({gh-pr}`211`)
- Add Dependabot configuration file ({gh-pr}`211`)
- Add GitHub issue templates ({gh-pr}`211`)
- Add support for Python 3.13 ({gh-pr}`217`)
- Add a CodeQL GitHub workflow ({gh-pr}`220`)

---

~~0.1.28~~
----------

- Ooops! This release was skipped due to a mistake in the release process. The changes in this release were included in the 0.1.29 release.

---

0.1.27
------

### Breaking changes

- Dropped support for Python 3.8, in accordance with the official Python support policy[^1]. ({gh-pr}`204`)
- Removed deprecated function `get_all_colorscale_names()` in favor of `list_all_colorscale_names()` ({gh-pr}`200`)

### CI/CD

- Adopt `setuptools-scm` for package versioning ({gh-pr}`200`)
- Add `actionlint` pre-commit hook ({gh-pr}`201`)
- Improve logic in `.github/workflows/check-release-notes.yml` to post comments to the PR ({gh-pr}`201`)
- Handle footnotes in the automatically generated release notes ({gh-pr}`209`)

---

0.1.26
------

### Breaking changes

- Dropped support for `statsmodels==0.14.2` due to import-time issue. See {gh-issue}`197` for more details. ({gh-pr}`198`)

### CI/CD

- Refactor test coverage logic ({gh-pr}`193`)
- Replace `pip` and `venv` with `uv` ({gh-pr}`189`)
- Move all CI/CD utilities to the `cicd_utils/` directory ({gh-pr}`186`)
- Publish to PyPi as a Trusted Publisher ({gh-pr}`187`)
- Add `check-jsonschema` pre-commit hooks and define `timeout-minutes` for all GitHub workflows ({gh-pr}`187`)

---

0.1.25
------

This release contains a number of improvements to the docs, API reference, CI/CD logic (incl. official support for Python 3.12), and other minor internal changes.

### Documentation

- Misc documentation improvements ({gh-pr}`180`)
- Move changelog to `./docs/reference/changelog.md` ({gh-pr}`180`)

### Internals

- Migrate from `setup.cfg` from `pyproject.toml` ({gh-pr}`176`)
- Use `importlib.resources` to load data assets from within the package - to be PEP-302 compliant ({gh-pr}`176`)
- Enforce "strict" mypy mode (mostly improved type annotations for generic types) ({gh-pr}`177`)

### CI/CD

- Add support for Python 3.12 ({gh-pr}`182`)

---

0.1.24
------

### Breaking changes

- Dropped support for Python 3.7, in accordance with the official Python support policy[^1]. ({gh-pr}`154`)

### Features

- Add hoverinfo by default to the Plotly traces. ({gh-pr}`174`)

### Documentation

- Use the `{raw} html :file: _static/charts/<PLOT-ID>.html` directive to load the interactive Plotly graphs in the generated Sphinx docs. The generated HTML artefacts only include a `<div>` wrapper block now and the plotly.min.js is now vendored and automatically loaded via the `html_js_files` Sphinx config. ({gh-pr}`132`)
- Small adjustments to the example plots in the documentation. ({gh-pr}`132`)
- Reformat markdown files, removing all line breaks. ({gh-pr}`132`)

### Internals

- Define a `ridgeplot._missing.MISSING` sentinel object for internal use (this replaces the multiple module-level `_MISSING = object()` sentinels). ({gh-pr}`154`)
- Add an internal `extras/` directory to place helper modules and packages used in different CI tasks. ({gh-pr}`154` and {gh-pr}`161`)

### CI/CD

- Replace `isort`, `flake8`, and `pyupgrade` with `ruff`. ({gh-pr}`131`)
- Add regression tests for the figure artifacts generated by the examples in `ridgeplot_examples`. ({gh-pr}`154`)
- Remove the Python locked dependency files. ({gh-pr}`163`)

---

0.1.23
------

- Fix the references to the interactive Plotly IFrames ({gh-pr}`129`)

---

0.1.22
------

### Deprecations

- The `colormode='index'` value has been deprecated in favor of `colormode='row-index'`, which provides the same functionality but is more explicit and allows to distinguish between the `'row-index'` and `'trace-index'` modes. ({gh-pr}`114`)
- The `show_annotations` argument has been deprecated in favor of `show_yticklabels`. ({gh-pr}`114`)
- The `get_all_colorscale_names()` function has been deprecated in favor of `list_all_colorscale_names()`. ({gh-pr}`114`)

### Features

- Add functionality to allow plotting of multiple traces per row. ({gh-pr}`114`)
- Add `ridgeplot.datasets.load_lincoln_weather()` helper function to load the "Lincoln Weather" toy dataset. ({gh-pr}`114`)
- Add more versions of the _probly_ dataset (`"wadefagen"` and `"illinois"`). ({gh-pr}`114`)
- Add support for Python 3.11.

### Documentation

- Major update to the documentation, including more examples, interactive plots, script to generate the HTML and WebP images from the example scripts, improved API reference, and more. ({gh-pr}`114`)

### Internal

- Remove `mdformat` from the automated CI checks. It can still be triggered manually. ({gh-pr}`114`)
- Improved type annotations and type checking. ({gh-pr}`114`)

---

0.1.21
------

### Features

- Add `ridgeplot.datasets.load_probly()` helper function to load the `probly` toy dataset. The `probly.csv` file is now included in the package under `ridgeplot/datasets/data/`. ({gh-pr}`80`)

### Documentation

- Change to numpydoc style docstrings. ({gh-pr}`81`)
- Add a robots.txt to the docs site. ({gh-pr}`81`)
- Auto-generate a site map for the docs site using `sphinx_sitemap`. ({gh-pr}`81`)
- Change the sphinx theme to `furo`. ({gh-pr}`81`)
- Improve the internal documentation and some of these internals to the API reference. ({gh-pr}`81`)

### Internal

- Fixed and improved some type annotations, including the introduction of `ridgeplot._types` module for type aliases such as `Numeric` and `NestedNumericSequence`. ({gh-pr}`80`)
- Add the `blacken-docs` pre-commit hook and add the `pep8-naming`, `flake8-pytest-style`, `flake8-simplify`, `flake8-implicit-str-concat`, `flake8-bugbear`, `flake8-rst-docstrings`, `flake8-rst-docstrings`, etc... plugins to the `flake8` pre-commit hook. ({gh-pr}`81`)
- Cleanup and improve some type annotations. ({gh-pr}`81`)
- Update deprecated `set-output` commands (GitHub Actions) ({gh-pr}`87`)

---

0.1.17
------

- Automate the release process. See .github/workflows/release.yml, which issues a new GitHub release whenever a new git tag is pushed to the main branch by extracting the release notes from the changelog.
- Fix automated release process to PyPI. ({gh-pr}`27`)

---

0.1.16
------

- Upgrade project structure, improve testing and CI checks, and start basic Sphinx docs. ({gh-pr}`21`)
- Implement `LazyMapping` helper to allow `ridgeplot._colors.PLOTLY_COLORSCALES` to lazy-load from `colors.json` ({gh-pr}`20`)

---

0.1.14
------

- Remove `named_colorscales` from public API ({gh-pr}`18`)

---

0.1.13
------

- Add tests for example scripts ({gh-pr}`14`)

---

0.1.12
------

### Internal

- Update and standardise CI steps ({gh-pr}`6`)

### Documentation

- Publish official contribution guidelines (`CONTRIBUTING.md`) ({gh-pr}`8`)
- Publish an official Code of Conduct (`CODE_OF_CONDUCT.md`) ({gh-pr}`7`)
- Publish an official release/change log (`CHANGES.md`) ({gh-pr}`6`)

---

0.1.11
------

- `colors.json` was missing from the final distributions ({gh-pr}`2`)

---

0.1.0
------

- 🚀 Initial release!

---

[^1]: <https://devguide.python.org/versions/>
