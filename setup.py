"""Setup script for the mazegen package.

This script configures the maze generation package for installation
using setuptools. It enables the package to be installed via pip
or built into a distributable wheel.

Usage:
    pip install .
    python setup.py bdist_wheel
"""

from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="1.0.0",
    python_requires=">=3",
    packages=find_packages()
)
