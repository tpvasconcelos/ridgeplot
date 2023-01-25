from ridgeplot.datasets import _DATA_DIR, load_probly


def test_data_dir_exists() -> None:
    assert _DATA_DIR.exists()


def test_data_dir_not_empty() -> None:
    assert len(list(_DATA_DIR.iterdir())) > 0


def test_load_probly() -> None:
    data = load_probly()
    assert len(data) > 0
