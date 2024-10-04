from __future__ import annotations

import os
from pathlib import Path

import pytest

PATH_CICD_SCRIPTS = Path(__file__).parents[3] / "cicd_utils/cicd/scripts"
CICD_SCRIPTS = [
    p
    for p in PATH_CICD_SCRIPTS.iterdir()
    if p.is_file() and p.suffix in {".py"} and p.name != "__init__.py"
]


def test_cicd_scripts_not_empty() -> None:
    assert len(CICD_SCRIPTS) > 0


@pytest.mark.parametrize("script_path", CICD_SCRIPTS, ids=[p.name for p in CICD_SCRIPTS])
def test_scripts_are_executable(script_path: Path) -> None:
    assert os.access(script_path, os.X_OK)


@pytest.mark.parametrize("script_path", CICD_SCRIPTS, ids=[p.name for p in CICD_SCRIPTS])
def test_scripts_have_py_shebang(script_path: Path) -> None:
    with script_path.open("r") as f:
        first_line = f.readline()
    assert first_line.startswith("#!/usr/bin/env python")
