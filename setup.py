#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import fixerio_for_pdr

NAME = "fixerio_for_pdr"


def readme():
    with open("README.md") as f:
        return f.read()


install_requires = []
with open("./requirements.txt") as f:
    install_requires = f.read().splitlines()
with open("./requirements-dev.txt") as f:
    tests_require = f.read().splitlines()

setup(
    name=NAME,
    version=fixerio_for_pdr.__version__,
    description="This package allows the pandas_datareader to use the fixer api"
    "to request historical forex rates for a specific day and range of currencies.",
    long_description=readme(),
    license="Apache-2.0",
    author="Mark J. Rees",
    author_email="mark@jmmjsolutions.com",
    url="https://github.com/jmmjsolutions/fixerio_for_pdr",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    keywords="data",
    install_requires=install_requires,
    packages=find_packages(exclude=["docs", "tests*"]),
    test_suite="tests",
    tests_require=tests_require,
    zip_safe=False,
    python_requires=">=3.6",
)