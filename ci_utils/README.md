# CI utilities

This directory contains python source code needed by some CI tasks such as our test suites or documentation building. The modules are not packaged or installed anywhere by default. Instead, they should be appended to the Python PATH when needed. For instance:

- For pytest, we configure this using the [pythonpath](https://docs.pytest.org/en/7.4.x/reference/reference.html#confval-pythonpath) option in `pytest.ini`.
- For Sphinx, we set `PYTHONPATH={env:PYTHONPATH}{:}{toxinidir}/ci_utils` in the relevant environment in `tox.ini`.
- For mypy, we can add it to the `files` option in `mypy.ini` to help with import discovery.
- For ruff/isort, we also added it to the `known-first-party` list (`ruff.toml`)

It is not mandatory, but it is highly recommended to test the code in this directory. See `tests/ci_utils/` for examples.
