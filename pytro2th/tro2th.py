######!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Copyright (c) 2020 Xavier Robert <xavier.robert@ird.fr>
# SPDX-License-Identifier: GPL-3.0-or-later


"""
	!---------------------------------------------------------!
	!                                                         !
	!                    Tro to Therion                       !
	!                                                         !
	!           Code to transform the .tro files              !
	!            Visual Topo into files that can              !
	!                  be used by Therion                     !
	!                                                         !
	!              Written by Xavier Robert                   !
	!                                                         !
	!---------------------------------------------------------!

	 ENGLISH :
	 This code is to transform the .tro file from Visualtopo (http://vtopo.free.fr/)
	 into files that can be read by Therion (http://therion.speleo.sk/).
	 It reads .tro file and produce one .th file (file with survey data),
	 and one thconfig file (file that is used to compile and build the survey with Therion).
	 
	 TODOS : - Correct the errors in encodings... This is the most important....
	         - Check all the situations possibles...
	         - Add title to the centerline !
"""
# Do divisions with Reals, not with integers
# Must be at the beginning of the file
from __future__ import division
#from __future__ import unicode_literals
import sys, os

# Import Python modules
#modulesNames = ['sys', 'warnings']
#for module in modulesNames:
#	try:
#		# because we want to import using a variable, do it this way
#		module_obj = __import__(module)
#		# create a global object containging our module
#		globals()[module] = module_obj
#	except ImportError:
#		sys.exit("ERROR : Module " + module + " not present. \n\n Please, install it \
#			      \n\n Edit the source code for more information")

from buildparam import *
from vtopotools import *
from datathwritetools import *
from buildthconfig import *


def tro2th(fle_tro_fnme = None, fle_th_fnme = None, 
			thlang = u'fr',
			cavename = None, 
			icomments = True, icoupe = True, 
			ithconfig = True, thconfigfnme = None, 
			ithc = True, thcpath = None, thcfnme = u'config.thc', 
			sourcefile = None, xviscale = 1000, xvigrid = 10, scale = 500,
			Errorfiles = True):
	
	"""
		Main function to convert tro to th files. 
		This is this function that should be called from python.
	
		INPUTS:
			fle_tro_fnme : (string) Path and name of the .tro file to convert. 
			               if None (value by default), the function does not convert anything 
			               but build .thconfig and config.thc files
			               If the path is not given, the function will look in the folder from where it is launched
			fle_th_fnme  : (string) Path and name of the .th file to create from the .tro file. 
			               If None (value by default), this file is created from the .tro file name 
			               and in the same folder than that .tro file
			thlang       : (string) String that set the language. 'fr' by default. 
			               If you need english, change 'fr' to 'en' in the function definition
			              set 'fr' for french
			              set 'en' for english
			              ... other languages are not implemented
			cavename     : (string) Name of the cave. 
			               If set to None (default value), it is get from the .tro file.
			icomments    : (Boolean) To add (True, by default) or not (False) comments in the produced files
			icoupe       : (Boolean) To set (True, by default) or not (False) an extended-elevation layout in the .thconfig file
			ithconfig    : (Boolean) To set if the thconfig file is created (True, by default) or not 
			thconfigfnme : (string) Path and name of the thconfig file. 
			               If None (by default), path and name build from the .tro file
			ithc         : (Boolean) To build (True, by default) or not (False) a config file config.thc 
			thcpath      : (string) Path to the directry that contains the config file called in the cave.thconfig file.
			                If used with ithc = False, this path is only used for the declaration 
			                in the cave.thconfig
			                If used with ithc = True, the config file will be written in that directory.
			                Set to None by default
			thcfnme      : (string) Name of the config.thc (value by default if set to None or if ommitted)
			sourcefile   : (list of strings) Define the source files declared in the cave.thconfig
							ex :['example.th', 'example.th2', 'example-coupe.th2']
							If None or ommitted, it is build from the .tro file or the cavename
			xviscale     : (Real) Scale of the xvi file. 
			                Set to 1000 by default that corresponds to 1/1000 
			xvigrid      : (Real) Spacing of the grid for the xvi, in meters. 
			               Set 10 by default
			scale        : (Real) scale of the map
			               Set to 500 by default that corresponds to 1/500 	
			Errorfiles   : (Boolean) If True (by default), an error will be raised if output files exists in the folder
			               If False, only a warning is raised, and the previous files are erased by the new ones.
			               Use with caution
			
		OUTPUTS:
			Depending of the parameters inputed, several files can be produced
			cavename.th       : survey data for Therion
			cavename.thconfig : file to build the pdf's maps and others
			confgi.thc        : config file for the .thconfig file.
			
		USAGE:
			To build everything
			tro2th(fle_tro_fnme = 'Test', fle_th_fnme = 'Test', 
			       thlang = 'fr',
			       cavename = 'Test', 
			       icomments = True, icoupe = True, 
			       ithconfig = True, thconfigfnme = None, 
			       ithc = True, thcpath = None, thcfnme = 'config.thc', 
			       sourcefiles = None, xviscale = 1000, xvigrid = 10, scale = 500,
			       Errorfiles = True)
			
			To build only a .th file
			tro2th(fle_tro_fnme = 'Test', fle_th_fnme = 'Test', 
			       thlang = 'fr',
			       cavename = 'Test', 
			       icomments = True, icoupe = True, 
			       ithconfig = False
			       ithc = False
			       Errorfiles = True)
			
			To build only a thonfig file, in english, without any comments and without extended elevation layout
			tro2th(thlang = 'en',
			       cavename = 'Test', 
			       icomments = False, icoupe = False, 
			       ithconfig = False, thconfigfnme = None, 
			       ithc = False, thcpath = my/path/to/my/confg/file, thcfnme = 'config.thc', 
			       sourcefiles = ['Test.th', 'Test.th2'], xviscale = 1000, xvigrid = 10, scale = 500,
			       Errorfiles = True)
		
		Author: Xavier Robert, Lima 2016/06/27
		
		Licence: CCby-nc
	"""
	
	if thlang in [u'fr', u'FR', u'Fr', u'fR']: thlang = u'fr'
	elif thlang in [u'en',u'EN', u'En', u'eN']: thlang = u'en'
	else: raise NameError(u'ERROR: Language %s not implemented\n'
	                      u'       Use "en" instead' % thlang )
	print(u'____________________________________________________________\n\n\t\tTRO 2 THERION\n____________________________________________________________\n')
	if thlang == u'fr':
		print(u'\nEcrit par Xavier Robert, Groupe spéléo Vulcain - Lyon, France\n')
	elif thlang == u'en':
		print(u'\nWritten by Xavier Robert, Groupe spéléo Vulcain - Lyon, France\n')
	print(u'____________________________________________________________\n\n')
	
	coordsyst = None		
	if fle_tro_fnme is not None:
		if fle_tro_fnme[-4:] != u'.tro':
			fle_tro_fnme = fle_tro_fnme + u'.tro'
		# check if file exists
		if os.path.isfile(fle_tro_fnme) == False :
			if thlang == u'fr': raise NameError(u'ERROR : Le fichier {FileNa} n\'existe pas'.format(FileNa=str(fle_tro_fnme)))
			elif thlang == u'en': raise NameError(u'ERROR : File {FileNa} does not exist'.format(FileNa=str(fle_tro_fnme)))
		
		if fle_th_fnme is None:
			# convert tro file to th file
			cavename, coordsyst, fle_th_fnme = convert_tro(fle_tro_fnme, 
			                                              icomments = icomments, icoupe = icoupe, 
			                                              thlang = thlang, Errorfiles = Errorfiles)
		else:
			cavename, coordsyst, fle_th_fnme = convert_tro(fle_tro_fnme, fle_th_fnme, cavename,
			                                               icomments = icomments, icoupe = icoupe, 
			                                               thlang = thlang, Errorfiles = Errorfiles)
		
		if thlang == u'fr': print(u'\tFichier Therion %s construit à partir des données %s' %(fle_th_fnme, fle_tro_fnme))
		elif thlang == u'en': print(u'\tFile %s built from %s' %(fle_th_fnme, fle_tro_fnme))
	else:
		if thlang == u'fr': print(u'\tPas de fichier .tro en entrée, pas de fichier .th créé...')
		elif thlang == u'en': print(u'\tNo .tro File input, no .th file created...')

	if sourcefile is None:
		if fle_th_fnme is None:
			if cavename is None: cavename = u'cave'
			sourcefile = [cavename.replace(u' ', u'_') + u'.th', 
			              u'#' + cavename.replace(u' ', u'_') + u'.th2', 
			              u'#' + cavename.replace(u' ', u'_') + u'-coupe.th2']
		else:
			sourcefile = [fle_th_fnme, u'#' + fle_th_fnme[0:-4] + u'th2', u'#' + fle_th_fnme[0:-4] + u'-coupe.th2' ]
	# Build the dictionnary for the thconfig file	
	dictcave = [sourcefile, xviscale, xvigrid, cavename, coordsyst, scale]

	# build thc file
	if ithc :
		if  thcpath is not None :
			writethc(thcpath + thcfnme)
		else:
			writethc(thcfnme)
	
	# build thconfig file
	if ithconfig :
		# write the file
		if thconfigfnme is None or thconfigfnme == u'':
			if fle_th_fnme is None:	thconfigfnme = cavename.replace(u' ', u'_') + u'.thconfig'
			else: thconfigfnme = fle_th_fnme[0:-3] + u'.thconfig'
		
		if thcpath is not None:
			thcfnme = thcpath + thcfnme
		writethconfig(thconfigfnme, icomments, icoupe, thlang,
			              dictcave,
		                  ithc, thcfnme)
	print(u'____________________________________________________________')
	print(u'')
	
	return
	

	
def convert_tro(fle_tro_fnme, fle_th_fnme = None, cavename = None, 
                icomments = True, icoupe = True, thlang = u'fr', Errorfiles = True):	
	"""
		Function that manages the tro 2 th conversion
		
		INPUTS:
			fle_tro_fnme : path and file name of the .tro file to convert
			fle_th_fnme  : path and file name of the .th file to create. 
			               If ommitted, set to None, and this varaible will be set in function of the fle_tro_fnme or cavename
			cavename     : Name of the cave. If ommitted, it is set to None, and it is get from the .tro file 
        	Errorfiles   : True (by default if ommitted) to get an error if the .th file already exists.
	                       False if only a warning...
		OUTPUTS:
			new .th file with surveyed data for Therion
			cavename      : Name of the cave from the .tro file
			coordsyst     : Coordinates system used by the .tro file
			
		USAGE:
			cavename, coordsyst = convert_tro(fle_tro_fnme, [fle_th_fnme = fle_th_fnme, cavename = cavename, Errorfiles = Errorfiles])
			          fle_th_fnme, cavename and Errorfiles can be ommitted.
		
		Author: Xavier Robert, Lima 2016/06/27
		
		Licence: CCby-nc
	"""
	
	#from codecs import open
		
	# Initialization of some variables...
	#xcoord=0.
	#ycoord=0.
	#alt=0.
	
	# open the .tro survey	
	if thlang == u'fr': print(u'\tTravail sur %s' % fle_tro_fnme)
	elif thlang == u'en':print(u'\tProcessing %s' % fle_tro_fnme)
	print(' ')
	fle_tro = open(fle_tro_fnme, 'rU')
	# read the .tro file
	lines = fle_tro.readlines()
	# change the encoding
	lines = convert_text(lines)
	
	# read the header
	cavename, coordinates, coordsyst, club, entrance, versionfle = read_vtopo_header(lines)
	
	if cavename is None or cavename == '' or cavename == ' ':
		cavename = u'cave'
	
	if fle_th_fnme is None:
		fle_th_fnme = cavename.replace(u' ', u'_') + u'.th'
		print (fle_th_fnme)
	if fle_th_fnme[-3:] != u'.th':
		fle_th_fnme = fle_th_fnme + u'.th'	
	
	# check if file exists... 
	checkfiles(fle_th_fnme, Errorfiles)
	# open the .th file

	fle_th = open (fle_th_fnme, 'w')
	# write the .th header
	writeheader_th(fle_th, cavename, entrance)
	
	# initiate variables
	i = 0
	iline = []
	dataold = []
	
	# get line numbers of the lines beginning with 'Param'
	for line in lines:
		if u'Param' in line: iline.append(i)
		i+=1
	
	for j in iline:
		# read the settings of the survey
		settings, comments = read_settings(lines[j].replace(u'\n', u''))
		
		# read the data from the tro file
		data = read_data(lines, settings, j, iline)
		
		# write centerline header
		writecenterlineheader(fle_th, entrance, settings, comments, data, coordsyst, coordinates, club,
		                      icomments, thlang)

		# write the data to the .th file
		writedata(fle_th, settings, data, dataold)
		
		# write the end of the centerline in the .th file
		fle_th.write(u'\n\tendcenterline\n\n')
		dataold = data	
	# write the end of the survey in the .th file
	fle_th.write(u'\nendsurvey\n')
	fle_th.close
	
	print fle_th_fnme
	
	if thlang == u'fr': print (u'\tFichier %s écrit !' % fle_th_fnme)
	elif thlang == u'en': print (u'\tFile %s written!' % fle_th_fnme)
	
	return cavename, coordsyst, fle_th_fnme


if __name__ == u'__main__':
	
	
	# initiate variables
	
	# run the transformation  
	tro2th()
