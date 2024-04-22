# GitHub workflows

| Workflow                 | Description                                                                                                                           |
| ------------------------ |---------------------------------------------------------------------------------------------------------------------------------------|
| check-release-notes.yaml | Checks whether the user remembered to update the changelog.                                                                           |
| ci.yaml                  | Run all CI checks on all pushes to the main branch or pull-request updates.                                                           |
| release.yaml             | Publishes a new GitHub release whenever a new git tag is pushed, followed by building and publishing the new package version to PyPI. |
