from __future__ import annotations

import json
from pathlib import Path

import pytest

from ridgeplot_examples import ALL_EXAMPLES, Example


@pytest.mark.parametrize("example", ALL_EXAMPLES)
def test_examples_width_height_set(example: Example) -> None:
    msg = "Both `width` and `height` should be set in all example plots."
    assert isinstance(example.fig.layout.width, int), msg
    assert isinstance(example.fig.layout.height, int), msg


PATH_ARTIFACTS = Path(__file__).parent / "artifacts"


@pytest.mark.parametrize("example", ALL_EXAMPLES)
def test_regressions(example: Example) -> None:
    """Verify that the rendered JPEG images match the current artifacts."""
    expected = (PATH_ARTIFACTS / f"{example.plot_id}.json").read_text()
    assert example.fig.to_dict() == json.loads(expected)


def _update_all_artifacts() -> None:
    """Update the artifacts for all examples.

    This function is intended to be run manually when the examples
    have been updated and the artifacts need to be refreshed.

    To update the artifacts, run:

        $ PYTHONPATH='cicd_utils/' python ./tests/e2e/test_examples.py

    """
    for example in ALL_EXAMPLES:
        # Save JSONs for regression tests
        example.to_json(PATH_ARTIFACTS)
        # We also save JPEGs for visual inspection (e.g., in PRs)
        # (Don't use JPEGs for regression tests because outputs
        #  will vary between Plotly versions and platforms)
        example.to_jpeg(PATH_ARTIFACTS)


if __name__ == "__main__":
    _update_all_artifacts()
