# Requirements files

| Requirements file         | Used in:                                                                                               | Inherits from:                 |
|---------------------------|--------------------------------------------------------------------------------------------------------| ------------------------------ |
| tox.txt                   | - .github/workflows/publish-pypi.yaml<br>- .github/workflows/ci.yaml<br>- requirements/mypy.in         |                                |
| pre-commit.txt            | - tox.ini:testenv:pre-commit<br>- requirements/local-dev.in<br>- requirements/dependency-management.in |                                |
| tests.txt                 | - tox.ini:testenv<br>- requirements/mypy.in                                                            | - `-e file:.`                  |
| mypy.txt                  | - tox.ini:testenv:mypy                                                                                 | - `-r tests.in`                |
| docs.txt                  | - tox.ini:testenv:docs<br>- .readthedocs.yaml                                                          | - `-e file:.`                  |
| dependency-management.txt | - tox.ini:testenv:upgrade-deps<br>- requirements/local-dev.in                                          | - `-r pre-commit.in`           |
| release.txt               | - tox.ini:testenv:build<br>- tox.ini:testenv:publish-pypi-test<br>- tox.ini:testenv:publish-pypi       |                                |
| release-notes.txt         | - tox.ini:testenv:release-notes                                                                        |                                |
| local-dev.txt             | - Makefile                                                                                             | - `-e file:.`<br>- `-r tox.in` |
