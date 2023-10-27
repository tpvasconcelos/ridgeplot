from __future__ import annotations

import os
import platform
import subprocess
import sys
from dataclasses import dataclass, field
from importlib.abc import Loader
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from types import ModuleType
    from typing import Any, List, Tuple, Union


def import_pyscript_as_module(path: Union[str, Path]) -> ModuleType:
    """Import a Python script as a module.

    Parameters
    ----------
    path
        The path to the Python file to import as a module.

    Returns
    -------
    ModuleType
        The imported module.

    .. note::

        This was mostly taken from the Python docs:
        https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    """
    path_posix = Path(path).resolve().as_posix()
    module_name = path_posix.split("/")[-1].split(".")[0]
    spec = cast(
        ModuleSpec,
        spec_from_file_location(
            name=module_name,
            location=path_posix,
        ),
    )
    module = module_from_spec(spec)
    sys.modules[module_name] = module
    loader = cast(Loader, spec.loader)
    loader.exec_module(module)
    return module


def import_attrs_from_pyscript(path: Union[str, Path], *attributes: str) -> Tuple[Any, ...]:
    r"""Import attributes from a Python script.

    Parameters
    ----------
    path
        The path to the Python file to import.
    \*attributes
        The attributes to import from the module.

    Returns
    -------
    Tuple[Any, ...]
        The imported attributes.

    Examples
    --------
    So, instead of doing

    >>> from path.to.script import Foo, bar

    You can instead do:

    >>> Foo, bar = import_attrs_from_pyscript("path/to/script.py", "Foo", "bar")

    """
    module = import_pyscript_as_module(path)
    return tuple(getattr(module, attr) for attr in attributes)


def get_py_version() -> str:
    """Get the Python version environment marker."""
    return "".join(platform.python_version_tuple()[:2])


def get_sys_platform() -> str:
    """Get the Python sys_platform environment marker."""
    return sys.platform


def get_cibw_platform() -> str:
    """Get the platform name used by cibuildwheel.

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


@dataclass
class ToxEnvVariables:
    """Set the environment variables used in tox.ini.

    PY_PYTHON_VERSION and PY_SYS_PLATFORM are used to determine which locked
    requirements file to use, while CIBW_PLATFORM is used by cibuildwheel to
    determine which wheels to build.

    Take a look inside tox.ini for more details.
    """

    PY_PYTHON_VERSION: str = field(default_factory=get_py_version)
    PY_SYS_PLATFORM: str = field(default_factory=get_sys_platform)
    CIBW_PLATFORM: str = field(default_factory=get_cibw_platform)

    def set_env(self) -> None:
        env_vars = (
            ("PY_PYTHON_VERSION", self.PY_PYTHON_VERSION),
            ("PY_SYS_PLATFORM", self.PY_SYS_PLATFORM),
            ("CIBW_PLATFORM", self.CIBW_PLATFORM),
        )
        for name, value in env_vars:
            if name in os.environ:
                print(
                    f"Not setting {name} to {value!r}, as it is already set to {os.environ[name]!r}"
                )
                continue
            print(f"Setting {name} to {value!r}")
            os.environ[name] = value


def set_tox_env_variables() -> None:
    ToxEnvVariables().set_env()


ANSI_RED = "\033[31m"
ANSI_RESET = "\033[0m"


def _fail(exit_code: int, print_err_message: bool = True) -> None:
    if print_err_message:
        msg = f"{' '.join(sys.argv)!r} failed with exit code {exit_code}"
        print(f"{ANSI_RED}{msg}{ANSI_RESET}", file=sys.stderr)
    sys.exit(exit_code)


def run_subprocess(popen_args: List[str], print_err_message: bool = True) -> None:
    print(f"Running: {' '.join(popen_args)}")
    try:
        subprocess.run(popen_args, check=True)  # noqa: S603
    except subprocess.CalledProcessError as exc:
        _fail(exc.returncode, print_err_message=print_err_message)
