#!/usr/bin/env python
import os
import subprocess
import sys
from pathlib import Path
from typing import List

ANSI_RED = "\033[31m"
ANSI_RESET = "\033[0m"


def _set_env_markers() -> None:
    import os
    import platform
    import sys

    env_markers = (
        ("PY_PYTHON_VERSION", "".join(platform.python_version_tuple()[:2])),
        ("PY_SYS_PLATFORM", sys.platform),
    )
    for name, value in env_markers:
        if name in os.environ:
            print(f"Not setting {name} to {value!r}, as it is already set to {os.environ[name]!r}")
            continue
        print(f"Setting {name} to {value!r}")
        os.environ[name] = value


def _exit(exit_code: int, print_err_message: bool = True) -> None:
    if print_err_message:
        cmd_original = " ".join(sys.argv)
        msg = f"{cmd_original!r} failed with exit code {exit_code}"
        print(f"{ANSI_RED}{msg}{ANSI_RESET}", file=sys.stderr)
    sys.exit(exit_code)


def _run_subprocess(popen_args: List[str]) -> None:
    cmd_string = " ".join(popen_args)
    print(f"Running: {cmd_string}")
    try:
        subprocess.run(popen_args, check=True)
    except subprocess.CalledProcessError as exc:
        _exit(exc.returncode)


def main() -> None:
    _set_env_markers()
    py_python_version = os.environ["PY_PYTHON_VERSION"]
    py_sys_platform = os.environ["PY_SYS_PLATFORM"]

    popen_args = [
        'pip-compile-multi', '--upgrade', '--allow-unsafe', '--backtracking',
        '--out-ext', f'{py_python_version}-{py_sys_platform}.txt',
    ]  # fmt: skip
    _run_subprocess(popen_args)

    for reqs_txt in Path("requirements/").glob(f"*{py_python_version}-{py_sys_platform}.txt"):
        locked_path = Path("requirements/locked").joinpath(reqs_txt.name)
        print(f"Moving {reqs_txt} to {locked_path}")
        reqs_txt.replace(locked_path)


if __name__ == "__main__":
    main()
