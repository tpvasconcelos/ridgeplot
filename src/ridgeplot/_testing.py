from __future__ import annotations

import pickle
from typing import TYPE_CHECKING, Any, TypeVar, cast

if TYPE_CHECKING:
    from typing import Optional, Union

    from plotly.graph_objs import Figure


def patch_plotly_show() -> None:
    """Patch the :func:`plotly.io.show()` function to skip any rendering steps and,
    instead, simply call :func:`plotly.io._utils.validate_coerce_fig_to_dict()`."""
    import plotly.io
    from plotly.io._utils import validate_coerce_fig_to_dict

    def wrapped(
        fig: Union[Figure, dict[str, Any]],
        renderer: Optional[str] = None,
        validate: bool = True,
        **kwargs: Any,
    ) -> None:
        validate_coerce_fig_to_dict(fig, validate)

    plotly.io.show = wrapped


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
