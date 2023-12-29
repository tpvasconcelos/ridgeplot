from __future__ import annotations

import platform
import subprocess
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List


def get_py_version() -> str:
    """Get the Python version environment marker."""
    return "".join(platform.python_version_tuple()[:2])


def get_sys_platform() -> str:
    """Get the Python `sys_platform` environment marker."""
    return sys.platform


def get_cibw_platform() -> str:
    """Get the platform name used by `cibuildwheel`.

    This is used by the cibuildwheel package to determine which wheels to build.
    """
    if sys.platform.startswith("linux"):
        cibw_platform = "linux"
    elif sys.platform == "darwin":
        cibw_platform = "macos"
    elif sys.platform == "win32":
        cibw_platform = "windows"
    else:
        raise ValueError(f"Unsupported platform: {platform!r}")
    return cibw_platform


ANSI_RED = "\033[31m"
ANSI_RESET = "\033[0m"


def _fail(exit_code: int, print_err_message: bool = True) -> None:
    if print_err_message:
        msg = f"{' '.join(sys.argv)!r} failed with exit code {exit_code}"
        print(f"{ANSI_RED}{msg}{ANSI_RESET}", file=sys.stderr)
    sys.exit(exit_code)


def run_subprocess(args: List[str], print_err_message: bool = True) -> None:
    print(f"Running: $ {' '.join(args)}")
    try:
        subprocess.run(args, check=True)  # noqa: S603
    except subprocess.CalledProcessError as exc:
        _fail(
            exit_code=exc.returncode,
            print_err_message=print_err_message,
        )
