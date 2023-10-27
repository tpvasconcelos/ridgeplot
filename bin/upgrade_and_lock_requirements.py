#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path

# isort: split
from utils import ToxEnvVariables, run_subprocess


def get_env_tag() -> str:
    tox_env_vars = ToxEnvVariables()
    py_version = tox_env_vars.PY_PYTHON_VERSION
    sys_platform = tox_env_vars.PY_SYS_PLATFORM
    return f"{py_version}-{sys_platform}"


def main() -> None:
    env_tag = get_env_tag()
    popen_args = [
        "pip-compile-multi",
        "--upgrade",
        f"--out-ext={env_tag}.txt",
        "--directory=requirements/",
        "--autoresolve",
        "--backtracking",
        "--allow-unsafe",
    ]
    run_subprocess(popen_args)
    for reqs_txt in Path("requirements/").glob(f"*{env_tag}.txt"):
        locked_path = Path("requirements/locked").joinpath(reqs_txt.name)
        print(f"Moving {reqs_txt} to {locked_path}")
        reqs_txt.replace(locked_path)


if __name__ == "__main__":
    main()
