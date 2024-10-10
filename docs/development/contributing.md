# Contributing

**Thank you for your interest in improving ridgeplot!** 🚀

We really appreciate you taking the time to help make this project better for everyone.

The contribution process for ridgeplot usually starts with [filing a GitHub issue](https://github.com/tpvasconcelos/ridgeplot/issues/new/choose). We define three main categories of issues, each with its own issue template

- ⭐ **Feature request**: Have an idea for a new feature or an enhancement to existing functionality? This is the place to share it.
- 🐛 **Bug report**: Encountered a problem or noticed something not working as expected? Please let us know.
- 📚 **Documentation improvement**: Spotted a typo, missing info, or have suggestions for a new section or example? We'd love to hear about it.

For broader discussions, questions, or general feedback, please head over to [GitHub Discussions](https://github.com/tpvasconcelos/ridgeplot/discussions).

Our response times may vary, but we'll get back to you as soon as we can!

After the implementation strategy has been agreed on by a ridgeplot contributor, the next step is to introduce your changes as a pull request (see [](#pull-request-workflow)) against the ridgeplot repository. Once your pull request is merged, your changes will be automatically included in the next ridgeplot release. Every change should be listed in the ridgeplot [Changelog](../reference/changelog.md).

The following is a set of (slightly opinionated) rules and general guidelines for contributing to ridgeplot. Emphasis on **guidelines**, not _rules_. Use your best judgment, and feel free to propose changes to this document in a pull request.

(Development-environment)=
## Development environment

Here are some guidelines for setting up your development environment. Most of the steps have been abstracted away using the [make](<https://en.wikipedia.org/wiki/Make_(software)>) build automation tool. Feel free to peak inside {repo-file}`Makefile` at any time to see exactly what is being run, and in which order.

First, you will need to [clone](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#step-2-create-a-local-clone-of-your-fork) this repository. For this, make sure you have a [GitHub account](https://github.com/join), fork ridgeplot to your GitHub account by clicking the [Fork](https://github.com/tpvasconcelos/ridgeplot/fork) button, and clone the main repository locally (e.g. using SSH)

```shell
git clone git@github.com:tpvasconcelos/ridgeplot.git
cd ridgeplot
```

You will also need to add your fork as a remote to push your work to. Replace `{username}` with your GitHub username.

```shell
git remote add fork git@github.com:{username}/ridgeplot.git
```

The following command will 1) create a new virtual environment (under `.venv`), 2) install ridgeplot in [editable mode](https://pip.pypa.io/en/stable/cli/pip_install/#install-editable) (along with all it's dependencies), and 3) set up and install all [pre-commit hooks](https://pre-commit.com/). Make sure you always work within this virtual environment (i.e., `$ source .venv/bin/activate`). On top of this, you should also set up your IDE to always point to this python interpreter. In PyCharm, open `Preferences -> Project: ridgeplot -> Project Interpreter` and point the python interpreter to `.venv/bin/python`.

```shell
make init
```

The default and **recommended** base python is `python3.9`. You can change this by exporting the `BASE_PYTHON` environment variable:

```shell
BASE_PYTHON=python3.13 make init
```

If you need to use jupyter-lab, you can install all extra requirements, as well as set up the environment and jupyter kernel with

```shell
make init-jupyter
```

## Pull Request Workflow

1. Always confirm that you have properly configured your Git username and email.
   ```shell
   git config --global user.name '<Your name>'
   git config --global user.email '<Your email address>'
   ```
2. Branch off the `main` branch:
   ```shell
   git fetch origin
   git branch <YOUR-BRANCH-NAME> origin/main
   ```
3. Implement and commit your changes.
4. Make sure that all integration approval steps are passing locally (see [Continuous Integration](#continuous-integration) below).
   ```shell
   tox -p -m static tests
   ```
5. Push your changes to your fork
   ```shell
   git push --set-upstream fork <YOUR-BRANCH-NAME>
   ```
6. [Create a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request), and remember to update the pull request's description with relevant notes on the changes implemented, and [link to relevant issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) (e.g., `fixes #XXX` or `closes #XXX`).
7. At this point, you'll probably also want to add an entry to {repo-file}`docs/reference/changelog.md` summarising the changes in this pull request. The entry should follow the same style and format as other entries, i.e.
   > `- Your summary here. ({gh-issue}`XXX`)`
   where `XXX` should be replaced with your PR's number. If you think that the changes in this pull request do not warrant a changelog entry, please state it in your pull request's description. In such cases, a maintainer should add a `skip news` label to make CI pass.
8. Wait for all remote CI checks to pass and for a ridgeplot contributor to approve your pull request.
9. Once your pull request is approved, it will be merged into the `main` branch, and your changes will be automatically included in the next ridgeplot release.

## Continuous Integration

From GitHub's [Continuous Integration and Continuous Delivery (CI/CD) Fundamentals](https://resources.github.com/ci-cd/):

> _Continuous Integration (CI) automatically builds, tests, and **integrates** code changes within a shared repository._

The first step to Continuous Integration (CI) is having a version control system (VCS) in place. Luckily, you don't have to worry about that! As you have already noticed, we use [git](https://git-scm.com/) and host on [GitHub](https://github.com/tpvasconcelos/ridgeplot).

On top of this, we also run a series of integration approval steps that allow us to ship code changes faster and more reliably. In order to achieve this, we run automated tests and coverage reports, as well as syntax (and type) checkers, code style formatters, and dependency vulnerability scans.

### Running it locally

Our tool of choice to configure and reliably run all integration approval steps is [Tox](https://github.com/tox-dev/tox), which allows us to run each step in reproducible isolated virtual environments. To trigger all checks in parallel, simply run:

```shell
tox -p -m static tests
```

It's that simple 🙌 !! Note that this could take a while the first time you run the command, since it will have to create all the required virtual environments (along with their dependencies) for each CI step.

The configuration for Tox can be found in {repo-file}`tox.ini`.

#### Tests and coverage reports

We use [pytest](https://github.com/pytest-dev/pytest) as our testing framework, and [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) to track and measure code coverage. To trigger all tests in parallel, run:

```shell
tox -p -m tests
```

If you need more control over which tests are running, or which flags are being passed to pytest, you can also invoke `tox -e pytest -- <PYTEST_FLAGS>`. For instance, to run only the tests in the `tests/unit/test_init.py` file without coverage, you could run:

```shell
tox -e pytest -- tests/unit/test_init.py --no-cov
```

For more details on how these checks are configured, take a look at the {repo-file}`pytest.ini`, {repo-file}`.coveragerc`, and/or {repo-file}`tox.ini` configuration files.

#### Linting and formatting

This project uses [pre-commit hooks](https://pre-commit.com/) to check and automatically fix any code formatting issues. These checks are triggered against all [staged files](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F/#_the_three_states) before creating any git commit. To manually trigger all pre-commit hooks against all files, run:

```shell
pre-commit run --all-files
```

For more information on all the checks being run, take a look inside the {repo-file}`.pre-commit-config.yaml` configuration file.

### GitHub Actions

We use [GitHub Actions](https://github.com/features/actions) to automatically run all integration approval steps defined with Tox on every push or pull request event. These checks run on all major operating systems and all supported Python versions. Finally, the generated coverage reports are uploaded to [Codecov](https://about.codecov.io/) and [Codacy](https://www.codacy.com/). Check {repo-file}`.github/workflows/ci.yaml` for more details.

### Tools and software

Here is a quick overview of ~all~ most of the CI tools and software used in this project, along with their respective configuration files. If you have any questions or need help with any of these tools, feel free to ask for help from the community by commenting on your issue or pull request.

| Tool                                                                       | Category         | config files                           | Details                                                                                                                                                                                                |
|----------------------------------------------------------------------------|------------------|----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Tox](https://github.com/tox-dev/tox)                                      | 🔧 Orchestration | {repo-file}`tox.ini`                   | We use Tox to reliably run all integration approval steps in reproducible isolated virtual environments.                                                                                               |
| [GitHub Actions](https://github.com/features/actions)                      | 🔧 Orchestration | {repo-file}`.github/workflows/ci.yaml` | Workflow automation for GitHub. We use it to automatically run all integration approval steps defined with Tox on every push or pull request event.                                                    |
| [git](https://git-scm.com/)                                                | 🕰 VCS           | {repo-file}`.gitignore`                | Projects version control system software of choice.                                                                                                                                                    |
| [pytest](https://github.com/pytest-dev/pytest)                             | 🧪 Testing       | {repo-file}`tox.ini`                   | Testing framework for python code.                                                                                                                                                                     |
| [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)                 | 📊 Coverage      | {repo-file}`tox.ini`                   | Coverage plugin for pytest.                                                                                                                                                                            |
| [Codecov](https://about.codecov.io/) and [Codacy](https://www.codacy.com/) | 📊 Coverage      | {repo-file}`.github/workflows/ci.yaml` | Two great services for tracking, monitoring, and alerting on code coverage and code quality.                                                                                                           |
| [pre-commit hooks](https://pre-commit.com/)                                | 💅 Linting       | {repo-file}`.pre-commit-config.yaml`   | Used to to automatically check and fix any formatting rules on every commit.                                                                                                                           |
| [mypy](https://github.com/python/mypy)                                     | 💅 Linting       | {repo-file}`mypy.ini`                  | A static type checker for Python. We use quite a strict configuration here, which can be tricky at times. Feel free to ask for help from the community by commenting on your issue or pull request.    |
| [black](https://github.com/psf/black)                                      | 💅 Linting       | {repo-file}`pyproject.toml`            | "The uncompromising Python code formatter". We use `black` to automatically format Python code in a deterministic manner. Maybe we'll replace this with `ruff` in the future.                          |
| [ruff](https://github.com/astral-sh/ruff)                                  | 💅 Linting       | {repo-file}`ruff.toml`                 | "An extremely fast Python linter and code formatter, written in Rust." For this project, ruff replaced Flake8 (+plugins), isort, pydocstyle, pyupgrade, and autoflake with a single (and faster) tool. |
| [EditorConfig](https://editorconfig.org/)                                  | 💅 Linting       | {repo-file}`.editorconfig`             | This repository uses the `.editorconfig` standard configuration file, which aims to ensure consistent style across multiple programming environments.                                                  |
| [bumpversion](https://github.com/c4urself/bump2version)                    | 📦 Packaging     | {repo-file}`.bumpversion.cfg`          | A small command line tool to simplify releasing software by updating all version strings in your source code by the correct increment.                                                                 |

## Release process

You need to have push-access to the project's repository to make releases. Therefore, the following release steps are intended to be used as a reference for maintainers and [contributors](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-user-account-settings/permission-levels-for-a-personal-account-repository#collaborator-access-for-a-repository-owned-by-a-personal-account) with push-access to the repository.

1. Review the `## Unreleased changes` section in {repo-file}`docs/reference/changelog.md` by checking for consistency in format and, if necessary, refactoring related entries into relevant subsections (e.g., _Features_, _Docs_, _Bugfixes_, _Security_, etc.). Take a look at previous release notes for guidance and try to keep it consistent.
2. Submit a pull request with these changes only and use the `"Cleanup release notes for X.X.X release"` template for the pull request title. ridgeplot uses the [SemVer](https://semver.org/) (`MAJOR.MINOR.PATCH`) versioning standard. You can determine the latest release version by running `git describe --tags --abbrev=0` on the `main` branch. Based on this, you can determine the next release version by incrementing the MAJOR, MINOR, or PATCH. More on this in the next section. Remember to merge this pull request into the `main` branch before continuing to the next step!
3. TODO: Put steps 4. and 5. in a separate script in `cicd_utils/` and call it from here. The script should ask for user confirmation before proceeding. To avoid accidental releases, maybe require the user to type out the exact version to be released (you can include the version in the script's output so the user can copy-paste it). The script to validate that the user is running the script from the correct cwd, git branch (`main`), set the `SKIP='no-commit-to-branch'` environment variable to skip the pre-commit hook that doesn't allow commits to the `main` branch, and finally, run the `bumpversion <major|minor|patch>` command. Maybe ask for confirmation to push all changes and new tags to the remote repository or to revert all changes and tags if the user decides to cancel the release?
4. Use the [bumpversion](https://github.com/peritus/bumpversion) utility to bump the current version. This utility will automatically bump the current version, and apply a relevant commit and git tag. E.g.,
   ```shell
   # Bump MAJOR version (e.g., 0.4.2 -> 1.0.0)
   SKIP='no-commit-to-branch' bumpversion major

   # Bump MINOR version (e.g., 0.4.2 -> 0.5.0)
   SKIP='no-commit-to-branch' bumpversion minor

   # Bump PATCH version (e.g., 0.4.2 -> 0.4.3)
   SKIP='no-commit-to-branch' bumpversion patch
   ```
   You can always perform a dry-run to see what will happen under the hood.
   ```shell
   bumpversion --dry-run --verbose [--allow-dirty] [major,minor,patch]
   ```
4. Push your changes along with the new git tag to the remote repository.
   ```shell
   git push --follow-tags
   ```
5. At this point, a couple of GitHub Actions workflows will be triggered:
    1. {repo-file}`.github/workflows/ci.yaml`: Runs all integration approval checks.
    2. {repo-file}`.github/workflows/release.yaml`: Builds and publishes the new packaged Python distributions to PyPi (and TestPyPi) and publishes a new GitHub Release with relevant release notes and Sigstore-certified built distributions.
6. **Trust but verify!**
    1. Verify that all workflows run successfully: <https://github.com/tpvasconcelos/ridgeplot/actions>
    2. Verify that the new git tag is present in the remote repository: <https://github.com/tpvasconcelos/ridgeplot/tags>
    3. Verify that the new release is present in the remote repository: <https://github.com/tpvasconcelos/ridgeplot/releases>
        1. and that the release notes were correctly parsed
        2. and that the relevant assets were correctly uploaded
    4. Verify that the new package is available in PyPI: <https://pypi.org/project/ridgeplot/>
        1. and TestPyPI: <https://test.pypi.org/project/ridgeplot/>
    5. Verify that the docs were updated and published to <https://ridgeplot.readthedocs.io/en/stable/>

## Code of Conduct

Please remember to read and follow our standard {repo-file}`Code of Conduct <CODE_OF_CONDUCT.md>`. 🤝
