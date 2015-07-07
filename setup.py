#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from pip.req import parse_requirements

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as fh:
    readme = fh.read()

requirements = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'))
install_requires = [str(req.req) for req in requirements]

setup(
    name='django-debian',
    version='0.1',
    description='Reference Django app for Debian packaging',
    long_description=readme,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
