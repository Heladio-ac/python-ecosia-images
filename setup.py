#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = "0.3.1"

setup(name='ecosia_images',
    version=__version__,
    description='Python scripts for searching and downloading pictures from Ecosia',
    author='Heladio Amaya',
    author_email='heladio.ac@gmail.com',
    url="https://github.com/Heladio-ac/python-ecosia-images",
    packages=['ecosia_images']
)