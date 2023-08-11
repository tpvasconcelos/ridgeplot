from pathlib import Path
from runpy import run_path

import pytest

ROOT_DIR = Path(__file__).parents[2]
assert ROOT_DIR.name == "ridgeplot"
PATH_EXAMPLES = ROOT_DIR / "docs/_examples"


@pytest.mark.parametrize("example_script", PATH_EXAMPLES.glob("*.py"))
def test_example_scripts(example_script: Path) -> None:
    """Assert that the example scripts run with no errors."""
    assert example_script.exists()
    # TODO: check against expected output
    run_path(example_script.as_posix(), run_name="__main__")
