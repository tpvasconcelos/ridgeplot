"""A collection of miscellaneous functional tests."""

from __future__ import annotations

from ridgeplot import ridgeplot


def test_color_discrete_map_eq_colormode_hack() -> None:
    """Test that using an "*index*" colormode is a hack that produces the
    same result as using the new `color_discrete_map` argument."""
    red = "rgba(255, 0, 0, 1)"
    blue = "rgba(0, 0, 255, 1)"
    fig1 = ridgeplot(
        samples=[[[1, 2, 3], [4, 5, 6]]],
        color_discrete_map={"A": blue, "B": red},
        labels=["A", "B"],
    )
    fig2 = ridgeplot(
        samples=[[[1, 2, 3], [4, 5, 6]]],
        colorscale=[red, blue],
        colormode="trace-index-row-wise",
        labels=["A", "B"],
    )
    fig3 = ridgeplot(
        samples=[[[1, 2, 3], [4, 5, 6]]],
        colorscale=[red, blue],
        colormode="trace-index",
        labels=["A", "B"],
    )
    assert fig1 == fig2 == fig3
