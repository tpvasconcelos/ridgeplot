from __future__ import annotations

from ridgeplot._color.css_colors import CSS_NAMED_COLORS


def test_css_named_colors() -> None:
    assert len(CSS_NAMED_COLORS) == 147
    assert "black" in CSS_NAMED_COLORS
    assert "white" in CSS_NAMED_COLORS
