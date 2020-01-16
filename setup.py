######!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Xavier Robert <xavier.robert@ird.fr>
# SPDX-License-Identifier: GPL-3.0-or-later


from setuptools import setup, find_packages

# import the library
#from pytro2th import tro2th
import pytro2th

def readme():
	with open('README.rst') as f:
		return f.read()

setup(name='pytherion',
	version=pytro2th.__version__,
	description='Module that provides tools for manage data transformations for the software Therion',
	long_descritpion=open('README.rst').read(),
	#url='http://github.com/robertxa/pytro2th',
	#dowload_url='https://github.com/robertxa/pytro2th/archive/master.zip',
	author='Xavier Robert',
	author_email='xavier.Robert@univ-grenoble-alpes.fr',
	license='GPL-V3.0',
	packages=find_packages(),
	#packages=['pytro2th'],
	#scripts=['bin/tro2therion'],
	#install_requires=[
	#      'os',
	#      'numpy',
	#      'sys'
	#],
	#classifiers=[
	#	"Programming language :: Python",
	#	"Operating System :: OS Independent",
	#	"Topic :: Caving",
	#],
	include_package_data=True,
	zip_safe=False)
      