#!/usr/bin/env python
# -*- coding:utf-8 -*-

import io
from distutils.core import setup

version = '0.1.0'

setup(
    name='python-control4',
    version=version,
    description='Python bindings for Control4 API',
    keywords='control4',
    author='Aleksi Asikainen',
    author_email='aleksi.asikainen@gmail.com',
    url='https://github.com/r3pi/python-control4',
    packages=['control4',],
    install_requires=['requests>=1.0.0',],
    entry_points={
      'console_scripts': ['control4=control4.command_line:main']
    },
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=io.open('README.txt', encoding='UTF-8').read(),
)
