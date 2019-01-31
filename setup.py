import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
)

#!/usr/bin/env python

from setuptools import setup

setup(
    setup_requires=['pbr>=1.9', 'setuptools>=17.1'],
    pbr=True,
)
