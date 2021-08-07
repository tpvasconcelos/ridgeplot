from pathlib import Path
from runpy import run_module


def run_module_as_main(module: str) -> None:
    run_module(mod_name=module, run_name="__main__")


def test_example_scripts() -> None:
    path_examples_package = Path(__file__).parents[2].joinpath("examples")
    for py_module in path_examples_package.glob("*.py"):
        run_module_as_main(module=f"{path_examples_package.name}.{py_module.stem}")
