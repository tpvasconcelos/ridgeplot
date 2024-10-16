from __future__ import annotations

import pytest

from ridgeplot.datasets import _DATA_DIR, load_probly


def test_data_dir_contains_data_files() -> None:
    allowed_extensions = (".csv",)
    all_files = list(_DATA_DIR.iterdir())
    assert len(all_files) > 0
    for file in all_files:
        assert file.is_file()
        assert file.name.endswith(allowed_extensions)


def test_data_dir_not_empty() -> None:
    assert len(list(_DATA_DIR.iterdir())) > 0


def test_load_probly() -> None:
    # zonination's version should be the default
    df_default = load_probly()
    df_zonination = load_probly(version="zonination")
    assert df_default.shape == df_zonination.shape == (46, 17)
    df_wadefagen = load_probly(version="wadefagen")
    assert df_wadefagen.shape == (123, 20)
    df_illinois = load_probly(version="illinois")
    assert df_illinois.shape == (75, 17)
    with pytest.raises(ValueError, match="Unknown version"):
        load_probly(version="nonexistent")  # type: ignore[arg-type]
