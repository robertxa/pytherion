######!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Xavier Robert <xavier.robert@ird.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

import importlib.util
from setuptools import setup


spec = importlib.util.spec_from_file_location(
    "pytro2th._version",
    "pytro2th/_version.py",
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
VERSION = module.__version__

def readme():
	with open('README.rst') as f:
		return f.read()

setup(name='pytherion',
	version=VERSION,
	description='Module that provides tools for manage data transformations for the software Therion',
	long_descritpion=open('README.rst').read(),
	#url='http://github.com/robertxa/pytro2th',
	#dowload_url='https://github.com/robertxa/pytro2th/archive/master.zip',
	author='Xavier Robert',
	author_email='xavier.Robert@univ-grenoble-alpes.fr',
	license='GPL-V3.0',
    entry_points={
        "console_scripts": [
            "pytro2th=pytro2th.command_line:main",
        ],
    },
	packages=['pytro2th'],
	#scripts=['bin/tro2therion'],
	install_requires=[
        'wget',
        'pyproj'
	],
	#classifiers=[
	#	"Programming language :: Python",
	#	"Operating System :: OS Independent",
	#	"Topic :: Caving",
	#],
	include_package_data=True,
	zip_safe=False)
      