from __future__ import annotations

import platform
import subprocess
import sys
from dataclasses import dataclass, field
from importlib.abc import Loader
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Any, List, Tuple, Union, cast


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


@dataclass
class ToxEnvMarkers:
    """Set the environment markers used in tox.ini to determine which locked
    requirements file to use.

    Take a look at the tox.ini file to see how these are used.
    """

    PY_PYTHON_VERSION: str = field(default_factory=get_py_version)
    PY_SYS_PLATFORM: str = field(default_factory=get_sys_platform)

    def set_env(self) -> None:
        import os

        env_markers = (
            ("PY_PYTHON_VERSION", self.PY_PYTHON_VERSION),
            ("PY_SYS_PLATFORM", self.PY_SYS_PLATFORM),
        )
        for name, value in env_markers:
            if name in os.environ:
                print(
                    f"Not setting {name} to {value!r}, as it is already set to {os.environ[name]!r}"
                )
                continue
            print(f"Setting {name} to {value!r}")
            os.environ[name] = value


def set_tox_env_markers() -> None:
    ToxEnvMarkers().set_env()


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
        subprocess.run(popen_args, check=True)
    except subprocess.CalledProcessError as exc:
        _fail(exc.returncode, print_err_message=print_err_message)
