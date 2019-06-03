#!/usr/bin/env python
# encoding: utf-8

"""Packaging script for the simpleconfig library."""

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.md')).read()

setup(
    name="simpleconfig",
    version="0.1",
    author="Johann Petrak",
    author_email="johann.petrak@gmail.com",
    description='Configure components/classes using config files, command line options etc in a simple way',
    long_description=readme,
    long_description_content_type="text/markdown",
    setup_requires=[],
    install_requires=[],
    python_requires=">=3.5",
    license="MIT",
    keywords="",
    url="http://github.com/johann-petrak/simpleconfig",
    py_modules=['simpleconfig'],
    packages=find_packages(),
    # test_suite='tests',
    # tests_require=['mock'],
    classifiers=["Development Status :: 5 - Production/Stable",
                 "License :: OSI Approved :: MIT License",
                 "Natural Language :: English",
                 "Programming Language :: Python :: 3",
                 "Topic :: Software Development",
                 "Intended Audience :: Developers",
                ],
)
