from __future__ import annotations

import contextlib
import pickle
import sys
from importlib.abc import Loader
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar, cast

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import ModuleType

    from plotly.graph_objs import Figure


@contextlib.contextmanager
def patch_plotly_show() -> Iterator[None]:
    """Patch the :func:`plotly.io.show()` function to skip any rendering steps
    and, instead, simply call
    :func:`plotly.io._utils.validate_coerce_fig_to_dict()`.
    """
    from unittest.mock import MagicMock, patch

    from plotly.io._utils import validate_coerce_fig_to_dict

    def patched(
        fig: Figure | dict[str, Any],
        renderer: str | None = None,  # noqa: ARG001
        validate: bool = True,
        **kwargs: Any,  # noqa: ARG001
    ) -> None:
        validate_coerce_fig_to_dict(fig, validate)

    with patch("plotly.io.show", MagicMock(side_effect=patched)):
        yield


_T = TypeVar("_T", bound=Any)


def round_trip_pickle(obj: _T, protocol: int = pickle.HIGHEST_PROTOCOL) -> _T:
    """Round-trip an object through pickle.

    Parameters
    ----------
    obj
        The object to round-trip through pickle.
    protocol
        The pickle protocol to use. If not specified, the highest protocol
        available will be used.

    Returns
    -------
    The object that was pickled and unpickled.

    """
    return cast(_T, pickle.loads(pickle.dumps(obj, protocol=protocol)))  # noqa: S301


def import_pyscript_as_module(path: str | Path) -> ModuleType:
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


def import_attrs_from_pyscript(path: str | Path, *attributes: str) -> tuple[Any, ...]:
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

    >>> from path.to.script import Foo, bar  # doctest: +SKIP

    You can instead do:

    >>> Foo, bar = import_attrs_from_pyscript("path/to/script.py", "Foo", "bar")  # doctest: +SKIP

    """
    module = import_pyscript_as_module(path)
    return tuple(getattr(module, attr) for attr in attributes)
