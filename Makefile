# ==============================================================
# >>>  Variables
# ==============================================================

BASE_PYTHON ?= python3.7

VENV_PATH := .venv
VENV_BIN  := $(VENV_PATH)/bin

PY_PYTHON_VERSION = $(shell $(VENV_BIN)/python -c 'import platform; print("".join(platform.python_version_tuple()[:2]))')
PY_SYS_PLATFORM   = $(shell $(VENV_BIN)/python -c 'import sys; print(sys.platform)')


# ==============================================================
# >>>  Help (default goal)
# ==============================================================

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_\.-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


# ==============================================================
# >>>  Setup development environment
# ==============================================================

.PHONY: init
init: clean-all install ## initialise development environment
	@echo "==> Initialised development environment!"


.venv: ## create a virtual environment
	@echo "==> Creating local virtual environment under: $(VENV_PATH)/ ($(BASE_PYTHON))"
	@$(BASE_PYTHON) -m pip install --upgrade pip
	@$(BASE_PYTHON) -m venv "$(VENV_PATH)"
	@echo "==> Installing and/or upgrading build dependencies..."
	@$(VENV_BIN)/python -m pip install --upgrade pip setuptools wheel


.PHONY: install
install: .venv ## install all local development dependencies
	@echo "==> Installing local development requirements..."
	@$(VENV_BIN)/python -m pip install -r requirements/locked/local-dev.$(PY_PYTHON_VERSION)-$(PY_SYS_PLATFORM).txt
	@echo "==> Installing pre-commit hooks..."
	@$(VENV_BIN)/pre-commit install --install-hooks


.PHONY: init-jupyter
jupyter-init: ## initialise a jupyterlab environment and install extensions
	@echo "==> Setting up jupyterlab environment..."
	@$(VENV_BIN)/python -m pip install --upgrade ipykernel jupyterlab
	@$(VENV_BIN)/python -m ipykernel install --user --name="ridgeplot"
	@$(VENV_BIN)/python -m jupyter lab build


# ==============================================================
# >>>  Cleaning
# ==============================================================

.PHONY: clean-all
clean-all: clean-ci clean-venv clean-build clean-pyc ## remove all artifacts
	@echo "==> Removed all artifacts!"


.PHONY: clean-build
clean-build: ## remove build artifacts
	@echo "==> Removing build artifacts..."
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +


.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	@echo "==> Removing python file artifacts..."
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +


.PHONY: clean-ci
clean-ci: ## remove linting, testing, and coverage artifacts
	@echo "==> Removing lint, test, and coverage artifacts..."
	@rm -fr .tox/
	@rm -fr .pytest_cache
	@rm -fr .mypy_cache/
	@find . -name 'coverage.xml' -exec rm -f {} +
	@find . -name '.coverage' -exec rm -f {} +


.PHONY: clean-venv
clean-venv: ## remove venv artifacts
	@echo "==> Removing virtual environment..."
	@rm -fr .venv
