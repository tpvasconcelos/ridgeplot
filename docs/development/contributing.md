# Contributing

Thank you for your interest in improving ridgeplot! 🚀

We really appreciate you taking the time to help make this project better for everyone.

The contribution process for ridgeplot usually starts with [filing a GitHub issue](https://github.com/tpvasconcelos/ridgeplot/issues/new/choose). We define two main categories of issues, each with its own issue template

- ⭐ **Feature request**: Suggest a new idea or enhancement to ridgeplot
- 🐛 **Bug report**: Report an issue you encountered with ridgeplot

For broader discussions, questions, or general feedback, please head over to our [GitHub Discussions](https://github.com/tpvasconcelos/ridgeplot/discussions) page.

Please note that this is a volunteer-run project, and we may not be able to respond to every issue or pull request immediately.
Our response time may vary, but we appreciate your patience and will try to get back to you as soon as possible.

After we've triaged your issue and an implementation strategy has been agreed on by a ridgeplot maintainer, the next step is to introduce your changes as a pull request (see [](#pull-request-workflow)). Once the pull request is merged, the changes will be automatically included in the next ridgeplot release. Every significant change should be listed in the ridgeplot [Changelog](../reference/changelog.md).

The following is a set of (slightly opinionated) rules and general guidelines for contributing to ridgeplot. Emphasis on **guidelines**, not _rules_. Use your best judgment, and feel free to propose changes to this document if you think something could be improved.

(Development-environment)=
## Development environment

Here are our guidelines for setting a **working** development environment. Most of the steps have been abstracted away using the [make](<https://en.wikipedia.org/wiki/Make_(software)>) build automation tool. Feel free to peak inside the {repo-file}`Makefile` to see exactly what is being run, and in which order.

First, you will need to [clone](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#step-2-create-a-local-clone-of-your-fork) this repository. For this, make sure you have a [GitHub account](https://github.com/join), fork ridgeplot by clicking the [Fork](https://github.com/tpvasconcelos/ridgeplot/fork) button, and clone the main repository locally (_e.g.,_ using SSH)

```shell
git clone git@github.com:tpvasconcelos/ridgeplot.git
cd ridgeplot
```

You will also need to add your fork as a [remote](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories) to push your work to. Replace `{username}` with your GitHub username.

```shell
git remote add fork git@github.com:{username}/ridgeplot.git
```

### Bootstrapping the development environment

The following command will:

1. Delete any existing environment artifacts (e.g., `.venv`, `.tox`, `.pytest_cache`, etc.)
2. Create a new virtual environment under `.venv`
3. Install ridgeplot in [editable mode](https://pip.pypa.io/en/stable/cli/pip_install/#install-editable) along with all it's development dependencies
4. Set up and install all [pre-commit](https://pre-commit.com/) hooks.

```shell
make init
```

The default and **recommended** base Python is `python3.9`. However, if you encounter any issues or don't have this specific version installed on your system, you can change by it exporting the `BASE_PYTHON` environment variable to a valid executable you do have installed. Please note that we no longer support any Python versions lower than 3.9. For example, to use `python3.13`, you should run:

```shell
BASE_PYTHON=python3.13 make init
```

If you need to use jupyter in this environment, run the following command:

```shell
make jupyter-init
```

:::{admonition} Note
:class: danger

Make sure you always work within this virtual environment (_e.g.,_ `$ source .venv/bin/activate`). We also recommend that you set up your IDE to always point to this Python interpreter. If you are unsure how to do this, please refer to the documentation of your specific IDE, and get comfortable using virtual environments in Python. You can thank us later! 🐍
:::

## Pull Request Workflow

If you're reading this, it means you're probably getting ready to submit a pull request (or at least thinking about it). Either way, **congrats!** and we thank you in advance for putting in the time and effort to contribute to ridgeplot! 🎉

1. Always confirm that you have properly [configured](https://git-scm.com/docs/git-config) your name and email address in your git environment. This information will be used to identify you as a contributor in the project's commit history.
   ```shell
   # e.g., to set your name and email address globally
   git config --global user.name '<Your name>'
   git config --global user.email '<Your email address>'
   ```
2. Branch off the `main` [branch](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell).
   ```shell
   # e.g., to create a new branch named `feat/awesome-feature`
   git fetch origin
   git switch -c feat/awesome-feature origin/main
   ```
3. **Implement and commit your changes** 🚀
4. Make sure all CI checks are passing locally (see [Continuous Integration](#continuous-integration) below).
   ```shell
   tox -m static tests
   ```
5. Push your changes to your fork
   ```shell
   git push --set-upstream fork <YOUR-BRANCH-NAME>
   ```
6. [Create a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request), and remember to update the pull request's description with relevant notes on the changes implemented, and [link to relevant issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) (e.g., `fixes #XXX` or `closes #XXX`).
7. At this point, you'll probably also want to add an entry to {repo-file}`docs/reference/changelog.md` summarising the changes in this pull request. The entry should follow the same style and format as other entries, i.e.
   > `- Your summary here. ({gh-issue}`XXX`)`

   where `XXX` should be replaced with your PR's number. If you think that the changes in this pull request do not warrant a changelog entry (e.g., simply fixing a typo), please state it in your pull request's description. In such cases, a maintainer should add a `skip news` label to make the CI checks pass.
8. Wait for all remote CI checks to pass and for a ridgeplot maintainer to review your changes. If you're not done with your changes yet, you can set your pull request to a [Draft](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request) state, which will signal to the maintainers that you're still working on it. **Just remember to mark it as ready for review when you're done!**
9. Once your pull request is approved, it will be merged into the `main` branch, and your changes will be automatically included in the next ridgeplot release. 🚀

## Continuous Integration

```{epigraph}
Continuous Integration (CI): automatically builds, tests, and **integrates** code changes within a shared repository.

-- GitHub: [CI/CD: The what, why, and how](https://github.com/resources/articles/devops/ci-cd)
```

The first step to Continuous Integration (CI) is having a version control system (VCS) in place. Luckily, you don't have to worry about that! As you have astutely noticed, we use [git](https://git-scm.com/) and host on [GitHub](https://github.com/tpvasconcelos/ridgeplot).

On top of this, we also run a series of integration approval steps that allow us to ship changes faster and with greater confidence that we won't be breaking things for users down the line. In order to achieve this, we run a suite of automated tests and coverage reports, as well as a series of linters and type checkers.

### Running it locally

Our tool of choice for configuring and reliably run all integration checks is [Tox](https://github.com/tox-dev/tox), which allows us to run each step in reproducible isolated virtual environments.

To trigger all checks, simply run:

```shell
tox -m static tests
```

...yes, it's that simple! 🤓

Note that this could take a while the first time you run the command, since it will have to create all the required virtual environments (along with their dependencies) for each CI step.

The configuration for Tox and each test environment can be found in {repo-file}`tox.ini`.

If you need more control over which set of checks is running, take a look at the following two sections.

#### Tests and coverage reports

We use [pytest](https://github.com/pytest-dev/pytest) as our testing framework, and [Coverage.py](https://github.com/nedbat/coveragepy) to track and measure code coverage.

To trigger all test suites with coverage reports, run:

```shell
tox -m tests
```

If you need more control over which tests are running, or which flags are being passed to pytest, you can also invoke `tox -e pytest -- <PYTEST_FLAGS>`. For instance, to run only the tests in the `tests/unit/test_init.py` file without coverage, you could run:

```shell
tox -e pytest -- tests/unit/test_init.py --no-cov
```

For more details on how these checks are configured, take a look at the {repo-file}`pytest.ini`, {repo-file}`.coveragerc`, and/or {repo-file}`tox.ini` configuration files.

#### Static checks

This project uses [pre-commit](https://pre-commit.com/) hooks to check and automatically fix any linting code formatting issues. These checks are triggered against all [staged files](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F#_the_three_states) before creating any git commit. To manually trigger all pre-commit hooks against all files, run:

```shell
pre-commit run --all-files
```

For more information on all the checks being run here, take a look inside the {repo-file}`.pre-commit-config.yaml` configuration file.

The only static check that is not run by pre-commit is [mypy](https://github.com/python/mypy), which is too expensive to run on every commit. To run mypy against all files, run:

```shell
tox -e mypy
```

Just like with pytest, you can also pass extra positional arguments to mypy by running `tox -e mypy -- <MYPY_FLAGS>`.

To trigger all static checks, run:

```shell
tox -m static
```

### GitHub Actions

We use [GitHub Actions](https://github.com/features/actions) to automatically run all integration approval steps defined with Tox on every push or pull request event. These checks run on all major operating systems and all supported Python versions. Coverage data is also uploaded to [Codecov](https://about.codecov.io/) and [Codacy](https://www.codacy.com/) here. Check {repo-file}`.github/workflows` for more details.

Additionally, we use [CodeQL](https://securitylab.github.com/tools/codeql) to automatically check for security vulnerabilities in the codebase. This check is set to run every day but also on every push or pull request event. Check {repo-file}`.github/workflows/codeql.yml` for more details.

Finally, we have a small workflow (see {repo-file}`.github/workflows/check-release-notes.yml`) that checks if the PR author remembered to add an entry to the changelog. If the PR does not warrant a changelog entry, the author can add a `skip news` label to make the CI checks pass.

## Tools and software

Here is a quick overview of ~~all~~ most of the CI tools and software used in this project, along with their respective configuration files. If you have any questions or need help with any of these tools, feel free to ask for help from the community by commenting on your issue or pull request.

| Tool                                                                       | Category         | config files                          | Details                                                                                                                                                                                                |
|----------------------------------------------------------------------------|------------------|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Tox](https://github.com/tox-dev/tox)                                      | 🔧 Orchestration | {repo-file}`tox.ini`                  | We use Tox to reliably run all integration approval steps in reproducible isolated virtual environments.                                                                                               |
| [GitHub Actions](https://github.com/features/actions)                      | 🔧 Orchestration | {repo-file}`.github/workflows/ci.yml` | Workflow automation for GitHub. We use it to automatically run all integration approval steps on every push or pull request event.                                                                     |
| [git](https://git-scm.com/)                                                | 🕰 VCS           | {repo-file}`.gitignore`               | The project's version control system.                                                                                                                                                                  |
| [pytest](https://github.com/pytest-dev/pytest)                             | 🧪 Testing       | {repo-file}`pytest.ini`               | Testing framework for python code.                                                                                                                                                                     |
| [Coverage.py](https://github.com/nedbat/coveragepy)                        | 📊 Coverage      | {repo-file}`.coveragerc`              | The code coverage tool for Python                                                                                                                                                                      |
| [Codecov](https://about.codecov.io/) and [Codacy](https://www.codacy.com/) | 📊 Coverage      | {repo-file}`.github/workflows/ci.yml` | Two external services for tracking, monitoring, and alerting on code coverage and code quality.                                                                                                        |
| [pre-commit](https://pre-commit.com/)                                      | 💅 Linting       | {repo-file}`.pre-commit-config.yaml`  | Used to to automatically check and fix any formatting rules on every commit.                                                                                                                           |
| [mypy](https://github.com/python/mypy)                                     | 💅 Linting       | {repo-file}`mypy.ini`                 | A static type checker for Python. We use quite a strict configuration here, which can be tricky at times. Feel free to ask for help from the community by commenting on your issue or pull request.    |
| [black](https://github.com/psf/black)                                      | 💅 Linting       | {repo-file}`pyproject.toml`           | "The uncompromising Python code formatter". We use `black` to automatically format Python code in a deterministic manner. Maybe we'll replace this with `ruff` in the future.                          |
| [ruff](https://github.com/astral-sh/ruff)                                  | 💅 Linting       | {repo-file}`ruff.toml`                | "An extremely fast Python linter and code formatter, written in Rust." For this project, ruff replaced Flake8 (+plugins), isort, pydocstyle, pyupgrade, and autoflake with a single (and faster) tool. |
| [EditorConfig](https://editorconfig.org/)                                  | 💅 Linting       | {repo-file}`.editorconfig`            | This repository uses the `.editorconfig` standard configuration file, which aims to ensure consistent style across multiple programming environments.                                                  |
| [bumpversion](https://github.com/c4urself/bump2version)                    | 📦 Packaging     | {repo-file}`.bumpversion.cfg`         | A small command line tool to simplify releasing software by updating all version strings in your source code by the correct increment.                                                                 |


## Code of Conduct

Please remember to read and follow our standard {repo-file}`Code of Conduct <CODE_OF_CONDUCT.md>`. 🤝
