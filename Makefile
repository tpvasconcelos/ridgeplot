# ==============================================================
# >>>  Variables
# ==============================================================

BASE_PYTHON ?= python3.10

VENV_PATH := .venv
VENV_BIN  := $(VENV_PATH)/bin

OFFLINE ?= 0
ifeq ($(OFFLINE), 1)
    _UV_OFFLINE_ARG = --offline

else
    _UV_OFFLINE_ARG =
endif

# ==============================================================
# >>>  Help (default goal)
# ==============================================================

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

print("Available targets:")
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


.PHONY: _check-sys
_check-sys: ## Check system requirements
	@if ! command -v uv > /dev/null; then \
		echo "[ERROR] uv doesn't seem to be installed on your system!"; \
		echo "Please install uv by following the instructions at: https://docs.astral.sh/uv/"; \
	else \
		echo "==> System check passed!"; \
	fi


$(VENV_PATH): _check-sys ## create a virtual environment
	@echo "==> Creating local virtual environment under: $(VENV_PATH)/ ($(BASE_PYTHON))"
	@uv venv $(_UV_OFFLINE_ARG) --python="$(BASE_PYTHON)" --seed "$(VENV_PATH)"


.PHONY: install
install: $(VENV_PATH) ## install all local development dependencies
	@echo "==> Installing local development requirements..."
	@uv pip install $(_UV_OFFLINE_ARG) --upgrade -r requirements/local-dev.txt
	@if [ $(OFFLINE) -eq 0 ]; then \
		echo "==> Installing pre-commit hooks..."; \
		$(VENV_BIN)/pre-commit install --install-hooks; \
	else \
		echo "[WARN] Skipping pre-commit hooks installation (offline mode)"; \
	fi


.PHONY: jupyter-init
jupyter-init: install ## initialise a jupyter environment
	@echo "==> Setting up jupyterlab environment..."
	@$(VENV_BIN)/uv pip install --upgrade ipykernel jupyter
	@$(VENV_BIN)/python -m ipykernel install --user --name='ridgeplot' --display-name='ridgeplot'


# ==============================================================
# >>>  Cleaning
# ==============================================================

.PHONY: clean-all
clean-all: clean-docs clean-build clean-pyc clean-cov clean-ci-caches clean-tox clean-venv ## remove all artifacts
	@echo "==> Removed all artifacts!"


.PHONY: clean-docs
clean-docs: ## remove documentation build artifacts
	@echo "==> Removing documentation build artifacts..."
	@rm -fr docs/_build/ docs/api/autogen/ docs/api/public/
	@find . -wholename 'docs/_static/charts/*.html' -exec rm -fr {} +


.PHONY: clean-build
clean-build: ## remove build artifacts
	@echo "==> Removing build artifacts..."
	@rm -fr build/ dist/ .eggs/
	@find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +


.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	@echo "==> Removing python file artifacts..."
	@find . -name '*.pyc' -o -name '*.pyo' -o -name '*~' -o -name '__pycache__' -exec rm -fr {} +


.PHONY: clean-cov
clean-cov: ## remove coverage artifacts
	@echo "==> Removing coverage artifacts..."
	@find . \( -name 'coverage.*.xml' -o -name 'coverage.xml' -o -name '.coverage.*' \) -exec rm -fr {} +
	@rm -fr coverage/


.PHONY: clean-ci-caches
clean-ci-caches: ## remove CI caches (e.g. `.pytest_cache`, `.mypy_cache`, etc...)
	@echo "==> Removing CI caches..."
	@rm -fr .pytest_cache/ .mypy_cache/ .ruff_cache/


.PHONY: clean-tox
clean-tox: ## remove Tox artifacts
	@echo "==> Removing Tox artifacts..."
	@rm -fr .tox/


.PHONY: clean-venv
clean-venv: ## remove venv artifacts
	@echo "==> Removing virtual environment..."
	@rm -fr $(VENV_PATH)
