# Release notes

This document outlines the list of changes to ridgeplot between each release. For full details, see
the [commit logs](https://github.com/tpvasconcelos/ridgeplot/commits/).

Unreleased changes
------------------

- 🔧 Automate the release process. See .github/workflows/release.yaml, which issues a new GitHub
  release whenever a new git tag is pushed to the master branch by extracting the release notes from
  the changelog.
- 🔧 Fix automated release process to
  PyPi. ([#27](https://github.com/tpvasconcelos/ridgeplot/pull/27))

0.1.16
------

- 🔧 Upgrade project structure, improve testing and CI checks, and start basic Sphinx
  docs. ([#21](https://github.com/tpvasconcelos/ridgeplot/pull/21))
- 🔧 Implement `LazyMapping` helper to allow `ridgeplot._colors.PLOTLY_COLORSCALES` to lazy-load from
  `colors.json` ([#20](https://github.com/tpvasconcelos/ridgeplot/pull/20))

0.1.14
------

- 📦 Remove `named_colorscales` from public
  API ([#18](https://github.com/tpvasconcelos/ridgeplot/pull/18))

0.1.13
------

- 🧪 Add tests for example scripts ([#14](https://github.com/tpvasconcelos/ridgeplot/pull/14))

0.1.12
------

### Internal

- 📦 Update and standardise CI steps ([#6](https://github.com/tpvasconcelos/ridgeplot/pull/6))

### Documentation

- 📚 Publish official contribution
  guidelines (`CONTRIBUTING.md`) ([#8](https://github.com/tpvasconcelos/ridgeplot/pull/8))
- 📚 Publish an official Code of
  Conduct (`CODE_OF_CONDUCT.md`) ([#7](https://github.com/tpvasconcelos/ridgeplot/pull/7))
- 📚 Publish an official release/change
  log (`CHANGES.md`) ([#6](https://github.com/tpvasconcelos/ridgeplot/pull/6))

0.1.11
------

- 🐛 `colors.json` was missing from the final distributions
  ([#2](https://github.com/tpvasconcelos/ridgeplot/pull/2))

0.1.0
------

- 🚀 Initial release!
