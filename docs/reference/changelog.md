# Release Notes

This document outlines the list of changes to ridgeplot between each release. For full details, see the [commit logs](https://github.com/tpvasconcelos/ridgeplot/commits/).

Unreleased changes
------------------

- ...

---

0.2.0
------

After almost 4 years, 30 _"patch"_ releases, +200 pull-requests, and close to 1,000 commits, this is ridgeplot's first _minor_ release (`v0.1.30 -> v0.2.0`)! 🚀

ridgeplot has been downloaded [over 400k times](https://pepy.tech/projects/ridgeplot) (peaking at [102k](https://pypistats.org/packages/ridgeplot) downloads in a single month), is listed as a dependency in [135](https://github.com/tpvasconcelos/ridgeplot/network/dependents?dependent_type=REPOSITORY) public GitHub repositories, and - perhaps most relevantly - is a dependency of larger projects such as [Shiny for Python](https://github.com/posit-dev/py-shiny), [Ploomber](https://github.com/ploomber), and [NiMARE](https://github.com/neurostuff/NiMARE) which further extends the impact and reach of the project.

This release marks a small milestone for ridgeplot, which we believe has now reached a level of maturity and stability that warrants a stricter and more structured, predictable, and standard release and versioning process. Even though we have managed to never publish breaking changes in the past (if you find any, please let us know!), we will from now on be even more careful and mindful of the impact of any changes that could affect downstream users and their applications.

We will make an effort to standardise and document our versioning policy. For now, we will try to simply adhere to the following general rules:

- We are explicitly **not** going to follow [Semantic Versioning](https://semver.org/), as we believe it is not a good fit for this project yet.
- `MAJOR.MINOR.PATCH` versioning scheme:
  - **MAJOR**: We don't have any plans for this yet... we will probably use this in the future once we settle on a more stable API and feature set
  - **MINOR**: New features, significant improvements, and deprecations
  - **PATCH**: Backwards-compatible bug fixes, small improvements, internal changes, and documentation updates
- **Breaking changes:**
  - **We might introduce breaking changes in minor releases!**
  - However, this will never happen without a proper deprecation period and a clear upgrade path. i.e., we will always first deprecate the old API via a `DeprecationWarning` and provide a clear migration path to the new API.
  - Such instances will be kept to a minimum and will likely only show up in the form of deprecated or renamed parameters or the meaning/behaviour of their arguments/values.

### Breaking changes

- Remove support for the deprecated `show_annotations` parameter and `colormode='index'` value ({gh-pr}`254`)
- The new default colormode is `"fillgradient"` ({gh-pr}`244`)
- The default value for `line_width` changed from `1` to `1.5` ({gh-pr}`253`)

### Features

- Implement new `"fillgradient"` colormode ({gh-pr}`244`)
- Add new `line_color` parameter to the `ridgeplot` function ({gh-pr}`253`)
- Add a `line_color='fill-color'` option which automatically matches the trace's line color to the trace's fill color ({gh-pr}`253`)
- Add new `norm` parameter to the `ridgeplot` function to allow users to normalize the data before plotting ({gh-pr}`255`)
- Add `sample_weights` argument to `ridgeplot()` to allow users to pass sample weights to the KDE estimator ({gh-pr}`259`)

### Deprecations

- Rename `coloralpha` to `opacity` for consistently with Plotly Express and deprecate the old parameter name ({gh-pr}`245`)
- Rename `linewidth` to `line_width` for consistency with Plotly's API and deprecate the old parameter name ({gh-pr}`253`)

### Dependencies

- The new minimum version of Plotly is `5.20` to leverage the new `fillgradient` feature ({gh-pr}`244`)

### Optimizations

- Importing statsmodels, scipy, and numpy can be slow, so we now only import the `ridgeplot._kde` module when the user needs this functionality ({gh-pr}`242`)

### Documentation

- Update examples in the getting-started guide to reflect the new default colormode ({gh-pr}`244`)
- Update the `plotly.min.js` version from `2.27` to `2.35.2` to leverage the `fillgradient` feature ({gh-pr}`244`)
- Fix the API reference docs for the internal `ridgeplot._color` module ({gh-pr}`244`)
- Tighten margins in generated examples ({gh-pr}`257`)
- Add the reference jupyter notebook used to generate the ridgeplot logo ({gh-pr}`242`)
- Update ridgeplot's logo to use Plotly's official colors ({gh-pr}`243`)

### CI/CD

- Stop sending coverage reports to Codacy ({gh-pr}`265`)
- Improve local development experience and optimise the CI pipeline ({gh-pr}`273`)

### Internal

- Simplify and refactor `interpolate_color` to not depend on `px.colors.find_intermediate_color` ({gh-pr}`253`)
- Improve type narrowing using `typing.TypeIs` ({gh-pr}`259`)
- Refactor community health files ({gh-pr}`260`)

Thanks to {gh-user}`sstephanyy` for their contributions to this release! 🚀

---

0.1.30
------

### Features

- Add support for named CSS colors ({gh-pr}`229`)
- Allow users to define color scales as a collection of colors. (`Collection[Color]`) ({gh-pr}`231`)
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

- Dropped support for Python 3.8, in accordance with the official Python support policy[^1] ({gh-pr}`204`)
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

- Dropped support for `statsmodels==0.14.2` due to import-time issue. See {gh-issue}`197` for more details ({gh-pr}`198`)

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

- Dropped support for Python 3.7, in accordance with the official Python support policy[^1] ({gh-pr}`154`)

### Features

- Add hoverinfo by default to the Plotly traces ({gh-pr}`174`)

### Documentation

- Use the `{raw} html :file: _static/charts/<PLOT-ID>.html` directive to load the interactive Plotly graphs in the generated Sphinx docs. The generated HTML artefacts only include a `<div>` wrapper block now and the plotly.min.js is now vendored and automatically loaded via the `html_js_files` Sphinx config ({gh-pr}`132`)
- Small adjustments to the example plots in the documentation ({gh-pr}`132`)
- Reformat markdown files, removing all line breaks ({gh-pr}`132`)

### Internals

- Define a `ridgeplot._missing.MISSING` sentinel object for internal use (this replaces the multiple module-level `_MISSING = object()` sentinels) ({gh-pr}`154`)
- Add an internal `extras/` directory to place helper modules and packages used in different CI tasks ({gh-pr}`154` and {gh-pr}`161`)

### CI/CD

- Replace `isort`, `flake8`, and `pyupgrade` with `ruff` ({gh-pr}`131`)
- Add regression tests for the figure artifacts generated by the examples in `ridgeplot_examples` ({gh-pr}`154`)
- Remove the Python locked dependency files ({gh-pr}`163`)

---

0.1.23
------

- Fix the references to the interactive Plotly IFrames ({gh-pr}`129`)

---

0.1.22
------

### Deprecations

- The `colormode='index'` value has been deprecated in favor of `colormode='row-index'`, which provides the same functionality but is more explicit and allows to distinguish between the `'row-index'` and `'trace-index'` modes ({gh-pr}`114`)
- The `show_annotations` argument has been deprecated in favor of `show_yticklabels` ({gh-pr}`114`)
- The `get_all_colorscale_names()` function has been deprecated in favor of `list_all_colorscale_names()` ({gh-pr}`114`)
- Deprecated `colorscale='default'` and `list_all_colorscale_names()` in favour of Plotly Express' `px.colors.named_colorscales()` ({gh-pr}`262`)

### Features

- Add functionality to allow plotting of multiple traces per row ({gh-pr}`114`)
- Add `ridgeplot.datasets.load_lincoln_weather()` helper function to load the "Lincoln Weather" toy dataset ({gh-pr}`114`)
- Add more versions of the _probly_ dataset (`"wadefagen"` and `"illinois"`) ({gh-pr}`114`)
- Add support for Python 3.11.

### Documentation

- Major update to the documentation, including more examples, interactive plots, script to generate the HTML and WebP images from the example scripts, improved API reference, and more ({gh-pr}`114`)

### Internal

- Remove `mdformat` from the automated CI checks. It can still be triggered manually ({gh-pr}`114`)
- Improved type annotations and type checking ({gh-pr}`114`)

---

0.1.21
------

### Features

- Add `ridgeplot.datasets.load_probly()` helper function to load the `probly` toy dataset. The `probly.csv` file is now included in the package under `ridgeplot/datasets/data/` ({gh-pr}`80`)

### Documentation

- Change to numpydoc style docstrings ({gh-pr}`81`)
- Add a robots.txt to the docs site ({gh-pr}`81`)
- Auto-generate a site map for the docs site using `sphinx_sitemap` ({gh-pr}`81`)
- Change the sphinx theme to `furo` ({gh-pr}`81`)
- Improve the internal documentation and some of these internals to the API reference ({gh-pr}`81`)

### Internal

- Fixed and improved some type annotations, including the introduction of `ridgeplot._types` module for type aliases such as `Numeric` and `NestedNumericSequence` ({gh-pr}`80`)
- Add the `blacken-docs` pre-commit hook and add the `pep8-naming`, `flake8-pytest-style`, `flake8-simplify`, `flake8-implicit-str-concat`, `flake8-bugbear`, `flake8-rst-docstrings`, `flake8-rst-docstrings`, etc... plugins to the `flake8` pre-commit hook ({gh-pr}`81`)
- Cleanup and improve some type annotations ({gh-pr}`81`)
- Update deprecated `set-output` commands (GitHub Actions) ({gh-pr}`87`)

---

0.1.17
------

- Automate the release process. See .github/workflows/release.yml, which issues a new GitHub release whenever a new git tag is pushed to the main branch by extracting the release notes from the changelog.
- Fix automated release process to PyPI ({gh-pr}`27`)

---

0.1.16
------

- Upgrade project structure, improve testing and CI checks, and start basic Sphinx docs ({gh-pr}`21`)
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
