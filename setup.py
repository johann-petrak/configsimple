#!/usr/bin/env python
# encoding: utf-8

"""Packaging script for the configsimple library."""

import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    readme = f.read()


def versionfromfile(*filepath):
    here = os.path.abspath(os.path.dirname(__file__))
    infile = os.path.join(here, *filepath)
    with open(infile) as fp:
        version_match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]",
                                  fp.read(), re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string in {}.".format(infile))


setup(
    name="configsimple",
    version=versionfromfile("configsimple/__init__.py"),
    author="Johann Petrak",
    author_email="johann.petrak@gmail.com",
    description='Configure components/classes using config files, command line options etc in a simple way',
    long_description=readme,
    long_description_content_type='text/markdown',
    setup_requires=["pytest-runner"],
    install_requires=[],
    python_requires=">=3.5",
    tests_require=['pytest'],
    platforms='any',
    license="MIT",
    keywords="",
    url="http://github.com/johann-petrak/configsimple",
    packages=find_packages(),
    test_suite='tests',
    classifiers=[
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Intended Audience :: Developers",
      ],
)
