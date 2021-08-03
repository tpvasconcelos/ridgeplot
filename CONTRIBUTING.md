# Contributing

Thanks for taking the time and considering contributing to `ridgeplot`! 🚀

The following is a set of (slightly opinionated) rules and general guidelines for contributing to
`ridgeplot`. Emphasis on **guidelines**, not _rules_. Use your best judgment, and feel
free to propose changes to this document in a pull request.

Examples of contributions include:

- Code patches
- Documentation improvements
- Bug reports and patch reviews

## Code of Conduct

Please remember to read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). 🤝

## Development environment

Here are some guidelines for setting up your development environment. Most of the steps have been abstracted
away using the [`make`](https://en.wikipedia.org/wiki/Make_(software)) build automation tool. Feel free to
peak inside [`Makefile`](Makefile) at any time to see exactly what is being run, and in which order.

First, you will need to clone this repository. For instance (using SSH)

```shell
git clone git@github.com:tpvasconcelos/ridgeplot.git
cd ridgeplot
```

The following command will 1) create a new virtual environment, 2) install `ridgeplot`
in [editable mode](https://pip.pypa.io/en/stable/cli/pip_install/#install-editable) (along with all it's
dependencies), and 3) set up and install all [pre-commit hooks](https://pre-commit.com/). The default path to
the virtual environment is `.venv`, which is ignored by all Continuous Integration tools used in this project.

```shell
make init
```

The default and **recommended** base python is `python3.7` . You can change this by exporting the
`BASE_PYTHON` environment variables. For instance, you could instead run:

```shell
BASE_PYTHON=python3.8 make init
```

If you need to use jupyter-lab, you can install all extra requirements, as well as set up the environment and
jupyter kernel with

```shell
make jupyter-init
```

**Bonus:** If you need to use
[plotly inside a jupyter-lab](https://plotly.com/python/getting-started/#jupyterlab-support)
notebook, just run

```shell
make jupyter-plotly
```

## Continuous Integration

From GitHub's
[Continuous Integration and Continuous Delivery (CI/CD) Fundamentals](https://resources.github.com/ci-cd/):
> _Continuous Integration (CI) automatically builds, tests, and **integrates** code changes within a shared
> repository._

The first step to Continuous Integration (CI) is having a version control system (VCS) in place. Luckily, you
don't have to worry about that! As you have already noticed, we use [Git](https://git-scm.com/) and host
on [GitHub](https://github.com/tpvasconcelos/ridgeplot).

On top of this, we also run a series of integration approval steps that allow us to ship code changes faster
and more reliably. In order to achieve this, we run automated tests and coverage reports, as well as syntax
(and type) checkers, code style formatters, and dependency vulnerability scans.

### Running it locally

Our tool of choice to configure and reliably run all integration approval steps is
[Tox](https://github.com/tox-dev/tox), which allows us to run each step in reproducible isolated virtual
environments. To trigger all checks, simply run

```shell
tox
```

It's that simple 🙌 !! Note only that this will take a while the first time you run the command, since it will
have to create all the required virtual environments (along with their dependencies) for each CI step.

The configuration for Tox can be found in [`tox.ini`](tox.ini).

#### Tests and coverage reports

We use [`pytest`](https://github.com/pytest-dev/pytest) as our testing framework,
and [`pytest-cov`](https://pytest-cov.readthedocs.io/en/latest/) to track and measure code coverage. You can
find all configuration details in [`tox.ini`](tox.ini). To trigger all tests, simply run

```shell
tox -e py
```

You can also run your tests against any other supported python versions (e.g., `tox -e py38`). If you need
more control over which tests are running, or which flags are being passed to pytest, you can also
invoke `pytest` directly which will run on your current virtual environment. Configuration details can be
found in [`tox.ini`](tox.ini).

#### Linting

This project uses [pre-commit hooks](https://pre-commit.com/) to check and automatically fix any formatting
rules. These checks are triggered before creating any git commit. To manually trigger all linting steps (i.e.,
all pre-commit hooks), run

```shell
tox -e lint
```

For more information on which hooks will run, have a look inside the
[`.pre-commit-config.yaml`](.pre-commit-config.yaml) configuration file. If you want to manually trigger
individual hooks, you can invoke the `pre-commit` script directly. If you need even more control over the
tools used you could also invoke them directly (e.g., `isort .`). Remember however that this is **not** the
recommended approach.

### GitHub Actions

We use [GitHub Actions](https://github.com/features/actions) to automatically run all integration approval
steps defined with Tox on every push or pull request event. These checks run on all major operating systems
and all supported Python versions. Finally, the generated coverage reports are uploaded to
[Codecov](https://about.codecov.io/) and [Codacy](https://www.codacy.com/).
Check [`.github/workflows/ci.yaml`](.github/workflows/ci.yaml) for more details.

### Tools and software

Here is a quick overview of all CI tools and software in use, some of which have already been discussed in the
sections above.

| Tool                                                                       | Category         | config files                                             | Details      |
| -------------------------------------------------------------------------- | ---------------- | -------------------------------------------------------  | ------------ |
| [Tox](https://github.com/tox-dev/tox)                                      | 🔧 Orchestration | [`tox.ini`](tox.ini)                                     | We use Tox to reliably run all integration approval steps in reproducible isolated virtual environments. |
| [GitHub Actions](https://github.com/features/actions)                      | 🔧 Orchestration | [`.github/workflows/ci.yaml`](.github/workflows/ci.yaml) | Workflow automation for GitHub. We use it to automatically run all integration approval steps defined with Tox on every push or pull request event. |
| [Git](https://git-scm.com/)                                                | 🕰 VCS           | [`.gitignore`](.gitignore)                               | Projects version control system software of choice. |
| [pytest](https://github.com/pytest-dev/pytest)                             | 🧪 Testing       | [`tox.ini`](tox.ini)                                     | Testing framework for python code. |
| [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)                 | 📊 Coverage      | [`tox.ini`](tox.ini)                                     | Coverage plugin for pytest. |
| [Codecov](https://about.codecov.io/) and [Codacy](https://www.codacy.com/) | 📊 Coverage      |                                                          | Two great services for tracking, monitoring, and alerting on code coverage and code quality. |
| [pre-commit hooks](https://pre-commit.com/)                                | 💅 Linting       | [`.pre-commit-config.yaml`](.pre-commit-config.yaml)     | Used to to automatically check and fix any formatting rules on every commit. |
| [mypy](https://github.com/python/mypy)                                     | 💅 Linting       | [`mypy.ini`](mypy.ini)                                   | A static type checker for Python. We use quite a strict configuration here, which can be tricky at times. Feel free to ask for help from the community by commenting on your issue or pull request. |
| [black](https://github.com/psf/black)                                      | 💅 Linting       | [`pyproject.toml`](pyproject.toml)                       | "The uncompromising Python code formatter". We use `black` to automatically format Python code in a deterministic manner. We use a maximum line length of 120 characters. |
| [flake8](https://github.com/pycqa/flake8)                                  | 💅 Linting       | [`setup.cfg`](setup.cfg)                                 | Used to check the style and quality of python code. |
| [isort](https://github.com/pycqa/isort)                                    | 💅 Linting       | [`setup.cfg`](setup.cfg)                                 | Used to sort python imports. |
| [EditorConfig](https://editorconfig.org/)                                  | 💅 Linting       | [`.editorconfig`](.editorconfig)                         | This repository uses the `.editorconfig` standard configuration file, which aims to ensure consistent style across multiple programming environments. |

## Project structure

### Community health files

GitHub's community health files allow repository maintainers to set contributing guidelines to help
collaborators make meaningful, useful contributions to a project. Read more on this official
[reference](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions).

- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) - A CODE_OF_CONDUCT file defines standards for how to engage in a
  community. For more information, see
  "[Adding a code of conduct to your project.](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project)"
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - A CONTRIBUTING file communicates how people should contribute to your
  project. For more information, see
  "[Setting guidelines for repository contributors.](https://docs.github.com/en/articles/setting-guidelines-for-repository-contributors)"

### Configuration files

For more context on some of the tools referenced below, refer to the sections
on [Continuous Integration](#continuous-integration).

- [`.github/workflows/ci.yaml`](.github/workflows/ci.yaml) - Workflow definition for our CI GitHub Actions
  pipeline.
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml) - List of pre-commit hooks.
- [`.editorconfig`](.editorconfig) -
  [EditorConfig](https://editorconfig.org/) standard configuration file.
- [`mypy.ini`](mypy.ini) - Configuration for the `mypy` static type checker.
- [`pyproject.toml`](pyproject.toml) -
  [build system](https://setuptools.readthedocs.io/en/latest/build_meta.html) requirements (probably won't
  need to touch these!) and [`black`](https://github.com/psf/black) configurations.
- [`setup.cfg`](setup.cfg) - Here, we specify the package metadata, requirements, as well as configuration
  details for [`flake8`](https://github.com/pycqa/flake8) and [`isort`](https://github.com/pycqa/isort).
- [`tox.ini`](tox.ini) - Configuration for [`tox`](https://github.com/tox-dev/tox),
  [`pytest`](https://github.com/pytest-dev/pytest), and
  [`coverage`](https://coverage.readthedocs.io/en/latest/index.html).
