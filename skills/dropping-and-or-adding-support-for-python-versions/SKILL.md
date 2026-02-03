---
name: dropping-and-or-adding-support-for-python-versions
description: Update supported Python versions across CI, configs, and docs in line with the official Python support policy. Use when adding or dropping Python version support.
---
This project follows the official Python support policy: https://devguide.python.org/versions/

When adding support for a new Python version
1. Update `.github/workflows/ci.yml` at `jobs.software-tests.strategy.matrix.python-version`.
2. Update `pyproject.toml` at `project.classifiers`.
3. Update `docs/reference/changelog.md` at the top of "Unreleased changes" with:
   "Add support for Python 3.XX, in accordance with the official Python support policy[^1] ({gh-pr}`XXX`)".

When dropping support for an end-of-life Python version
1. Remove it from the CI pipeline and update the entries listed below.
2. Update `docs/reference/changelog.md` under an "Unreleased changes" -> "Breaking changes" section with:
   "Dropped support for Python 3.XX, in accordance with the official Python support policy[^1] ({gh-pr}`XXX`)".

Files to update when dropping support for a Python version
- `.github/workflows/ci.yml`: `jobs.software-tests.strategy.matrix.python-version`,
  `jobs.static-checks.steps.with.python-version`.
- `.github/workflows/release.yml`: `jobs.build.steps.with.python-version`,
  `jobs.github-release.steps.with.python-version`.
- `.pre-commit-config.yaml`: `default_language_version.python`.
- `.readthedocs.yml`: `build.tools.python`.
- `AGENTS.md`: wherever relevant.
- `docs/development/contributing.md`: wherever relevant.
- `Makefile`: `BASE_PYTHON`.
- `mypy.ini`: `python_version`.
- `pyproject.toml`: `project.classifiers`, `project.requires-python`.
- `pyrightconfig.json`: `pythonVersion`.
- `ruff.toml`: `target-version`.
