# Release notes

This document outlines the list of changes to ridgeplot between each release. For full details, see
the [commit logs](https://github.com/tpvasconcelos/ridgeplot/commits/).

Unreleased changes
------------------

- ...

---

0.1.23
------

- Fix the references to the interactive Plotly IFrames
  ([#129](https://github.com/tpvasconcelos/ridgeplot/pull/129))

---

0.1.22
------

### Deprecations

- The `colormode='index'` value has been deprecated in favor of `colormode='row-index'`, which
  provides the same functionality but  is more explicit and allows to distinguish between the
  `'row-index'` and `'trace-index'` modes.
  ([#114](https://github.com/tpvasconcelos/ridgeplot/pull/114))
- The `show_annotations` argument has been deprecated in favor of `show_yticklabels`.
  ([#114](https://github.com/tpvasconcelos/ridgeplot/pull/114))
- The `get_all_colorscale_names()` function has been deprecated in favor of
  `list_all_colorscale_names()`.
  ([#114](https://github.com/tpvasconcelos/ridgeplot/pull/114))

### Features

- Add functionality to allow plotting of multiple traces per row.
  ([#114](https://github.com/tpvasconcelos/ridgeplot/pull/114))
- Add `ridgeplot.datasets.load_lincoln_weather()` helper function to load the "Lincoln Weather"
  toy dataset. ([#114](https://github.com/tpvasconcelos/ridgeplot/pull/114))
- Add more versions of the _probly_ dataset (`"wadefagen"` and `"illinois"`).
  ([#114](https://github.com/tpvasconcelos/ridgeplot/pull/114))
- Add support for Python 3.11.

### Documentation

- Major update to the documentation, including more examples, interactive plots, script to
  generate the HTML and WebP images from the example scripts, improved API reference, and more.
  ([#114](https://github.com/tpvasconcelos/ridgeplot/pull/114))

### Internal

- Remove `mdformat` from the automated CI checks. It can still be triggered manually.
  ([#114](https://github.com/tpvasconcelos/ridgeplot/pull/114))
- Improved type annotations and type checking.
  ([#114](https://github.com/tpvasconcelos/ridgeplot/pull/114))

---

0.1.21
------

### Features

- Add `ridgeplot.datasets.load_probly()` helper function to load the `probly` toy dataset. The
  `probly.csv` file is now included in the package under `ridgeplot/datasets/data/`.
  ([#80](https://github.com/tpvasconcelos/ridgeplot/pull/80))

### Documentation

- Change to numpydoc style docstrings.
  ([#81](https://github.com/tpvasconcelos/ridgeplot/pull/81))
- Add a robots.txt to the docs site.
  ([#81](https://github.com/tpvasconcelos/ridgeplot/pull/81))
- Auto-generate a site map for the docs site using `sphinx_sitemap`.
  ([#81](https://github.com/tpvasconcelos/ridgeplot/pull/81))
- Change the sphinx theme to `furo`.
  ([#81](https://github.com/tpvasconcelos/ridgeplot/pull/81))
- Improve the internal documentation and some of these internals to the API reference.
  ([#81](https://github.com/tpvasconcelos/ridgeplot/pull/81))

### Internal

- Fixed and improved some type annotations, including the introduction of `ridgeplot._types`
  module for type aliases such as `Numeric` and `NestedNumericSequence`.
  ([#80](https://github.com/tpvasconcelos/ridgeplot/pull/80))
- Add the `blacken-docs` pre-commit hook and add the `pep8-naming`, `flake8-pytest-style`,
  `flake8-simplify`, `flake8-implicit-str-concat`, `flake8-bugbear`, `flake8-rst-docstrings`,
  `flake8-rst-docstrings`, etc... plugins to the `flake8` pre-commit hook.
  ([#81](https://github.com/tpvasconcelos/ridgeplot/pull/81))
- Cleanup and improve some type annotations.
  ([#81](https://github.com/tpvasconcelos/ridgeplot/pull/81))
- Update deprecated `set-output` commands (GitHub Actions)
  ([#87](https://github.com/tpvasconcelos/ridgeplot/pull/87))

---

0.1.17
------

- Automate the release process. See .github/workflows/release.yaml, which issues a new GitHub
  release whenever a new git tag is pushed to the main branch by extracting the release notes from
  the changelog.
- Fix automated release process to PyPI.
  ([#27](https://github.com/tpvasconcelos/ridgeplot/pull/27))

---

0.1.16
------

- Upgrade project structure, improve testing and CI checks, and start basic Sphinx docs.
  ([#21](https://github.com/tpvasconcelos/ridgeplot/pull/21))
- Implement `LazyMapping` helper to allow `ridgeplot._colors.PLOTLY_COLORSCALES` to lazy-load from
  `colors.json` ([#20](https://github.com/tpvasconcelos/ridgeplot/pull/20))

---

0.1.14
------

- Remove `named_colorscales` from public API
  ([#18](https://github.com/tpvasconcelos/ridgeplot/pull/18))

---

0.1.13
------

- Add tests for example scripts ([#14](https://github.com/tpvasconcelos/ridgeplot/pull/14))

---

0.1.12
------

### Internal

- Update and standardise CI steps ([#6](https://github.com/tpvasconcelos/ridgeplot/pull/6))

### Documentation

- Publish official contribution guidelines (`CONTRIBUTING.md`)
  ([#8](https://github.com/tpvasconcelos/ridgeplot/pull/8))
- Publish an official Code of Conduct (`CODE_OF_CONDUCT.md`)
  ([#7](https://github.com/tpvasconcelos/ridgeplot/pull/7))
- Publish an official release/change log (`CHANGES.md`)
  ([#6](https://github.com/tpvasconcelos/ridgeplot/pull/6))

---

0.1.11
------

- `colors.json` was missing from the final distributions
  ([#2](https://github.com/tpvasconcelos/ridgeplot/pull/2))

---

0.1.0
------

- 🚀 Initial release!
