from __future__ import annotations

import re

import pytest

V_EXPECTED = "0.1.30"


def get_number(v_component: str) -> int:
    return int("".join(c for c in v_component if c.isdigit()))


def assert_dev_version_is_valid(v_base: str, v_dev: str) -> None:
    assert "dev" in v_dev

    base_info = tuple(v_base.split("."))
    dev_info = tuple(v_dev.split("."))

    assert base_info[:-1] == dev_info[: len(base_info) - 1]

    assert dev_info[-1].startswith("dev")
    assert dev_info[-1].removeprefix("dev").isdigit()

    assert get_number(dev_info[-2]) == get_number(base_info[-1]) + 1


@pytest.mark.parametrize(
    ("v_base", "v_dev", "valid"),
    [
        ("1.2.3", "1.2.3", False),
        ("1.2.3", "1.2.4", False),
        ("1.2.3", "1.2.3.dev0", False),
        ("1.2.3", "1.2.4.dev0", True),
        ("1.2.3.rc1", "1.2.3.rc1", False),
        ("1.2.3.rc1", "1.2.3.rc2", False),
        ("1.2.3.rc1", "1.2.3.rc1.dev0", False),
        ("1.2.3.rc1", "1.2.3.rc2.dev0", True),
    ],
)
def test_dev_version_is_valid(v_base: str, v_dev: str, valid: bool) -> None:
    if valid:
        assert_dev_version_is_valid(v_base, v_dev)
    else:
        with pytest.raises(AssertionError):
            assert_dev_version_is_valid(v_base, v_dev)


def test_version() -> None:
    from ridgeplot import __version__ as v_public
    from ridgeplot._version import __version__ as v_private

    assert v_public is v_private

    # Should at least contain major.minor.patch
    assert re.match(r"^\d+\.\d+\.\d", v_public)

    if "dev" in v_public:  # pragma: no cover
        assert_dev_version_is_valid(v_base=V_EXPECTED, v_dev=v_public)
    else:  # pragma: no cover
        assert v_public == V_EXPECTED
