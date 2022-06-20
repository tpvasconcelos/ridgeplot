from pathlib import Path
from runpy import run_path

import pytest

PATH_EXAMPLES = Path(__file__).parents[2].joinpath("examples")


@pytest.mark.parametrize("example_script", PATH_EXAMPLES.glob("*.py"))
def test_example_scripts(example_script: Path) -> None:
    """Assert that the example scripts run with no errors."""
    assert example_script.exists()
    run_path(example_script.as_posix(), run_name="__main__")
