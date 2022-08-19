# Requirements files

| Requirements file                        | Used in:                                                                                         | Inherits from:                 |
|------------------------------------------|--------------------------------------------------------------------------------------------------|--------------------------------|
| requirements/tox.txt                     | - .github/workflows/publish-pypi.yaml<br>- .github/workflows/ci.yaml<br>- requirements/typing.in |                                |
| requirements/pre-commit.txt              | - tox.ini:testenv:lint<br>- requirements/local-dev.in<br>- requirements/dependency-management.in |                                |
| requirements/tests.txt                   | - tox.ini:testenv<br>- requirements/typing.in                                                    | - `-e file:.`                  |
| requirements/typing.txt                  | - tox.ini:testenv:typing                                                                         | - `-r tests.in`                |
| requirements/docs.txt                    | - tox.ini:testenv:docs<br>- .readthedocs.yaml                                                    | - `-e file:.`                  |
| requirements/dependency-management.txt   | - tox.ini:testenv:upgrade-deps<br>- requirements/local-dev.in                                    | - `-r pre-commit.in`           |
| requirements/release.txt                 | - tox.ini:testenv:build<br>-tox.ini:testenv:release-test<br>-tox.ini:testenv:release-prod        |                                |
| requirements/local-dev.txt               | - Makefile                                                                                       | - `-e file:.`<br>- `-r tox.in` |
