from __future__ import annotations

from _compile_plotly_charts import PATH_DOCS


def test_path_docs_exists() -> None:
    assert PATH_DOCS.exists()
    assert PATH_DOCS.is_dir()
    assert PATH_DOCS.name == "docs"
