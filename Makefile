# ==============================================================
# ---  Help (default goal)
# ==============================================================

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


# ==============================================================
# ---  Variables
# ==============================================================

# Adjustable through export
BASE_PYTHON	?= python3.7

# Virtual environment
VENV_PATH	= .venv
VENV_BIN	= $(VENV_PATH)/bin
PYTHON		= $(VENV_BIN)/python


# ==============================================================
# ---  Setup development environment
# ==============================================================

.PHONY: init
init: clean-all venv-init install ## initialise development environment


.PHONY: venv-init
venv-init: clean-venv ## create a virtual environment
	$(BASE_PYTHON) -m pip install --upgrade pip
	$(BASE_PYTHON) -m venv "$(VENV_PATH)"


.PHONY: install
install: ## install the package in editable mode and install all pre-commit hooks
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	$(PYTHON) -m pip install -e ".[dev]"
	$(PYTHON) -m pre_commit install --install-hooks --overwrite


.PHONY: jupyter-init
jupyter-init: ## initialise a jupyterlab environment and install extensions
	$(PYTHON) -m pip install -e ".[notebook]"
	$(PYTHON) -m ipykernel install --user --name="ridgeplot"
	$(PYTHON) -m jupyter lab build


.PHONY: jupyter-plotly
jupyter-plotly: ## setup jupyterlab's plotly extensions
	$(PYTHON) -m jupyter labextension install @jupyter-widgets/jupyterlab-manager \
                                              jupyterlab-plotly \
                                              plotlywidget
	$(PYTHON) -m jupyter lab build


# ==============================================================
# ---  Building and releasing
# ==============================================================

.PHONY: docs
docs: ## generate Sphinx HTML documentation, including API docs
	#rm -f docs/ridgeplot.rst
	#rm -f docs/modules.rst
	#sphinx-apidoc -o docs/ ridgeplot
	$(MAKE) --directory=docs clean
	$(MAKE) --directory=docs html
	$(PYTHON) "scripts/open_in_browser.py" "docs/build/html/index.html"


.PHONY: servedocs
servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) --directory=docs html' -R -D .


.PHONY: dist
dist: clean-build ## builds source and wheel package
	$(PYTHON) setup.py sdist bdist_wheel
	$(PYTHON) -m twine check --strict dist/*


.PHONY: release-test
release-test: dist ## package and upload a release to test pypi
	$(PYTHON) -m twine upload --repository testpypi dist/*


.PHONY: release-prod
release-prod: dist ## package and upload a release prod pypi
	$(PYTHON) -m twine upload dist/*


# ==============================================================
# ---  Cleaning
# ==============================================================

.PHONY: clean-all
clean-all: clean-ci clean-venv clean-build clean-pyc ## remove all artifacts


.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +


.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


.PHONY: clean-ci
clean-ci: ## remove linting, testing, and coverage artifacts
	rm -fr .tox/
	rm -fr .pytest_cache
	rm -fr .mypy_cache/
	find . -name 'coverage.xml' -exec rm -f {} +
	find . -name '.coverage' -exec rm -f {} +


.PHONY: clean-venv
clean-venv: ## remove venv artifacts
	rm -fr .venv
