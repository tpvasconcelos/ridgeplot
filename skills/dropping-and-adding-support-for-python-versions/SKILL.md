---
name: dropping-and-adding-support-for-python-versions
description: "Use when adding or dropping Python version support by updating the supported Python versions across CI, configs, and docs in line with the official Python support policy."
---

# Dropping and adding support for Python versions

## Overview

This project adheres to the official Python support policy: https://devguide.python.org/versions/

Use this skill to keep Python version support in sync with the official Python support policy by updating the project files consistently.

## Workflow

1. Identify the change type: add support for a new Python version or drop support for an end-of-life Python version.
2. Confirm the exact Python version string (e.g., add support for 3.45) and the PR number to insert in the changelog entry (e.g., PR #1234)
3. Apply the relevant changelog entry and file updates listed below.

## Adding support for a new Python version

1. Update `docs/reference/changelog.md` at the top of "Unreleased changes" with:
    > Add support for Python 3.XX, in accordance with the official Python support policy[^1] ({gh-pr}`XXX`)".
2. Update the following locations:
   - .github/workflows/ci.yml: `jobs.software-tests.strategy.matrix.python-version`
   - pyproject.toml: `project.classifiers`

## Dropping support for an end-of-life Python version

1. Update `docs/reference/changelog.md` under "Unreleased changes" -> "Breaking changes" with:
    > Dropped support for Python 3.XX, in accordance with the official Python support policy[^1] ({gh-pr}`XXX`).
2. Update the following locations:
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
