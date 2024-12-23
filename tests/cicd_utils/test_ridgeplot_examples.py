from __future__ import annotations

import pytest

from ridgeplot_examples import ALL_EXAMPLES
from ridgeplot_examples._base import (
    round_fig_data,
    round_nested_seq,
    round_seq,
    round_sig_figs,
)


def test_all_examples() -> None:
    assert len(ALL_EXAMPLES) > 2


@pytest.mark.parametrize(
    ("sig", "x", "expected"),
    [
        (5, 0.123456, 0.12346),
        (12, 0.123456, 0.123456),
        (3, 1234, 1230),
        (1, 123e-3, 0.1),
    ],
)
def test_round_sig_figs(sig: int, x: float, expected: float) -> None:
    assert round_sig_figs(x, sig) == expected


def test_round_seq() -> None:
    assert round_seq([123456, 123.456, 0.123456], 5) == [123460, 123.46, 0.12346]


def test_round_nested_seq() -> None:
    assert round_nested_seq([[123456], [123.456]], 5) == [[123460], [123.46]]


def test_round_fig_data() -> None:
    import plotly.graph_objects as go

    fig = go.Figure(
        data=[
            go.Scatter(
                x=[123456, 123.456, 0.123456],
                y=[123456, 123.456, 0.123456],
                customdata=[[123456], [123.456], [0.123456]],
            )
        ]
    )
    fig_rounded = round_fig_data(fig, 5)
    assert fig_rounded.data[0].x == (123460, 123.46, 0.12346)
    assert fig_rounded.data[0].y == (123460, 123.46, 0.12346)
    assert fig_rounded.data[0].customdata == ([123460], [123.46], [0.12346])
