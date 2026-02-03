# ridgeplot Development Guide for AI Agents

`ridgeplot` is a Python package that provides a simple interface for plotting beautiful and interactive ridgeline plots within the extensive Plotly ecosystem.

This file provides guidance for AI assistants working with the ridgeplot codebase.

## Public API Overview

The library only exposes three public functions to end users.

Two of these functions are toy dataset loaders (`ridgeplot.datasets.load_probly()` and
`ridgeplot.datasets.load_lincoln_weather()`) but they are not the focus on the project and are only exposed for backwards compatibility reasons.

The third function (`ridgeplot.ridgeplot()`) is a Plotly Figure (
`plotly.graph_objects.Figure`) factory function, and it's the focus of this project. See its docstring at
`src/ridgeplot/_ridgeplot.py` for full details.

## .cursor rules directory

You can check
`.cursor/rules` before providing recommendations or generating code. This directory contains the authoritative rules for all development aspects.

To find the relevant rules:

1. Find ALL .md files in `.cursor/rules`
2. Read ALL relevant rules files, based on the filetypes/languages/libraries/tasks/folders involved (e.g., .tsx, .css, .java, React,
   `//web/src/pages/home`, etc)
3. If unsure, read metadata (first 5 lines) of any .mdc file to check rule scope/description/keywords

**For common tasks, you can check these specific files:**

- Bazel/testing: `.cursor/rules/bazel-test-execution.mdc`
- Java code: `.cursor/rules/java-conventions.mdc`
- TypeScript/web: `.cursor/rules/web-conventions.mdc`
- Pull requests: `.cursor/rules/pull-request-conventions.mdc`

**Documentation:** https://ridgeplot.readthedocs.io/en/stable/

**Python Version**: Requires Python 3.10+

## Common Commands

### Environment Setup

```bash
# Initialize full development environment (recommended for first-time setup)
# This creates .venv, installs dependencies, and sets up pre-commit hooks
make init

# Use a different Python version if needed (default is python3.10)
BASE_PYTHON=python3.14 make init

# Offline mode (uses cached packages only) -  useful when the internet is down
OFFLINE=1 make init

# Activate the virtual environment
source .venv/bin/activate
```

### Running Tests

```bash
# Run all test suits (unit + e2e + cicd_utils)
tox -m tests

# Run a specific test suite
tox -e tests-unit        # Unit tests with coverage
tox -e tests-e2e         # End-to-end tests
tox -e tests-cicd_utils  # CI/CD utilities tests

# Run pytest directly with custom options
tox -e pytest -- tests/unit/test_init.py --no-cov
tox -e pytest -- -k "test_specific_function" --no-cov
```

### Linting and Formatting

```bash
# Run the main static checks
tox -m static-quick

# Run the entire suite of static checks (incl. all pre-commit hooks)
# If running from the main branch, you'll need
# to skip the 'no-commit-to-branch' check with:
SKIP='no-commit-to-branch' tox -m static

# Run specific pre-commit hooks
pre-commit run ruff --all-files
pre-commit run ruff-format --all-files

# Run type checking with pyright only
tox -e typing
```

### Documentation

```bash
# Build static documentation
tox -e docs-static
```

## Architecture Overview

```
src/ridgeplot/
├── __init__.py           # Public API exports
├── _ridgeplot.py         # Main ridgeplot() function
├── _figure_factory.py    # Plotly Figure construction
├── _kde.py               # Kernel Density Estimation
├── _hist.py              # Histogram binning
├── _types.py             # Type aliases and type guards
├── _utils.py             # Utility functions
├── _missing.py           # Sentinel for missing values
├── _version.py           # Version string (setuptools-scm)
├── _color/               # Color handling
│   ├── colorscale.py     # Colorscale resolution
│   ├── css_colors.py     # CSS color parsing
│   ├── interpolation.py  # Color interpolation
│   └── utils.py          # Color utilities
├── _obj/traces/          # Trace objects
│   ├── area.py           # Area trace (filled curves)
│   ├── bar.py            # Bar trace (histograms)
│   └── base.py           # Base trace class
├── _vendor/              # Vendored dependencies
└── datasets/             # Built-in datasets
    └── data/             # CSV data files

tests/
├── conftest.py           # Shared pytest fixtures
├── unit/                 # Unit tests for individual modules
├── e2e/                  # End-to-end tests with expected outputs
│   └── artifacts/        # JSON artifacts for e2e comparisons
└── cicd_utils/           # Tests for CI/CD utilities

cicd_utils/               # CI/CD helper modules
├── cicd/                 # Scripts and test helpers
└── ridgeplot_examples/   # Example implementations for docs/testing
```

### Key Data Flow

1. User calls `ridgeplot(samples=...)` or `ridgeplot(densities=...)`
2. If samples provided → KDE (`_kde.py`) or histogram binning (`_hist.py`) produces densities
3. Densities are normalised if `norm` parameter is set
4. `create_ridgeplot()` in `_figure_factory.py` builds the Plotly Figure:
    - Resolves colorscale and computes colors for each trace
    - Creates trace objects (area or bar) for each density
    - Applies layout settings (spacing, padding, axes)
5. Returns a `plotly.graph_objects.Figure` that users can further customise

### Type System

The codebase uses extensive type annotations. Key types in `_types.py`:

- **Samples/Densities**: Ragged 3D arrays `[rows][traces_per_row][values]`
- **ShallowSamples/ShallowDensities**: 2D arrays (one trace per row)
- **ColorScale**: `Collection[tuple[float, Color]]`
- **Type guards**: `is_shallow_samples()`, `is_densities()`, etc.

## Code Style Guidelines

### General

- **Python version**: 3.10+ (uses modern typing features)
- **Line length**: 100 characters
- **Formatting**: Ruff (replaces black, isort, flake8)
- **Imports**: Always include `from __future__ import annotations`
- **Docstrings**: NumPy style
- **Type annotations**: Use full and modern type annotations throughout with strict pyright checking

### Type Annotations

- All functions must be fully typed
- Use `TYPE_CHECKING` blocks for import-only types
- Uses **pyright** in strict mode (see `pyrightconfig.json`)
- Use type guards for runtime type narrowing (see `_types.py`)
- Follow this general principle for user-facing code: be contravariant in the input type and covariant in the output type

## Working with This Codebase

### When Adding New Features

1. Start with `_ridgeplot.py` to understand the main entry point
2. Add new parameters following the existing patterns (with proper deprecation handling)
3. Update type annotations in `_types.py` if introducing new data structures
4. Add tests in `tests/unit/` with good coverage
5. Update documentation in docstrings following the existing conventions

### When Fixing Bugs

1. Write a failing test first
2. Fix the issue with minimal changes
3. Ensure all existing tests pass
4. Check type annotations are correct

### Common Patterns

**Handling deprecated parameters:**

```python
if deprecated_param is not MISSING:
    if new_param is not None:
        raise ValueError("Cannot use both...")
    warnings.warn("...", DeprecationWarning, stacklevel=2)
    new_param = deprecated_param
```

**Type narrowing with guards:**

```python
if is_shallow_samples(samples):
    samples = nest_shallow_collection(samples)
samples = cast("Samples", samples)
```

**Lazy imports for performance:**

```python
# Heavy imports inside functions to reduce import time
def _coerce_to_densities(...):
    from ridgeplot._kde import estimate_densities  # statsmodels is slow to import
```

### Testing Tips

- Use `--no-cov` flag during development for faster test runs
- Run specific tests: `tox -e pytest -- tests/unit/test_ridgeplot.py -k "test_name" --no-cov`
- The `tests/e2e/artifacts/` directory contains expected Plotly Figure JSON for e2e tests
- `conftest.py` patches `fig.show()` to prevent browser windows during tests

### Key Files to Know

| File                               | Purpose                     |
|------------------------------------|-----------------------------|
| `src/ridgeplot/_ridgeplot.py`      | Main `ridgeplot()` function |
| `src/ridgeplot/_figure_factory.py` | Figure construction logic   |
| `src/ridgeplot/_types.py`          | All type aliases and guards |
| `tests/unit/test_ridgeplot.py`     | Core function tests         |
| `cicd_utils/ridgeplot_examples/`   | Example scripts for docs    |
| `tox.ini`                          | CI environment definitions  |
| `ruff.toml`                        | Linting configuration       |

## CI/CD Pipeline

Tests run on GitHub Actions across:

- Python versions: 3.10, 3.11, 3.12, 3.13, 3.14
- Operating systems: Ubuntu, macOS, Windows

Coverage is uploaded to Codecov with:

- Overall: 98% minimum
- Diff coverage: 100% for new code

## Notes for AI Assistants

1. **Always run tests** after making changes: `tox -e pytest -- <path> --no-cov`
2. **Check types** with: `tox -e typing`
3. **Format code** with: `pre-commit run ruff-format --all-files`
4. **Respect existing patterns** - this is a mature codebase with consistent style
5. **Don't add unnecessary abstractions** - keep changes minimal and focused
6. **Preserve deprecation warnings** - the library maintains backward compatibility
7. **Update docstrings** when changing function signatures
8. **Use type guards** for runtime type narrowing instead of assertions
