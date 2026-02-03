---
name: dropping-and-adding-support-for-python-versions
description: "Keeps supported Python versions aligned across CI, configs, and docs. Use when adding a new Python version or dropping an end-of-life version per the official Python support policy."
---

# Dropping and adding support for Python versions

## When to use

- The user asks to add support for a specific Python version.
- The user asks to drop or deprecate an end-of-life Python version.
- The user asks to sync supported versions with the official [Python support policy](https://devguide.python.org/versions/).

## Required inputs

- Change type: add or drop a specific version, or asked to sync with the official support policy.
- Exact Python version string (e.g., 3.13), if applicable.

If any input is missing, ask before editing.

## Workflow

1. Confirm that you have the required inputs.
2. Apply the file updates for the change type.
3. Add an entry to the [changelog](docs/reference/changelog.md) as specified below.
4. Search for other mentions of the target version and update only those that describe supported versions.
5. Run the entire test suite to ensure no regressions.
6. Run all linters and type checks to ensure consistency.
7. Report the changes made, tests run, and any follow-ups needed.

## Adding support for a new Python version

- .github/workflows/ci.yml: `jobs.software-tests.strategy.matrix.python-version`
- pyproject.toml: `project.classifiers`

Finally, update the changelog at the top of "Unreleased changes" using the following template:

> Add support for Python 3.XX, in accordance with the official Python support policy[^1] ({gh-pr}`XXX`).

## Dropping support for an end-of-life Python version

- .github/workflows/ci.yml: `jobs.software-tests.strategy.matrix.python-version` and `jobs.static-checks.steps.with.python-version`
- .github/workflows/release.yml: `jobs.build.steps.with.python-version` and `jobs.github-release.steps.with.python-version`
- .pre-commit-config.yaml: `default_language_version.python`
- .readthedocs.yml: `build.tools.python`
- AGENTS.md: wherever relevant
- docs/development/contributing.md: wherever relevant
- Makefile: `BASE_PYTHON`
- mypy.ini: `python_version`
- pyproject.toml: `project.classifiers`, `project.requires-python`
- pyrightconfig.json: `pythonVersion`
- ruff.toml: `target-version`

Finally, update the changelog under "Unreleased changes" -> "Breaking changes" using the following template:

> Dropped support for Python 3.XX, in accordance with the official Python support policy[^1] ({gh-pr}`XXX`).

## Validation checks

- CI matrix, classifiers, and `requires-python` are consistent.
- Tooling configs reflect the new minimum version when dropping support.
- Docs mention the updated supported versions where appropriate.

## Out of scope

- Do not change dependency versions or code behavior unless the user asks.
- Do not update unrelated CI jobs or tooling settings.

## Output

- Summarize changes and list updated files.
- Note any tests run and follow-ups needed.
- If you encountered any discrepancies between these instructions and the locations in the codebase where supported Python versions are mentioned and need to be updated, please document them here for future reference.
