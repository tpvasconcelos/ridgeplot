from __future__ import annotations

import pytest

from ridgeplot_examples import ALL_EXAMPLES
from ridgeplot_examples._base import _round_sig_figs  # pyright: ignore[reportPrivateUsage]


def test_all_examples() -> None:
    assert len(ALL_EXAMPLES) > 2


@pytest.mark.parametrize(
    ("sig", "x", "expected"),
    [
        (2, 0.123456, 0.12),
        (3, 0.123456, 0.123),
        (4, 0.123456, 0.1235),
        (5, 0.123456, 0.12346),
    ],
)
def test_round_sig_figs(sig: int, x: float, expected: float) -> None:
    assert _round_sig_figs(x, sig) == expected
