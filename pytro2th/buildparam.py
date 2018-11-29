######!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to build Therion files
By Xavier Robert
Lima, 2016.06.21

USAGE :
  1- Run in the terminal: $ python buildthconfig.py


INPUTS:
The inputs are in the script file, in the "# Define data to analysis" section. 
The different arguments are described.

xavier.robert@ujf-grenoble.fr

(c) licence CCby-nc : http://creativecommons.org/licenses/by-nc/3.0/ 2015

"""

###### To DO :  #######
#   -   
###### End To DO #######

from __future__ import  division
# This to be sure that the result of the division of integers is a real, not an integer

# Import modules
import sys
import os
import copy
import numpy as np

########################

def builddictcave():
	"""
	
	"""
	
	########################
	#    Define parameters
	
	# thlang: language to set in the files, can be english [en] or french [fr]
	thlang = 'fr'
	# thcfile: set to True to build a config file, or False if not
	thcfile = True
	# thcfnme: name of the thc file
	thcfnme = 'config.thc'
	# thcpath: path where to add the config file.
	#          if None, it will be in the folder from where is run the code
	thcpath = None
	# thconfigfile: set to True to build a thconfig file, or False if not
	thconfigfile = True
	# thconfigpath: path where to add the thconfig file.
	#               if None, it will be in the folder from where is run the code
	thconfigpath = None
	# thconfigfnme: name of the thconfig file
	thconfigfnme= 'Test.thconfig'
	#icomments: True if we add comments inside the thconfig file,
	#          False if there is no comments inside the thconfig file
	icomments = True
	#icoupe: True if we want a layout for extended projection in the thconfig
	#       False if not
	icoupe = True
	
	# Errfiles: True to write on previous files; be careful in that case !!
	#           False if not
	Errfiles = True


	# sourcefiles: source files
	sourcefile = ['example.th', 'example.th2', 'example-coupe.th2']
	# xviscale: scale of the xvi file
	#           1000 corresponds to 1/1000
	xviscale = 1000
	# xvigrid: spacing of the grid for the xvi, in meters
	xvigrid = 10
	# cavefnme: cave fnme
	cavefnme = 'Example'
	# coord: coordinate system
	#        Can be set to None
	coord = None
	# scale: scale of the map
	#        500 corresponds to 1/500
	scale = 500 
	
	
	data = [thlang, thcfile, thcfnme, thcpath, 
	        thconfigfile, thconfigpath, thconfigfnme, 
	        icomments, icoupe, Errfiles]
	dictcave = [sourcefile, xviscale, xvigrid, cavefnme, coord, scale]
	
	return dictcave, data
