from __future__ import annotations

from typing import Any, Dict, Optional, Union


def patch_plotly_show() -> None:
    """Patch the :func:`plotly.io.show()` function to skip any rendering steps and,
    instead, simply call :func:`plotly.io._utils.validate_coerce_fig_to_dict()`."""
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
