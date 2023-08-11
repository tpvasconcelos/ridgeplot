# Installation

## Installing from PyPi

`ridgeplot` can be installed and updated from [PyPi](https://pypi.org/project/ridgeplot/) using [pip](https://pip.pypa.io/en/stable/quickstart/):

```shell
pip install -U ridgeplot
```

## Installing from source

The source code for this project is hosted on GitHub at: <https://github.com/tpvasconcelos/ridgeplot>

Take a look at the [contributing guide](/development/contributing) for instructions on how to build from the git source. Further, refer to the instructions on [creating a development environment](Development-environment) if you wish to create a local development environment, or wish to contribute to the project.

## Dependencies

We try to keep the number of dependencies to a minimum and only use common and well-established libraries in the scientific python ecosystem. Currently, we only depend on the following 3 Python packages:

- [plotly](https://plotly.com/) - The interactive graphing backend that powers `ridgeplot`
- [statsmodels](https://www.statsmodels.org/) - Used for Kernel Density Estimation (KDE)
- [numpy](https://numpy.org/) - Supporting library for multidimensional array manipulations
