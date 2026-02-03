# ridgeplot Development Guide for AI Agents

`ridgeplot` is a Python package for beautiful, interactive ridgeline plots built on Plotly.

## Start Here

- Read this file first, then the most relevant source file(s).
- Prefer local docs and tests over memory; do not guess behavior.
- If requirements are unclear or risky, ask a concrete question before changing code.

## Stack and Style Constraints

- Python >=3.10
- Plotly graph objects (dependency is `plotly>=5.20`)
- Line length 100, formatting with ruff
- Docstrings are NumPy style
- Type annotations are modern and throughout with strict checking via pyright

## Quick Commands

### Environment Setup

```bash
# Initialize full development environment (recommended for first-time setup)
# This creates .venv, installs dependencies, and sets up pre-commit hooks
make init

# Use a different Python version if needed (default is python3.10)
BASE_PYTHON=python3.14 make init

# Offline mode (uses cached packages only)
OFFLINE=1 make init

# Activate the virtual environment
source .venv/bin/activate
```

### Running Tests

```bash
# Run all test suites (unit + e2e + cicd_utils)
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

## Project Map

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

## Public API

The public API exposes one main function: `ridgeplot.ridgeplot(...) -> go.Figure`

The `ridgeplot()` docstring in `src/ridgeplot/_ridgeplot.py` contains the API contract.

`ridgeplot.datasets.load_probly()` and
  `ridgeplot.datasets.load_lincoln_weather()` are legacy loaders kept for
  backwards compatibility only.

## Key Data Flow

1. Users call `ridgeplot(samples=...)` or `ridgeplot(densities=...)`.
2. If samples are provided, KDE in `_kde.py` or histogram binning in `_hist.py`
   produces densities.
3. Densities are normalised if the `norm` parameter is set.
4. `create_ridgeplot()` in `_figure_factory.py` builds the Plotly Figure by
   resolving colors, creating traces, and applying layout settings.
5. The function returns a `plotly.graph_objects.Figure`.

## Key Files to Know

| File                               | Purpose                     |
|------------------------------------|-----------------------------|
| `src/ridgeplot/_ridgeplot.py`      | Main `ridgeplot()` function |
| `src/ridgeplot/_figure_factory.py` | Figure construction logic   |
| `src/ridgeplot/_types.py`          | All type aliases and guards |
| `tests/unit/test_ridgeplot.py`     | Core function tests         |
| `cicd_utils/ridgeplot_examples/`   | Example scripts for docs    |
| `docs/`                            | User and developer docs     |
| `tox.ini`                          | CI environment definitions  |
| `ruff.toml`                        | Linting configuration       |

Documentation: https://ridgeplot.readthedocs.io/en/stable/

## Workflow Expectations

### When Adding New Features

1. Start with `src/ridgeplot/_ridgeplot.py` to understand the entry point.
2. Add parameters following existing patterns and deprecation handling.
3. Update types in `src/ridgeplot/_types.py` when introducing new structures.
4. Add tests in `tests/unit/` with good coverage.
5. Update docstrings to match the new behavior.

### When Fixing Bugs

1. Write a failing test first.
2. Fix the issue with minimal changes.
3. Ensure tests and type checks pass.
4. Verify docstrings remain accurate.

### Type Annotations

- Uses **pyright** in strict mode (see `pyrightconfig.json`)
- All functions must be fully typed, following modern Python typing practices and existing project conventions.
- Use `TYPE_CHECKING` blocks for import-only types
- Use type guards for runtime type narrowing (see `_types.py`)
- Follow this general principle for user-facing code: be contravariant in the input type and covariant in the output type
- Add type aliases close to their usage. If widely used, place in `_types.py`.

## Common Patterns

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

## Testing Notes

- Use `--no-cov` flag during development for faster test runs
- Run targeted tests via: `tox -e pytest -- tests/unit/test_foo.py -k "test_bar" --no-cov`
- The `tests/e2e/artifacts/` directory contains expected Plotly Figure JSON for e2e tests

## Agent Skills

Agent skills live under `skills/`. For Python version support changes, follow
`skills/dropping-and-or-adding-support-for-python-versions/SKILL.md`.

## CI/CD Pipeline

GitHub Actions runs tests on Python 3.10–3.14 across Ubuntu, macOS, and Windows.
Codecov minimums are 98% overall and 100% diff coverage for new code.

## Notes for AI Assistants

1. Run tests after changes when feasible, starting with the smallest relevant
   subset.
2. Run `tox -e typing` if types are touched or errors are likely.
3. Run `pre-commit run ruff-format --all-files` to format code.
4. Preserve deprecation behavior and public API stability.
5. Keep changes minimal and aligned with existing patterns.
6. Respect existing patterns - this is a mature codebase with consistent style.
