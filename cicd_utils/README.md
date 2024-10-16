# CI utilities

This directory contains python source code and helper scripts used by CI/CD tasks.

**Note to maintainers:** It is not mandatory, but it is highly recommended to also test the code in this directory (meta, I know!). See `tests/cicd_utils/` for some examples.

## The `cicd` package

The `cicd/` directory is a Python package containing modules used/imported by some CI tasks such as our test suite (`tests/`) or documentation building entrypoint (`docs/conf.py`).

For this reason, the `cicd_utils` directory needs to be made explicitly discoverable to these tools by appending it to the Python PATH:

- For pytest, we configure this using the [pythonpath](https://docs.pytest.org/en/7.4.x/reference/reference.html#confval-pythonpath) option in `pytest.ini`.
- For Sphinx, we set `PYTHONPATH={env:PYTHONPATH}{:}{toxinidir}/cicd_utils` in the relevant environment in `tox.ini`.

Static analysis tools will also we need to be made aware of this package:

- For mypy, we can add it to the `files` option in `mypy.ini` to help with import discovery.
- For ruff's _isort_-implementation, we also added it to the `known-first-party` list (see `ruff.toml`)

### The `cicd/scripts` directory

The `cicd/scripts` directory contains various scripts used by some CI/CD tasks. These scripts should all be marked as executable and contain a shebang line at the top.


## The `ridgeplot_exampes` directory

The `ridgeplot_examples` directory is also a Python package but it is used to store example/helper functions that generate figures for the documentation. These scripts are run as part of the CI/CD pipeline to ensure that the examples are up-to-date and that the figures are generated correctly. These functions are also run by the `tests/e2e` test suite to ensure that the examples are working as expected and no regressions are introduced.
