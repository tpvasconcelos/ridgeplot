from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if sys.version_info >= (3, 10):
    from importlib.resources import files
else:
    from importlib_resources import files

if TYPE_CHECKING:
    from typing import Literal

import pandas as pd

__all__ = [
    "load_probly",
    "load_lincoln_weather",
]


_DATA_DIR = files("ridgeplot.datasets.data")


def load_probly(
    version: Literal["zonination", "wadefagen", "illinois"] = "zonination",
) -> pd.DataFrame:
    """Load a version of the "Perception of Probability Words"
    (a.k.a., *"probly"*) dataset.

    Parameters
    ----------
    version : {'zonination', 'wadefagen', 'illinois'}, default: 'zonination'
        The version of the dataset to load. Each version is slightly different
        and originates from different surveys. See the `Notes`_ section for
        more details on each version.

    Returns
    -------
    :class:`pandas.DataFrame`
        A dataframe containing a *probly* dataset.

    Notes
    -----
    .. _Notes:

    Sherman Kent, a CIA analyst, first published his work on the perception of
    probabilistic words in 1964 [1]_. This exercise has been repeated several
    times since then. This function provides three different versions of the
    dataset, each originating from a different survey. Valid options for the
    ``version`` parameter are:

    ``"zonination"``
        This is perhaps the most popular version of the dataset and originates
        from a survey conducted by the Reddit user `/u/zonination`_.

        .. collapse:: <i>Dataset details...</i>

            .. list-table::
               :stub-columns: 1
               :align: left

               * - Creator
                 - :gh-user:`zonination`
               * - Source
                 - https://raw.githubusercontent.com/zonination/perceptions/51207062aa173777264d3acce0131e1e2456d966/probly.csv
               * - Accessed on
                 - 2023-06-24

    ``"wadefagen"``
        This version of the dataset originates from a blogpost by Wade
        Fagen-Ulmschneider from the University of Illinois [2]_. It is based on
        a survey conducted on different social media platforms.

        .. collapse:: <i>Dataset details...</i>

            .. list-table::
               :stub-columns: 1
               :align: left

               * - Creator
                 - Wade Fagen-Ulmschneider (:gh-user:`wadefagen`)
               * - Source
                 - https://raw.githubusercontent.com/wadefagen/datasets/7e752937b72edc3126e3dd17e3cd97eb727af8f9/Perception-of-Probability-Words/survey-results.csv
               * - Accessed on
                 - 2023-06-24

    ``"illinois"``
        This version of the dataset originates from a survey of primarily
        undergraduate students conducted at The University of
        Illinois [3]_.

        .. collapse:: <i>Dataset details...</i>

            .. list-table::
               :stub-columns: 1
               :align: left

               * - Creator
                 - University of Illinois
               * - Source
                 - https://waf.cs.illinois.edu/discovery/words.csv
               * - Accessed on
                 - 2023-06-24

    References
    ----------
    .. [1] Sherman Kent. (1964). *"Words of estimative probability"*.
       https://www.cia.gov/static/Words-of-Estimative-Probability.pdf
    .. [2] Wade Fagen-Ulmschneider. *"Perception of Probability Words"*.
       https://waf.cs.illinois.edu/visualizations/Perception-of-Probability-Words/
    .. [3] University of Illinois. *"Perception of Probability Words Dataset"*.
       https://discovery.cs.illinois.edu/dataset/words/
    .. _/u/zonination: https://www.reddit.com/user/zonination

    """
    versions = {
        "zonination": "probly-zonination.csv",
        "wadefagen": "probly-wadefagen.csv",
        "illinois": "probly-illinois.csv",
    }
    if version not in versions:
        raise ValueError(
            f"Unknown version {version!r} for the probly dataset. "
            f"Valid versions are {list(versions.keys())}."
        )
    return pd.read_csv(_DATA_DIR / versions[version])


def load_lincoln_weather() -> pd.DataFrame:
    """Load the "Weather in Lincoln, Nebraska in 2016" dataset.

    Returns
    -------
    :class:`pandas.DataFrame`
        A dataframe containing the "Lincoln Weather" dataset.

    Notes
    -----
    The version of the dataset included in this package is the same
    version included in the `ggridges` R package [1]_. The dataset
    contains weather information from Lincoln, Nebraska (2016).
    The original data was taken from a blogpost by Austin Wehrwein
    in 2017 [2]_.

    .. collapse:: <i>Details...</i>

        .. list-table::
           :stub-columns: 1
           :align: left

           * - Source
             - https://raw.githubusercontent.com/wilkelab/ggridges/543a092c601b92d7b62e630fb34d038f54485a29/data-raw/lincoln-weather.csv
           * - Accessed on
             - 2023-08-07

    References
    ----------
    .. [1] ggridges. *"Weather in Lincoln, Nebraska in 2016"*.
       https://wilkelab.org/ggridges/reference/lincoln_weather.html
    .. [2] Austin Wehrwein. *"Plot inspiration via FiveThirtyEight"*.
       https://austinwehrwein.com/data-visualization/plot-inspiration-via-fivethirtyeight/

    """
    data = pd.read_csv(_DATA_DIR / "lincoln-weather.csv", index_col="CST")
    data.index = pd.to_datetime(data.index.to_list())
    return data
