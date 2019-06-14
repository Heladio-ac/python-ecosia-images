#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
import os
import io

__version__ = '0.4.10'

here = os.path.abspath(os.path.dirname(__file__))

DESCRIPTION = 'Python module for searching and downloading images from Ecosia'

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

REQUIRED = [
    'selenium',
    'requests'
]

setup(name='ecosia_images',
    version=__version__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Heladio Amaya',
    author_email='heladio.ac@gmail.com',
    url='https://github.com/Heladio-ac/python-ecosia-images',
    packages=['ecosia_images'],
    install_requires=REQUIRED
)