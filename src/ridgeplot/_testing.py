from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, Optional, Tuple, Union, cast


def patch_plotly_show() -> None:
    """Patch the :func:`plotly.io.show()` function to skip any rendering steps and,
    instead, simply call :func:`plotly.io._utils.validate_coerce_fig_to_dict()`."""
    from typing import Union

    import plotly.io
    from plotly.graph_objs import Figure
    from plotly.io._utils import validate_coerce_fig_to_dict  # noqa

    def wrapped(
        fig: Union[Figure, dict],
        renderer: Optional[str] = None,
        validate: bool = True,
        **kwargs: Dict[str, Any],
    ) -> None:
        validate_coerce_fig_to_dict(fig, validate)

    plotly.io.show = wrapped


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
    import importlib.util
    import sys

    path_posix = Path(path).resolve().as_posix()
    module_name = path_posix.split("/")[-1].split(".")[0]
    spec = cast(
        ModuleSpec,
        importlib.util.spec_from_file_location(
            name=module_name,
            location=path_posix,
        ),
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def import_attrs_from_pyscript(path: Union[str, Path], *attributes: str) -> Tuple[Any, ...]:
    """Import attributes from a Python script.

    Parameters
    ----------
    path
        The path to the Python file to import.
    *attributes : tuple[str]
        The attributes to import from the module.

    Returns
    -------
    Tuple[Any, ...]
        The imported attributes.

    Examples
    --------
    So, instead of doing:

        >>> from path.to.script import Foo, bar

    You can instead do:

        >>> Foo, bar = import_attrs_from_pyscript("path/to/script.py", "Foo", "bar")
    """
    module = import_pyscript_as_module(path)
    return tuple(getattr(module, attr) for attr in attributes)
