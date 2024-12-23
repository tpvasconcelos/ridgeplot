from __future__ import annotations

import pytest

from ridgeplot_examples import ALL_EXAMPLES
from ridgeplot_examples._base import _round_sig_figs  # pyright: ignore[reportPrivateUsage]


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
    assert _round_sig_figs(x, sig) == expected
