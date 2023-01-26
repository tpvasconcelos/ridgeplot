__all__ = ["load_probly"]

from pathlib import Path

import pandas as pd

_DATA_DIR = Path(__file__).parent / "data"


def load_probly() -> pd.DataFrame:
    """Load the `probly dataset`_.

    .. _probly dataset:
        https://github.com/zonination/perceptions/blob/
        51207062aa173777264d3acce0131e1e2456d966/probly.csv
    """
    data = pd.read_csv(_DATA_DIR / "probly.csv")
    return data
