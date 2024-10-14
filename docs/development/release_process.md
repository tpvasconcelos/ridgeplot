# Release process

:::{admonition} This page is intended for maintainers of the project only
:class: seealso

You need to have push-access to the project's repository to make releases. Therefore, the following release steps are intended to be used as a reference for maintainers or [collaborators](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-user-account-settings/permission-levels-for-a-personal-account-repository#collaborator-access-for-a-repository-owned-by-a-personal-account) with push-access to the repository.
:::

1. Review the `## Unreleased changes` section in {repo-file}`docs/reference/changelog.md` by checking for consistency in format and, if necessary, refactoring related entries into relevant subsections (e.g., _Features_, _Docs_, _Bugfixes_, _Security_, etc.). Take a look at previous release notes for guidance and try to keep it consistent.
2. Submit a pull request with these changes only and use the `"Cleanup release notes for X.X.X release"` template for the pull request title. ridgeplot uses the [SemVer](https://semver.org/) (`MAJOR.MINOR.PATCH`) versioning standard. You can determine the latest release version by running `git describe --tags --abbrev=0` on the `main` branch. Based on this, you can determine the next release version by incrementing the MAJOR, MINOR, or PATCH. More on this in the next section. Remember to merge this pull request into the `main` branch before continuing to the next step!
3. Use the [bumpversion](https://github.com/peritus/bumpversion) utility to bump the current version. This utility will automatically bump the current version, and apply a relevant commit and git tag. E.g.,
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
    1. {repo-file}`.github/workflows/ci.yml`: Runs all integration approval checks.
    2. {repo-file}`.github/workflows/release.yml`: Builds and publishes the new packaged Python distributions to PyPi (and TestPyPi) and publishes a new GitHub Release with relevant release notes and Sigstore-certified built distributions.
6. **Trust but verify!** ⚠️
    1. Verify that all workflows [run successfully](https://github.com/tpvasconcelos/ridgeplot/actions);
    2. Verify that the new git tag [is present](https://github.com/tpvasconcelos/ridgeplot/tags) in the remote repository;
    3. Verify that the new release [is present](https://github.com/tpvasconcelos/ridgeplot/releases) in the remote repository;
        1. and that the release notes were correctly parsed
        2. and that the relevant assets were correctly uploaded
    4. Verify that the new package is available [in PyPI](https://pypi.org/project/ridgeplot/);
        1. [and TestPyPI](https://test.pypi.org/project/ridgeplot/)
    5. Verify that the docs were updated and published [to ReadTheDocs](https://ridgeplot.readthedocs.io/en/stable/).
