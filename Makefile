.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"


.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


.PHONY: init
init: clean-all venv-init install jupyter-init ## initialise development environment


.PHONY: venv-init
venv-init: clean-venv ## create a virtual environment
	python3.7 -m pip install --upgrade pip virtualenv
	python3.7 -m virtualenv -p python3.7 .venv


.PHONY: install
install: clean ## install the package in editable mode and install all pre-commit hooks
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[tests,dev]"
	.venv/bin/pip install -U pre-commit
	.venv/bin/pre-commit install --install-hooks --overwrite


.PHONY: jupyter-init
jupyter-init: ## initialise a jupyterlab environment and install extensions
	.venv/bin/python -m ipykernel install --user --name="ridgeplot"
	.venv/bin/jupyter lab build


.PHONY: jupyter-plotly
jupyter-plotly: ## setup jupyterlab's plotly extensions
	.venv/bin/jupyter labextension install @jupyter-widgets/jupyterlab-manager \
                                           jupyterlab-plotly \
                                           plotlywidget
	.venv/bin/jupyter lab build


.PHONY: lint
lint: ## run all pre-commit hooks against all files
	.venv/bin/pre-commit run --all-files


.PHONY: test
test: ## run tests quickly with the default Python
	.venv/bin/pytest --cov=ridgeplot --cov=tests --cov-report=xml tests


.PHONY: test-all
test-all: ## run tests on every Python version with tox
	.venv/bin/tox


.PHONY: docs
docs: ## generate Sphinx HTML documentation, including API docs
	#rm -f docs/ridgeplot.rst
	#rm -f docs/modules.rst
	#sphinx-apidoc -o docs/ ridgeplot
	$(MAKE) --directory=docs clean
	$(MAKE) --directory=docs html
	$(BROWSER) docs/build/html/index.html


.PHONY: servedocs
servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .


.PHONY: dist
dist: clean ## builds source and wheel package
	.venv/bin/python setup.py sdist bdist_wheel
	.venv/bin/twine check --strict dist/*


.PHONY: release-test
release-test: dist ## package and upload a release to test pypi
	.venv/bin/twine upload --repository testpypi dist/*


.PHONY: release-prod
release-prod: dist ## package and upload a release prod pypi
	.venv/bin/twine upload dist/*


# ==============================================================
# ---  Clean
# ==============================================================

.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all artifacts (excl. venv!)


.PHONY: clean-all
clean-all: clean clean-venv ## remove all artifacts


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


.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f coverage.xml
	rm -f .coverage
	rm -fr .pytest_cache
	rm -fr .mypy_cache/


.PHONY: clean-venv
clean-venv: ## remove venv artifacts
	rm -fr .venv
