# GitHub workflows

| Workflow                 | Description                                                                                                                  |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------|
| ci.yaml                  | Run all CI checks with Tox on all pushed to master or pull-request updates.                                                  |
| release.yaml             | Issues a new GitHub release whenever a new git tag is pushed.                                                                |
| publish-pypi.yaml        | Builds, packages, and uploads the source and wheel package to pypi (and test pypi) whenever a new GitHub release is created. |
| check-release-notes.yaml | **\[Experimental\]** Checks whether the user remembered to update the changelog. See source for more details.                |
