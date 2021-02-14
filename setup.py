#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PyEPLAN module."""

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
import os

def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = ['pandas','pyomo']

from pyeplan import __version__, __author__, __email__, __status__, __url__, __name__

setup(
    name=__name__,
    version=__version__,
    description='Python library for planning and operation of resilient microgrids.',
    author=__author__,
    author_email=__email__,
    url=__url__,
    keywords=['Operation', 'Planning', 'Microgrids'],
    license='Apache License 2.0',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=install_requires, 
    classifiers=[
        "Development Status :: " + __status__,
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3"
    ]
)
