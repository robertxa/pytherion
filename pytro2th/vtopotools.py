######!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf8

# Copyright (c) 2020 Xavier Robert <xavier.robert@ird.fr>
# SPDX-License-Identifier: GPL-3.0-or-later


"""
	Functions to work on vtopo data to be able to write them in the Therion format
	By Xavier Robert
	Lima, 2016.06.21
	
	USAGE :
	  - They are normally used by other scripts
	
	
	INPUTS:
		The inputs are in the script file, in the "# Define data to analysis" section. 
		The different arguments are described.
		
"""

###### To DO :  #######
#    - Take in account the 'I' (extended elevation) inverse option in vtopo file --> set extend right/left
###### End To DO #######

from __future__ import  division
# This to be sure that the result of the division of integers is a real, not an integer
#from __future__ import unicode_literals

# Import modules
import sys
import os
import numpy as np

def read_vtopo_header(lines):
	"""
		Function to read header from vtopofile
		
		INPUTS:
			lines: file .tro read by the fonction lines = readlines(file_vtopo)
		
		OUTPUTS (all are strings):
			cavename    : Name of the cave
			coordinates : Entrance coordinates
			coordsyst   : Coordinates system to set the entrance coordinates
			club        : Name of the group that explored the cave
			entrance    : Entrance of the cave
			versionfle  : Vtopo version that has been used to produce the vtopofile
		
		USAGE:
			cavename, coordinates, coordsyst, club, entrance, versionfle = read_vtopo_header(lines)
				
		Author: Xavier Robert, Lima 2016/06/27
		
		Licence: CCby-nc
	"""
	
	# coord_dict: French Lambert system. To find number of your system, see extern/proj4/nad/epsg 
	#             file in the therion source distribution. You can add your own lines/systems
	coord_dict = {u'LT1' : u'EPSG:27571',
	             u'LT2' : u'EPSG:27572',
	             u'LT3' : u'EPSG:27573',
	             u'LT4' : u'EPSG:27574'
	             }
	for line in lines:
		if u"Version" in line:
			versionfle = line[1].replace(u'\n', u'').rstrip(u'\n\r').split(' ')
		if u'Trou' in line:
			# read Trou
	 		(cavename, xcoord, ycoord, alt, coordtro) = line[5:].replace(u'\n', u'').rstrip(u'\n\r').split(u',')
			coordinates = [xcoord, ycoord, alt]
		# read club
		if u'Club' in line: club = line[5:].replace(u'\n', u'')
		# read entrance name
		if u'Entree' in line : entrance = line[7:].replace(u'\n', u'')
	
	if coordtro[:3] in coord_dict:
		# Rewrite the coordinate system to be read by Therion
		# French Lambert system. To find number of your system, see extern/proj4/nad/epsg file in the therion source distribution. You can add you own lines/systems
		coordsyst = coord_dict[coordtro[0:3]]
	else:
		coordsyst = None
	
	return cavename, coordinates, coordsyst, club, entrance, versionfle

	
def read_settings(line):
	"""
		Function to read the line that define the settings of the survey session : 
		  intruments, directions, units, calibrations,...
		
		INPUTS:
			line     : string extractd from the .tro file that contains the information on the survey session
			
		OUTPUTS:
			settings : list of strings with all the measurments settings
			comments : string that correspond to the end of the string "Line" 
			           that do not correspond to the settings
		USAGE:
			settings, comments = read_settings(line)
			          
		Author: Xavier Robert, Lima 2016/06/27
		
		Licence: CCby-nc
	"""
	# Question: Do we have to update the code in function of the vtopo version number?
	param = line[6:].rstrip(u'\n\r').split(u' ')
	k = 8
	#k = 6
	if 'Topof' in param[:k]:
		k = k + 1
	if 'Prof' in param[:k] or 'Deniv' in param[:k]: 
		k = k - 1
	settings = param[:k]
	#commentst = param[k+2:]
	commentst = param[k:]
	comments = " ".join(str(elem)  for elem in commentst)
	
	#ucomments=comments.decode('us-ascii', errors = 'replace')
	#print ucomments
		 
	return settings, comments#.encode('utf-8', errors = "replace")


def read_data(lines, settings, j, iline):
	"""
		Function to read the data from the line
		
		INPUTS:
			lines    : file .tro read by the fonction lines = readlines(file_vtopo)
			settings : list of strings with all the measurments settings;
			           output of the function read_settings
			j        : number of the line that corresponds to the settings line in the list "lines"
			iline    : list of line numbers that correspond to the different settings line in the list "lines"
		
		OUTPUTS:
			data     : list of lists of data (string format)

		USAGE:
			data = read_data(lines, settings, j, iline)
				
		Author: Xavier Robert, Lima 2016/06/27
		
		Licence: CCby-nc
	"""
	
	data = []
	# check if we are at the end of the iline file or not !
	if iline.index(j) < len(iline)-1:
		for i in range(j+1, iline[iline.index(j)+1]):
 			datal = [x for x in lines[i].replace(u'\n', u'').rstrip(u'\n\r').split(u' ') if x != u'']
 			data.append(datal)
	else:
		i = j+1
		while 1:
 			if 'Configuration' in lines[i]:
 				break
 			else:
 				datal = [x for x in lines[i].replace(u'\n', u'').rstrip('\n\r').split(u' ') if x != u'']
	 			data.append(datal)
 				i+=1
	# remove white lines in datao
	data = [x for x in data if x != []]
	
	return data


def convert_text(lines):
	"""
		Fonction to convert characters encoding...
		The problem is that .tro files are encode with strange Windows settings, 
		and the accentuation is not well understood by other systems
		
		Bug, that is not working well
		
		INPUTS:
			lines :
		OUTPUTS:
			
		
		USAGE:
			lines = convert_text(lines)
			
		Author: Xavier Robert, Lima 2016/06/27
		
		Licence: CCby-nc
	"""
	dictcaract ={'\xe8' : u'è',
	             '\xe0' : u'à',
	             '\xe9' : u'é',
	             '\xe0' : u'à',
	             '\xf9' : u'ù',
	             '\xea' : u'ê',
	             '\xeb' : u'ë',
	             '\xf1' : u'ñ',
	             '\xfb' : u'û',
	             '\xee' : u'î',
	             '\xef' : u'ï'}
	
	#for line in lines:
	for line in lines.decode('cp1252'):
		# windows = latin-1 ? cp-1252 ? cp1252 ? mbcs ?
		for elem in dictcaract:
			#print line
			if elem in line:
				line = line.replace(elem, dictcaract[elem])
			
	return lines

	
if __name__ == u"__main__":
	
	from datathwritetools import writeheader_th, writecenterlineheader, writedata
	
	fle_tro_fnme = u'Test.tro'
	fle_th_fnme = u'test.th'
	icomments = True
	thlang = u'fr'
	
	# open tro file
	fle_tro = open(fle_tro_fnme, u'rU')
	# open new th file
	fle_th =  open(fle_th_fnme, u'w')
	
	# read the tro file
	lines = fle_tro.readlines()
	
	lines = convert_text(lines)
	
	# read the header
	#cavename, coordinates, coordtro, club, entrance = read_vtopo_header(fle_tro)
	cavename, coordinates, coordsyst, club, entrance, versionfle = read_vtopo_header(lines)
	
	writeheader_th(fle_th, cavename, entrance)
	
	# read line to line and find the Param
	i = 0
	iline = []
	dataold = []
	
	# get line numbers of the lines beginning with 'Param'
	for line in lines:
		#print i
		#print i, line.replace('\n', '')
		if u'Param' in line: iline.append(i)
		i+=1
	
	for j in iline:
		# read the settings of the survey
		settings, comments = read_settings(lines[j].replace(u'\n', u''))
		data = read_data(lines, settings, j, iline)
		
		# write centerline header
		writecenterlineheader(fle_th, entrance, settings, comments, data, coordsyst, coordinates, club,
		                      icomments, thlang)
		# write the data to the .th file
		writedata(fle_th, settings, data, dataold)
		
		fle_th.write(u'\n\tendcenterline\n')
		dataold = data	
	
	
	fle_th.write(u'\nendsurvey\n')
	
	fle_tro.close
	fle_th.close

