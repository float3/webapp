#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="trolley",
    version="1.0",
    # Modules to import from other scripts:
    packages=find_packages(),
    # Executables
    scripts=["app.py"],
)
