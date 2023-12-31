#!/usr/bin/env python
from __future__ import annotations

# isort: split
from utils import get_py_version, get_sys_platform, run_subprocess


def main() -> None:
    py_version = get_py_version()
    sys_platform = get_sys_platform()
    test_req = f"requirements/locked/{py_version}-{sys_platform}.txt"
    run_subprocess(["pip", "install", "-r", test_req])


if __name__ == "__main__":
    main()
