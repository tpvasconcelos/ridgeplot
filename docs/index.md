---
title: beautiful ridgeline plots in Python
---

:::{div} centered
# ridgeplot: beautiful ridgeline plots in Python

[![PyPI - Latest Release](https://img.shields.io/pypi/v/ridgeplot)](https://pypi.org/project/ridgeplot/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/ridgeplot)](https://pypi.org/project/ridgeplot/)
[![Pepy Total Downloads](https://img.shields.io/pepy/dt/ridgeplot)](https://pepy.tech/project/ridgeplot)
[![PyPI - Package Status](https://img.shields.io/pypi/status/ridgeplot.svg)](https://pypi.org/project/ridgeplot/)
[![PyPI - License](https://img.shields.io/pypi/l/ridgeplot)](https://github.com/tpvasconcelos/ridgeplot/blob/main/LICENSE)

[![GitHub CI](https://github.com/tpvasconcelos/ridgeplot/actions/workflows/ci.yml/badge.svg)](https://github.com/tpvasconcelos/ridgeplot/actions/workflows/ci.yml/)
[![CodeQL](https://github.com/tpvasconcelos/ridgeplot/actions/workflows/codeql.yml/badge.svg)](https://github.com/tpvasconcelos/ridgeplot/actions/workflows/codeql.yml/)
[![Docs](https://readthedocs.org/projects/ridgeplot/badge/?version=latest&style=flat)](https://ridgeplot.readthedocs.io/en/latest/)
[![codecov](https://codecov.io/gh/tpvasconcelos/ridgeplot/branch/main/graph/badge.svg)](https://codecov.io/gh/tpvasconcelos/ridgeplot)
[![CodeFactor](https://www.codefactor.io/repository/github/tpvasconcelos/ridgeplot/badge)](https://www.codefactor.io/repository/github/tpvasconcelos/ridgeplot)
[![Codacy code quality Badge](https://app.codacy.com/project/badge/Grade/e21652ac49874b6f94ed3c9b7ac77021)](https://app.codacy.com/gh/tpvasconcelos/ridgeplot/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
:::

-----------------

`ridgeplot` is a Python package that provides a simple interface for plotting beautiful and interactive [ridgeline plots](getting_started/getting_started.md) within the extensive [Plotly](https://plotly.com/python/) ecosystem.

![ridgeplot - beautiful ridgeline plots in Python](_static/img/hero.png){align=center w=800px}

<h2>Installation</h2>

`ridgeplot` can be installed and updated from [PyPi](https://pypi.org/project/ridgeplot/) using [pip](https://pip.pypa.io/en/stable/quickstart/):

```shell
pip install -U ridgeplot
```

For more information, see the [installation guide](getting_started/installation).

<h2>Getting started</h2>

Take a look at the [getting started guide](getting_started/getting_started), which provides a quick introduction to the `ridgeplot` library.

<h3>Basic example</h3>

For those in a hurry, here's a very basic example on how to quickly get started with the {py:func}`~ridgeplot.ridgeplot()` function.

```python
import numpy as np
from ridgeplot import ridgeplot

my_samples = [np.random.normal(n / 1.2, size=600) for n in range(8, 0, -1)]
fig = ridgeplot(samples=my_samples)
fig.update_layout(height=450, width=800)
fig.show()
```

```{raw} html
:file: _static/charts/basic.html
```

```{toctree}
---
caption: Getting started
maxdepth: 1
glob: true
hidden: true
---
getting_started/installation
getting_started/getting_started
```

```{toctree}
---
caption: Reference
maxdepth: 1
glob: true
hidden: true
---
api/index.rst
reference/*
```

```{toctree}
---
caption: Development
maxdepth: 1
glob: true
hidden: true
---
development/*
```
