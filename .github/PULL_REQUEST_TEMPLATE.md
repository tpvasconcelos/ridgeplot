## Description

<!--
Please try to include a summary of your changes here.
-->

## Related issues

<!--
If you're addressing an existing issue, please reference it here.
You can use keywords like "closes", "fixes", or "resolves" to automatically close the issue when the PR is merged.
-->

## PR check list

<!--
Sorry for the long list!

Please try to tick all boxes below, even the ones that don't apply to your PR.
This will let us know that at least you've considered these points.

If you have any questions at all, don't hesitate to ask. We're here to help!
The checklist below is only here to help you, not to scare you away! 🤓
-->

- [ ] Read the [contributing guidelines](https://ridgeplot.readthedocs.io/en/latest/development/contributing.html).
  - You don't have to read the whole thing, but it's a good idea to skim it. And definitely take a look at it if you're experiencing any issues getting your local environment up and running.
- [ ] Provided the relevant details in the PR's description.
- [ ] Referenced relevant issues in the PR's description.
- [ ] Added tests for all my changes.
  - The CI will fail unless 100% of all new code is covered by the tests.
- [ ] Updated the docs for relevant changes.
  - [ ] New modules (or renamed ones) are included in `docs/api/internal/`.
  - [ ] New public functions/classes/variables are documented in `docs/api/index.rst`.
  - [ ] Added the appropriate `versionadded`, `versionchanged`, or `deprecated` [directives](http://www.sphinx-doc.org/en/stable/markup/para.html#directive-versionadded) to docstrings.
    - The version should be the next release version, which you can infer by bumping the minor version in `MAJOR.MINOR.PATCH` (e.g., if the current version is `0.2.3`, the next release will be `0.3.0`).
- [ ] Changes are documented in `docs/reference/changelog.md`.
  - Please try to follow the conventions laid out in the file. In doubt, just ask!
- [ ] Consider granting [push permissions to your PR's branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/allowing-changes-to-a-pull-request-branch-created-from-a-fork), so maintainers can help you out if needed.
- [ ] The CI check are all passing, or I'm working on fixing them!
- [ ] I have reviewed my own code! 🤠
