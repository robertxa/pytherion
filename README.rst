pytro2th
========

This module is designed for cavers who need to convert cave's surveys from the Visual Topo software 
to the Therion software. It provides functions to read Visual Topo files (*.tro) and to write Therion files
(*.th, *.thconfig and config.thc)

WARNINGS
--------

This code crashes because of a problem of encoding reading when used with Visual Topo files which contain accentuated characters !!!
For the moment, I did not manage to solve that problem...

Install
-------

To install it :
	pip install pytherion

Usage
-----

Inside a (i)python environnement:

To import the module:
	>>> from pytro2th import tro2th
	
To create only a generic thconfig file with a config file:
    >>> tro2th()

To convert a cave.tro file:
	>>> tro2th(fle_tro_fnme = 'cave.tro')

To build only a thonfig file, in english, without any comments and without extended elevation layout
	>>> tro2th(thlang = 'en', cavename = 'Test', icomments = False, icoupe = False, ithconfig = False, thconfigfnme = None, ithc = False, thcpath = my/path/to/my/confg/file, thcfnme = 'config.thc', sourcefiles = ['Test.th', 'Test.th2'], xviscale = 1000, xvigrid = 10, scale = 500,Errorfiles = True)

Options/inputs
--------------

To use options or inputs, you need to set them as
	
	tro2th(option_name = option_value, [...])
	
Options/inputs are (option_names):
	1. fle_tro_fnme : (string) Path and name of the .tro file to convert. 
			          if None (value by default), the function does not convert anything 
			          but build .thconfig and config.thc files
			          If the path is not given, the function will look in the folder from where it is launched
	2. fle_th_fnme  : (string) Path and name of the .th file to create from the .tro file. 
			          If None (value by default), this file is created from the .tro file name 
			          and in the same folder than that .tro file
	3. thlang       : (string) String that set the language. 'fr' by default. 
			          If you need english, change 'fr' to 'en' in the function definition
			          set 'fr' for french
			          set 'en' for english
			          ... other languages are not implemented
	4. cavename     : (string) Name of the cave. 
			          If set to None (default value), it is get from the .tro file.
	5. icomments    : (Boolean) To add (True, by default) or not (False) comments in the produced files
	6. icoupe       : (Boolean) To set (True, by default) or not (False) an extended-elevation layout in the .thconfig file
	7. ithconfig    : (Boolean) To set if the thconfig file is created (True, by default) or not 
	8. thconfigfnme : (string) Path and name of the thconfig file. 
			          If None (by default), path and name build from the .tro file
	9. ithc         : (Boolean) To build (True, by default) or not (False) a config file config.thc 
	10. thcpath     : (string) Path to the directry that contains the config file called in the cave.thconfig file.
			          If used with ithc = False, this path is only used for the declaration 
			          in the cave.thconfig
			          If used with ithc = True, the config file will be written in that directory.
			          Set to None by default
	11. thcfnme     : (string) Name of the config.thc (value by default if set to None or if ommitted)
	12. sourcefile  : (list of strings) Define the source files declared in the cave.thconfig
					  ex :['example.th', 'example.th2', 'example-coupe.th2']
					  If None or ommitted, it is build from the .tro file or the cavename
	13. xviscale    : (Real) Scale of the xvi file. 
			          Set to 1000 by default that corresponds to 1/1000 
	14. xvigrid     : (Real) Spacing of the grid for the xvi, in meters. 
			          Set 10 by default
	15. scale       : (Real) scale of the map
			          Set to 500 by default that corresponds to 1/500 	
	16. Errorfiles  : (Boolean) If True (by default), an error will be raised if output files exists in the folder
			          If False, only a warning is raised, and the previous files are erased by the new ones.
			          Use with caution

Help files
----------

To get help in your (i)python environnement:
	>>> help(tro2th)
			
Outputs
-------

Depending of the input parameters, several files can be produced:
	
	1. cavename.th       : survey data for Therion
	2. cavename.thconfig : file to build the pdf's maps and others
	3. config.thc        : config file for the .thconfig file.

How to cite
-----------

.. image:: https://zenodo.org/badge/159739189.svg
  :target: https://zenodo.org/doi/10.5281/zenodo.10020982


Licence
-------

Copyright (c) 2020 Xavier Robert <xavier.robert@ird.fr>
SPDX-License-Identifier: GPL-3.0-or-later
