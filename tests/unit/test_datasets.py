from ridgeplot.datasets import _DATA_DIR, load_probly


def test_data_dir_exists() -> None:
    assert _DATA_DIR.exists()


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
