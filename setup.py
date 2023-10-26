#!/usr/bin/env python
import os

from Cython.Build import cythonize
from setuptools import setup


def get_n_processes() -> int:
    """Return a reasonable value for cythonize's nthreads parameter."""
    cpu_count = os.cpu_count()
    if cpu_count in (None, 0, 1, 2):
        return 0
    return cpu_count - 1



if __name__ == "__main__":
    setup(
        ext_modules=cythonize(
            module_list=["src/ridgeplot/_missing.pyx"],
            nthreads=get_n_processes(),
            show_all_warnings=True,
        )
    )
