from __future__ import annotations

from typing import Any

import pytest

from cicd.test_helpers import round_trip_pickle


@pytest.mark.parametrize(
    "obj",
    [
        None,
        True,
        0,
        1.0,
        "foo",
        [None, True, 0, {"foo": "bar"}],
        {"foo": "bar", False: (1, 2, 3)},
    ],
)
def test_round_trip_pickle(obj: Any) -> None:
    assert round_trip_pickle(obj) == obj
