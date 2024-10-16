# ==============================================================
# >>>  Variables
# ==============================================================

BASE_PYTHON ?= python3.9

VENV_PATH := .venv
VENV_BIN  := $(VENV_PATH)/bin


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
	@if command -v uv; then \
		uv venv --python="$(BASE_PYTHON)" --seed "$(VENV_PATH)"; \
	else \
		$(BASE_PYTHON) -m pip install --upgrade pip; \
		$(BASE_PYTHON) -m venv "$(VENV_PATH)"; \
		echo "==> Installing seed packages..."; \
		$(VENV_BIN)/pip install --upgrade pip setuptools wheel; \
	fi
	@echo "==> Installing uv in the virtual environment..."
	@$(VENV_BIN)/pip install uv


.PHONY: install
install: .venv ## install all local development dependencies
	@echo "==> Installing local development requirements..."
	@$(VENV_BIN)/uv pip install --upgrade -r requirements/local-dev.txt
	@echo "==> Installing pre-commit hooks..."
	@$(VENV_BIN)/pre-commit install --install-hooks


.PHONY: jupyter-init
jupyter-init: install ## initialise a jupyter environment
	@echo "==> Setting up jupyterlab environment..."
	@$(VENV_BIN)/uv pip install --upgrade ipykernel jupyter
	@$(VENV_BIN)/ipykernel install --user --name="ridgeplot"


# ==============================================================
# >>>  Cleaning
# ==============================================================

.PHONY: clean-all
clean-all: clean-build clean-pyc clean-cov clean-ci-caches clean-tox clean-venv ## remove all artifacts
	@echo "==> Removed all artifacts!"


.PHONY: clean-build
clean-build: ## remove build artifacts
	@echo "==> Removing build artifacts..."
	rm -fr build/ dist/ .eggs/
	find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +


.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	@echo "==> Removing python file artifacts..."
	find . -name '*.pyc' -o -name '*.pyo' -o -name '*~' -o -name '__pycache__' -exec rm -fr {} +


.PHONY: clean-cov
clean-cov: ## remove coverage artifacts
	@echo "==> Removing coverage artifacts..."
	find . \( -name 'coverage.*.xml' -o -name '.coverage.*' \) -exec rm -fr {} +
	rm -fr coverage/


.PHONY: clean-ci-caches
clean-ci-caches: ## remove CI caches (e.g. `.pytest_cache`, `.mypy_cache`, etc...)
	@echo "==> Removing CI caches..."
	rm -fr .pytest_cache/ .mypy_cache/ .ruff_cache/


.PHONY: clean-tox
clean-tox: ## remove Tox artifacts
	@echo "==> Removing Tox artifacts..."
	rm -fr .tox/


.PHONY: clean-venv
clean-venv: ## remove venv artifacts
	@echo "==> Removing virtual environment..."
	rm -fr .venv
