from __future__ import annotations

import json
from pathlib import Path

import pytest

from ridgeplot_examples import ALL_EXAMPLES, Example

PATH_ROOT = Path(__file__).parents[2].resolve()
PATH_ARTIFACTS = PATH_ROOT / "tests/e2e/artifacts"
PATH_CHARTS = PATH_ROOT / "docs/_static/charts"


def test_paths_exist() -> None:
    assert PATH_ROOT.name == "ridgeplot"
    assert PATH_ARTIFACTS.is_dir()
    assert PATH_CHARTS.is_dir()


@pytest.mark.parametrize("example", ALL_EXAMPLES, ids=lambda e: e.plot_id)
def test_examples_width_height_set(example: Example) -> None:
    msg = "Both `width` and `height` should be set in all example plots."
    assert isinstance(example.fig.layout.width, int), msg
    assert isinstance(example.fig.layout.height, int), msg


@pytest.mark.parametrize("example", ALL_EXAMPLES, ids=lambda e: e.plot_id)
def test_json_regressions(example: Example) -> None:
    expected = (PATH_ARTIFACTS / f"{example.plot_id}.json").read_text()
    assert json.loads(example.to_json()) == json.loads(expected)


def _update_all_artifacts() -> None:
    """Update the artifacts for all examples.

    This function is intended to be run manually when the examples
    have been updated and the artifacts need to be refreshed.

    To update the artifacts, run:

        $ PYTHONPATH='cicd_utils/' python ./tests/e2e/test_examples.py

    """
    for example in ALL_EXAMPLES:
        print(f"Updating artifacts for: {example.plot_id!r}")  # noqa: T201
        # Save JSONs for regression tests
        example.write_json(PATH_ARTIFACTS)
        # We also save JPEGs for visual inspection (e.g., in PRs)
        # (Don't use JPEGs for regression tests because outputs
        #  will vary between Plotly versions and platforms)
        example.write_jpeg(PATH_ARTIFACTS)
        # Just to keep things in sync with the docs, we should also
        # regenerate the WebP images used there. These are tracked
        # by Git because some are used in the README (which needs
        # to be rendered on GitHub), otherwise they would be in
        # the .gitignore file (like the HTML artifacts).
        example.write_webp(PATH_CHARTS)


if __name__ == "__main__":
    _update_all_artifacts()
