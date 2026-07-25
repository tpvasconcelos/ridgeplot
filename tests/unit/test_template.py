from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import pytest

from ridgeplot._template import validate_coerce_template


def test_none_passthrough() -> None:
    assert validate_coerce_template(None) is None


def test_registered_template_name() -> None:
    assert validate_coerce_template("plotly_dark") == pio.templates["plotly_dark"]


# Merging templates causes Plotly to internally instantiate all
# registered trace types, including the deprecated Scattermapbox
@pytest.mark.filterwarnings(r"ignore:\*scattermapbox\* is deprecated.*:DeprecationWarning")
def test_merged_template_names() -> None:
    assert validate_coerce_template("plotly_white+ggplot2") == pio.templates["plotly_white+ggplot2"]


def test_template_object() -> None:
    template = pio.templates["seaborn"]
    assert validate_coerce_template(template) == template


def test_template_dict() -> None:
    template = pio.templates["seaborn"]
    coerced = validate_coerce_template(template.to_plotly_json())
    assert isinstance(coerced, go.layout.Template)
    assert coerced == template


def test_invalid_template_name() -> None:
    with pytest.raises(ValueError, match=r"Invalid value .* received for the 'template' property"):
        validate_coerce_template("this-is-not-a-registered-template")


def test_invalid_template_type() -> None:
    with pytest.raises(ValueError, match=r"Invalid value .* received for the 'template' property"):
        validate_coerce_template(42)  # pyright: ignore[reportArgumentType]
