from __future__ import annotations

import pickle
from importlib import reload
from typing import Any

import pytest

from cicd.test_helpers import round_trip_pickle


def test_repr() -> None:
    from ridgeplot._missing import MISSING

    assert repr(MISSING) == "<MISSING>"


def test_pickle_round_trip() -> None:
    from ridgeplot._missing import MISSING

    for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
        assert round_trip_pickle(MISSING, protocol=proto) is MISSING


def assert_all_are(*args: Any) -> None:
    """Assert that all arguments are the same object."""
    assert len(args) > 1
    for i in range(len(args) - 1):
        a = args[i]
        b = args[i + 1]
        if a is not b:
            raise AssertionError(
                f"{a!r} and {b!r} (i={i}) are not the same object (id: {id(a)} != {id(b)})"
            )


@pytest.mark.xfail(
    reason="Reloading ridgeplot._missing is currently not allowed.",
    raises=RuntimeError,
)
def test_reloading() -> None:
    import ridgeplot
    import ridgeplot._missing as types_module
    from ridgeplot._missing import MISSING

    missing1 = ridgeplot._missing.MISSING
    missing2 = types_module.MISSING
    missing3 = MISSING

    assert_all_are(missing1, missing2, missing3)

    reload(ridgeplot)
    assert_all_are(
        missing1,
        missing2,
        missing3,
        ridgeplot._missing.MISSING,
        types_module.MISSING,
        MISSING,
    )

    reload(types_module)
    assert_all_are(
        missing1,
        missing2,
        missing3,
        ridgeplot._missing.MISSING,
        types_module.MISSING,
        MISSING,
    )
