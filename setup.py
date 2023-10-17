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

required = ['pandas', 'pyomo', 'networkx', 'mplleaflet', 'matplotlib==3.3.0', 'timezonefinder', 'scikit-learn==1.0.0', 'openpyxl', 'ipython']

setup(
    name='pyeplan',
    packages=find_packages(),
    version='0.4.6',
    description='Python library for planning and operation of resilient microgrids.',
    author="Shahab Dehghan",
    author_email="s.dehghan@ieee.org",
    url="https://github.com/SPS-L/pyeplan",
    keywords=['Operation', 'Planning', 'Microgrids'],
    license='Apache License 2.0',
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    install_requires=required, 
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3"
    ]
)
