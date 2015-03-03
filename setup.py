#!/usr/bin/env python
# coding=utf-8

import os
from distutils.core import setup

delattr(os, 'link')

setup(
    name='python-cmdline',
    version='1.0',
    author='Jérôme Belleman',
    author_email='Jerome.Belleman@gmail.com',
    url='http://cern.ch/jbl',
    description='"Cmdline module"',
    long_description='"Cmdline module wrapped around cmd."',
    data_files=[('share/man/man1', ['python-cmdline.1'])],
    py_modules=['cmdline'],
)
