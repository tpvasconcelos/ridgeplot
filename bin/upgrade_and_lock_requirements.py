#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path

# isort: split
from utils import get_py_version, get_sys_platform, run_subprocess


def get_out_ext() -> str:
    py_version = get_py_version()
    sys_platform = get_sys_platform()
    return f"{py_version}-{sys_platform}.txt"


def main() -> None:
    out_ext = get_out_ext()
    run_subprocess(
        [
            "pip-compile-multi",
            "--upgrade",
            f"--out-ext={out_ext}",
            "--directory=requirements/",
            "--autoresolve",
            "--backtracking",
            "--allow-unsafe",
        ]
    )
    for reqs_txt in Path("requirements/").glob(f"*{out_ext}"):
        locked_path = Path("requirements/locked").joinpath(reqs_txt.name)
        print(f"Moving {reqs_txt} to {locked_path}")
        reqs_txt.replace(locked_path)


if __name__ == "__main__":
    main()
