"""Plotly figure template utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from _plotly_utils.basevalidators import BaseTemplateValidator

if TYPE_CHECKING:
    import plotly.graph_objects as go

    from ridgeplot._types import PlotlyTemplate


def validate_coerce_template(template: PlotlyTemplate | None) -> go.layout.Template | None:
    """Convert mixed template representations into a
    :class:`plotly.graph_objects.layout.Template
    <plotly.graph_objs.layout.Template>` object.

    ``None`` is passed through as-is, meaning that no template has been
    specified and that Plotly's current default template should be used.
    """
    if template is None:
        return None
    validator = BaseTemplateValidator(
        plotly_name="template",
        parent_name="layout",
        data_class_str="Template",
        data_docs="",
    )
    return cast("go.layout.Template", validator.validate_coerce(template))
