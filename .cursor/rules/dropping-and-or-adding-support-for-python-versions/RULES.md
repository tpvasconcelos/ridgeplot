---
description: Dropping and/or adding support for Python versions
alwaysApply: false
---
This project tries to follow the [official](https://devguide.python.org/versions/) Python support policy.

When a new Python version is released, support for it should be added in the CI pipeline as soon as possible. This means updating `.github/workflows/ci.yml`'s `jobs.software-tests.strategy.matrix.python-version` and `pyproject.toml`'s `project.classifiers` to include the new version.

When a Python version reaches its end-of-life, support for it should be dropped. This means removing it from the CI pipeline and updating the following entries:

- `.github/workflows/ci.yml`:
  - `jobs.software-tests.strategy.matrix.python-version`
  - `jobs.static-checks.steps.with.python-version`
- `.github/workflows/release.yml`:
  - `jobs.build.steps.with.python-version`
  - `jobs.github-release.steps.with.python-version`
- `.pre-commit-config.yaml`: `default_language_version.python`
- `.readthedocs.yml`: `build.tools.python`
- `AGENTS.md`: Wherever relevant
- `docs/development/contributing.md`: Wherever relevant
- `makefile`: `BASE_PYTHON`
- `mypy.ini`: `python_version`
- `pyproject.toml`
  - `project.classifiers`
  - `project.requires-python`
- `pyrightconfig.json`: `pythonVersion`
- `ruff.toml`: `target-version`

In both instances, you should also update `docs/reference/changelog.md` to reflect the change in supported Python versions for the next release.

- When adding support for a new Python version, you can add an _"Add support for Python 3.XX, in accordance with the official Python support policy[^1] ({gh-pr}`XXX`)"_ entry at the top of the _"Unreleased changes"_ section.
- When dropping support for a Python version, you can add a _"Dropped support for Python 3.XX, in accordance with the official Python support policy[^1] ({gh-pr}`XXX`)"_ entry in a _"Breaking changes"_ section under the _"Unreleased changes"_ section.
