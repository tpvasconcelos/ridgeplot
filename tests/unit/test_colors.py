from ridgeplot._colors import PLOTLY_COLORSCALES, validate_colorscale
from ridgeplot._utils import LazyMapping


def test_plotly_colorscales() -> None:
    assert isinstance(PLOTLY_COLORSCALES, LazyMapping)
    for name, colorscale in PLOTLY_COLORSCALES.items():
        assert isinstance(name, str)
        validate_colorscale(colorscale=colorscale)
