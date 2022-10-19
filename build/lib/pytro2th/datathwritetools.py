######!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf8

# Copyright (c) 2020 Xavier Robert <xavier.robert@ird.fr>
# SPDX-License-Identifier: GPL-3.0-or-later


"""
Script to build Therion files
By Xavier Robert
Lima, 2016.06.21

USAGE :
  1- Run in the terminal: $ python buildthconfig.py


INPUTS:
The inputs are in the script file, in the "# Define data to analysis" section. 
The different arguments are described.

"""

###### To DO :  #######
#    - Test the MTL pdfs (I have not tested it, even if it should be OK)
#    - Add error bars on data graphs ? 
#      For that we should read the input data file given in topo_parameters.txt 
#                    (paragraphe N°12 of topo_parameters.txt)
#      
###### End To DO #######

from __future__ import  division
# This to be sure that the result of the division of integers is a real, not an integer
#from __future__ import unicode_literals

# Import modules
import sys, os, copy, datetime
import numpy as np
from pyproj import Proj, transform


def writeheader_th(file, cavename, entrance):
	"""
	Function to write the header of the file.th
	
	INPUTS:
	   file     : variable that sets the file.th
	   cavename : name of the cave
	   entrance : name of the entrance station
	   
	OUTPUTS:
		None
		
	USAGE:
		writeheader_th(file, cavename, entrance)
		
	Author: Xavier Robert, Lima 2016/06/27
	
	"""
	
	file.write(u'encoding utf-8 \n\nsurvey %s -title "%s" -entrance "%s" \n'
	           %(cavename.replace(u' ', u'_'), cavename, entrance))
	
	return


def writecenterlineheader(file, entrance, settings, comments, data, coordsyst, coordinates, club,
                          icomments, thlang):
	"""
	Function to write the centerline header
	
	
	INPUTS:
		file        : variable that sets the file.th
		entrance    : name of the entrance station
		settings    : List of the settings of this survey section
		comments    : String that correspond to the end of the string "Line" 
		              that do not correspond to the settings
		data        : data from this survey section
		coordsyst   : Coordinates system to set the entrance coordinates
		coordinates : Entrance coordinates
		club        : Name of the group that explored the cave
		icomments   : True if comments in the file
		              False if not
		thlang      : 'fr' for french
		              'en' for english
		              ... other languages not implemented
	   
	OUTPUTS:
		None
		
	USAGE:
		writeheader_th(file, cavename, entrance)
		
	Author: Xavier Robert, Lima 2016/06/27
	
	"""
	# First, define dictionaries to help the coding
	# angleU: define the angle unit
	angleU = {u'Deg' : u'degrees',
	          u'Degd' :u'degrees',
	          u'Gra' : u'grad'}
	# compassdir:
	dir = {u'Dir' : u'',
	       u'Inv' : u'back'}
	# lruddir: Set the LRUD
	lruddir = {u'Dir' : u'left right up down',
	           u'Inv' : u'right left up down',
	           u'Nod' : u''}
	# unitcounter: set the unit of the counter (for the length)
	unitcounter = {u'Vulc' : u'centi',
	               u'Prof' : u'',
	               u'Deniv': u''}
	# unitclino: used to correct the clino if topoVulcain
	unitclino = {u'Deg'  : u'90',
	             u'Degd' : u'90',
	             u'Gra'  : u'100'}
	# typelen: type of length measures
	#typelem = {u'Deca' : u'normal',
	#          u'Topof' : u'topofil',
	#          u'Vulc' : u'topofil',
	#          u'Prof' : u'diving',
	#          u'Deniv' : u'deniv'}
	# style: data style
	style = {u'Deca'   : u'normal',
	         u'Topof'  : u'topofil',
	         u'Diving' : u'diving',
	         u'Prof'   : u'diving',
	         u'Carth'  : u'carthesian',
	         u'Cylp'   : u'cylpolar',
	         u'Dim'    : u'dimensions',
	         u'Nosy'   : u'nosurvey'} 
	# station: type of stations
	station = {u'station' : u'station',
	           u'from'    : u'from',
	           u'to'      : u'to',
	           u'vtopo'   : u'from to'}
	# lensurv: how are set the length measurements
	lensurv = {u'Deca'   : u'length',
	           u'Topof'  : u'fromcount tocount',
	           u'Diving' : u'length',
	           u'Prof'   : u'length'}
	# slopesurv: how are set the slope measurements
	slopesurv = {u'Clino' : u'clino',
	             u'Vulc'  : u'clino',
	             u'Deniv' : u'depthchange',
	             u'Prof'  : u'depth'}	
    
    # Begin the centerline
	file.write(u'\n\tcenterline \n')
	
	# if entrance in the data, write the entrance coordinates
	if [datal for datal in data if entrance in datal] != []:
		if icomments:
			if thlang == u'fr':
				file.write(u'\t\t# Si le systeme de coordonnées n\'est pas le système' 
				           u' Lambert français, voir le Thbook et le fichier' 
			    	       u' extern/proj4/nad/epsg dans le dossier source de Therion \n')
				file.write(u'\t\t# Si les coordonnées de l\'entrée sont connues,' 
				           u' copier dans la centerline correspondante et décommenter' 
				           u' les 2 lignes suivantes : \n')
			elif thlang == u'en':
				file.write('u\t\t# If your are not in the french Lambert system, ' 
				           u' To find number of your system, see' 
				           u' extern/proj4/nad/epsg file in the Therion' 
			    	       u' source distribution \n')
				file.write(u'\t\t# If the entrance coordinates are known, uncomment and' 
				           u' copy in the corresponding centerline the next 2 lines: \n')
		if coordsyst != None:
			file.write(u'\t\tcs %s \n' 
		               u'\t\tfix %s %s %s %s \n\n' % (coordsyst, entrance, coordinates[0], coordinates[0], coordinates[0])) 
		else:
			file.write(u'\t\t#cs %s \n' 
		               u'\t\t#fix %s %s %s %s \n\n' % (coordsyst, entrance, coordinates[0], coordinates[0], coordinates[0])) 
	typem = u'Deca'
	if u'Topof' not in settings:
		settings [1:1]= u' '
		typem = u'Topof'
	if u'Prof' in settings or u'Deniv' in settings:
		settings[4:4] = u' '
	# next line used to debug
	#file.write(u'\t' + str(settings) + u'\n')
	# write the survey caracteristics
	file.write(u'\t\t#date YYYY.MM.DD \n')
	if icomments:
			if thlang == u'fr':
				file.write(u'\t\t# Si date est utilisé, commenter la ligne "declination", '
				           u'la date sera utilisée pour la calculer\n')
			elif thlang == u'en':
				file.write(u'\t\t# If date is used, comment the ligne "declination", '
				           u'the date will be use to compute it\n')
	file.write(u'\t\tdeclination %s %s \n'% (str(settings[-2]), angleU[settings[2]]))
	file.write(u'\t\t\tteam "G.S. Vulcain" \n')
	file.write(u'\t\t\tteam "%s" \n' % club)
	file.write(u'\t\t#explo-date YYYY.MM.DD \n')
	file.write(u'\t\t\texplo-team "G.S. Vulcain" \n')
	file.write(u'\t\t\texplo-team "%s" \n' % club)
	if icomments:
		if thlang == u'en': file.write(u'\t\t# (to be completed, add many lines as you need) \n')
		elif thlang == u'fr': file.write(u'\t\t# (peut être complété en ajoutant le nombre de lignes nécessaires) \n')
	
	dirs = settings[6].rstrip(u'\n\r').split(u',')
	
	file.write(u'\n\t\tunits length meters \n')
	if u'Topof' in settings:
		file.write(u'\t\tunits counter %smeters \n' % unitcounter[settings[3]])
		file.write(u'\t\tcalibrate counter 0 %s \n' % settings[1])
		# To set the slope
		if u'Vulc' in settings:
			file.write(u'\t\tcalibrate clino 1 %s -1\n' % unitclino[settings[4]])
	if u'Prof' in settings:
		file.write(u'\t\tunits depth meters \n')
		typem = u'Prof'
	elif u'Deniv' in settings:
		file.write(u'\t\tunits depth meters \n')
		typem = u'Diving'
	
	file.write(u'\t\tunits compass %s \n' % (angleU[settings[2]]))
	if u'Vulc' in settings or 'Clino' in settings:
		file.write(u'\t\tunits clino %s \n' % (angleU[settings[4]]))
	
	file.write(u'\n\t\tdata %s %s %s %scompass %s%s %s\n' 
	           % (style[typem], station[u'vtopo'], lensurv[settings[0]], 
	              dir[dirs[0]], dir[dirs[1]], slopesurv[settings[3]],
	              lruddir[dirs[2]]))
	if comments != u'':
		file.write(u'\t\t\t#' + comments + u'\n')
	
	return


def writedata(file, settings, data, dataold):
	"""
	function to write the data in the .th file
	
	INPUTS:
		file     : variable that sets the file.th
		settings : List of the settings of this survey section
		data     : data from this survey section
		dataold  : data from the previous survey section
	   
	OUTPUTS:
		None
		
	USAGE:
		writeheader_th(file, cavename, entrance)
		
	Author: Xavier Robert, Lima 2016/06/27
	
	"""
	
	# dictl = length of the data line
	dictl = {u'Deca'  : 9,
	         u'Topof' : 10}
	
	i=0
	for elems in data:
		for k in [0,2]:
			if elems[k] == u'*':
				# remove the '*', and replace them with the right data !
				if i == 0: elems[k] = dataold[len(dataold)-1][k+1]
				else: elems[k] = data[i-1][k+1]
		if 	elems[0] == elems[1]: elems[1] = elems[1] + u'd'
		for k in range (dictl[settings[0]]-4, dictl[settings[0]]):
			# Check that LRUD != '*'; If yes, change them to 0
			if elems[k] == u'*': elems[k] = u'0'
		
		# Check if option 'E'
		if u'E' in elems:
			file.write(u'\t\t\tflags duplicate \n')
		# We write the data
		file.write(u'\t\t\t' + u'\t'.join(x for x in elems[0:dictl[settings[0]]]))
		
		if len(elems) > (dictl[settings[0]] + 2):
			if elems[dictl[settings[0]] + 1] != u'N' and elems[dictl[settings[0]] + 1] != u'I':
				# we add the comment if there is one
				file.write(u'\t# ' + ' '.join(x for x in elems[(dictl[settings[0]]+1) : len(elems)])[1:-1] + u'\n')
			elif len(elems) > (dictl[settings[0]] + 3):
				file.write(u'\t# ' + ' '.join(x for x in elems[(dictl[settings[0]]+2) : len(elems)])[1:-1] + u'\n')
			else:
				file.write(u'\n')
		else:
			file.write(u'\n')
		if 	elems[(dictl[settings[0]])] == u'I':
			file.write(u'\t\t\textend reverse \n')
		if u'E' in elems:
			file.write(u'\t\t\tflags not duplicate \n')	
		i+=1
				
	return

def write_thtot(file, cavename = u'cave', icomments = True, thlang = 'en'):
	"""
	Function to write the file cavename-tot.th
	
	INPUTS:
	   file         : variable that sets the file.th
	   cavename     : name of the cave
	   icomments    : True if comments in the file
		              False if not
		thlang      : 'fr' for french
		              'en' for english
		              ... other languages not implemented
	   
	OUTPUTS:
		None
		
	USAGE:
		write_thtot(file, cavename,  icomments, thlang)
		
	Author: Xavier Robert, Grenoble 2021/01/03
	
	"""
	
	file.write(u'encoding utf-8 \n\n')

	#file.write(u'encoding utf-8' \n\nsurvey %s -title "%s" -entrance "%s" \n'
	#           %(cavename.replace(u' ', u'_'), cavename, entrance))

	if icomments:
		if thlang == u'fr':
			file.write(u'# Copyright (C) %s Xavier Robert <xavier.robert***@***ird.fr>\n' %(str(datetime.datetime.now().year)))
			file.write(u'# Ce travaille est sous la licence Creative Commons Attribution-ShareAlike-NonCommecial :\n')
			file.write(u'#	<http://creativecommons.org/licenses/by-nc-sa/4.0/>\n\n') 
	elif thlang == u'en':
			file.write(u'# Copyright (C) %s Xavier Robert <xavier.robert***@***ird.fr>\n' %(str(datetime.datetime.now().year)))
			file.write(u'# This work is under the Creative Commons Attribution-ShareAlike-NonCommecial License:\n')
			file.write(u'#	<http://creativecommons.org/licenses/by-nc-sa/4.0/>\n\n') 
 
	file.write(u'survey %s -title "%s"\n\n' %(cavename.replace(u' ', u'_'), cavename.replace(u' ', u'_')))

	if icomments:
		if thlang == u'fr':
			file.write(u'\t# Pour importer les différentes données de différents fichiers topos :\n') 
		if thlang == u'en':
			file.write(u'\t# To import data from different data files:\n')
	file.write(u'\tinput Data/%s.th\n\n' %(cavename.replace(u' ', u'_')))
	
	file.write(u'#\tcenterline\n')
	if icomments:
		if thlang == u'fr': file.write(u'\t\t##Rajout des longueurs explorées, non topo, ou topos perdues\n')
		elif thlang == u'en': file.write(u'\t\t##Add length explored, but not surveyed, or with lost surveys\n')

		file.write(u'#\t\tstation Ca.31@%s "+78 m explorés " continuation explored 78m\n' %(cavename.replace(u' ', u'_')))
	if icomments:
		if thlang == u'fr': file.write(u'\t\t## Pour assembler plusieurs fichiers topos\n')
		elif thlang == u'en': file.write(u'\t\t## To join different surveys\n')

	file.write(u'#\t\tequate  6@%s  0@%s\n\n'%(cavename.replace(u' ', u'_'), cavename.replace(u' ', u'_') + u'2'))
		
	file.write(u'#\tendcenterline)\n\n')
 
	if icomments:
		file.write(u'#\t##########################################################################################\n')
		if thlang == u'fr': 
			file.write(u'#\t## Pour importer les différents fichiers de dessins en plan\n')
			file.write(u'#\t## Et Pour assembler plusieurs scraps entre eux, il faut utiliser la commande\n')
			file.write(u"#\t## join scrap1 scrap2 -count n (où n = nombre de galerie à connecter, par défaut n = 1). C'est tout simple !\n")
		elif thlang == u'en':
			file.write(u'#\t## To import different th2 files\n')
			file.write(u'#\t## And to join different scraps together, you need to use the command\n')
			file.write(u"#\t## join scrap1 scrap2 -count n (wher n = number of connections, by default n = 1). This is simple!\n")

	file.write(u'#\tjoin scrap1 scrap2 #-count n\n\n')

	if icomments:
		if thlang == u'fr': file.write(u'## Pour le plan\n')
		elif thlang == u'en': file.write(u'## For plan view\n')
	
	file.write(u'input Data/%s.th2\n\n' %(cavename.replace(u' ', u'_')))

	if icomments:
		if thlang == u'fr': file.write(u'## Pour la coupe développée\n')
		elif thlang == u'en': file.write(u'## For extended elevation\n')

	file.write(u'input Data/%s-coupe.th2\n\n' %(cavename.replace(u' ', u'_')))

	if icomments:
		if thlang == u'fr': file.write(u'## Appel des maps\n')
		elif thlang == u'en': file.write(u'## Call the maps file\n')

	file.write(u'input %s-maps.th\n\n' %(cavename.replace(u' ', u'_')))
	file.write(u'endsurvey\n')

	return




def write_thmaps(file, cavename = u'cave', icomments = True, thlang = 'en'):
	"""
	Function to write the file cavename-maps.th
	
	INPUTS:
	   file         : variable that sets the file.th
	   cavename     : name of the cave
	   icomments    : True if comments in the file
		              False if not
		thlang      : 'fr' for french
		              'en' for english
		              ... other languages not implemented
	   
	OUTPUTS:
		None
		
	USAGE:
		write_thmaps(file, cavename, icomments, thlang)
		
	Author: Xavier Robert, Grenoble 2021/01/03
	
	"""
	
	file.write(u'encoding utf-8 \n\n')

	#file.write(u'encoding utf-8' \n\nsurvey %s -title "%s" -entrance "%s" \n'
	#           %(cavename.replace(u' ', u'_'), cavename, entrance))

	if icomments:
		if thlang == u'fr':
			file.write(u'# Copyright (C) %s Xavier Robert <xavier.robert***@***ird.fr>\n' %(str(datetime.datetime.now().year)))
			file.write(u'# Ce travail est sous la licence Creative Commons Attribution-ShareAlike-NonCommecial :\n')
			file.write(u'#	<http://creativecommons.org/licenses/by-nc-sa/4.0/>\n\n') 
	elif thlang == u'en':
			file.write(u'# Copyright (C) %s Xavier Robert <xavier.robert***@***ird.fr>\n' %(str(datetime.datetime.now().year)))
			file.write(u'# This work is under the Creative Commons Attribution-ShareAlike-NonCommecial License:\n')
			file.write(u'#	<http://creativecommons.org/licenses/by-nc-sa/4.0/>\n\n') 

	file.write(u'map MP-%s-plan-tot -title "%s"\n' %(cavename.replace(u' ', u'_'), cavename.replace(u' ', u'_')))
	file.write(u'\tSP-%s-1\n' %(cavename.replace(u' ', u'_')))
	file.write(u'\t#break\n')
	file.write(u'\t#SP-%s-2\n' %(cavename.replace(u' ', u'_')))
	file.write(u'endmap\n')

	file.write(u'map MC-%s-coupe-tot -title "%s"\n' %(cavename.replace(u' ', u'_'), cavename.replace(u' ', u'_')))
	file.write(u'\tSC-%s-1\n' %(cavename.replace(u' ', u'_')))
	file.write(u'\t#break\n')
	file.write(u'\t#SC-%s-2\n' %(cavename.replace(u' ', u'_')))
	file.write(u'endmap\n')

	return


def write_thcoords(file, cavename = u'cave', coordinates = None, coordsyst = None, icomments = True, thlang = u'en'):
	"""
	Function to write the file Legends/entrances_coordinates.th
	
	INPUTS:
		file         : variable that sets the file.th
		cavename     : name of the cave
		cordinates   : Coordinates of the Cave
		coordsyst    : Coordinates system and projection
		icomments    : True if comments in the file
		              False if not
		thlang      : 'fr' for french
		              'en' for english
		              ... other languages not implemented
	   
	OUTPUTS:
		None
		
	USAGE:
		write_thcoords(file, cavename, coordinates, coordsyst, icomments, thlang)
		
	Author: Xavier Robert, Grenoble 2021/01/03
	
	"""
	
	# Coordinates definition
	if coordinates: 
		if coordsyst:
			# Transform Lambert coordinates into Lat Long coordinates
			inProj = Proj(coordsyst)
			outProj = Proj('epsg:4326')
			latc, longc = transform(inProj, outProj, float(coordinates[0]), float(coordinates[1]))
		else:
			latc = coordinates[1] + u'(Check coord. syst.)'
			longc = coordinates[0] + u'(Check coord. syst.)'
		altc = coordinates[2]
	else:
		latc = u'None'
		longc = u'None'
		altc = u'None'
		
	file.write(u'encoding utf-8 \n\n')

	if icomments:
		if thlang == u'fr':
			file.write(u'# Copyright (C) %s Xavier Robert <xavier.robert***@***ird.fr>\n' %(str(datetime.datetime.now().year)))
			file.write(u'# Ce travail est sous la licence Creative Commons Attribution-ShareAlike-NonCommecial :\n')
			file.write(u'#	<http://creativecommons.org/licenses/by-nc-sa/4.0/>\n\n') 
	elif thlang == u'en':
			file.write(u'# Copyright (C) %s Xavier Robert <xavier.robert***@***ird.fr>\n' %(str(datetime.datetime.now().year)))
			file.write(u'# This work is under the Creative Commons Attribution-ShareAlike-NonCommecial License:\n')
			file.write(u'#	<http://creativecommons.org/licenses/by-nc-sa/4.0/>\n\n') 

	file.write(u'layout Entrances_coords_%s\n\n' %(cavename.replace(u' ', u'_')))
	
	if icomments:
		if thlang == u'fr':
			file.write(u'\t# Layout qui définit les différentes variables contenant du texte avec \n')
			file.write(u"\t# les coordonnées de l'entrée que nous voulons ajouter au header.\n")
			file.write(u"\t# Nous avons besoin d'une variable par entrée.\n")
			file.write(u'\t# Ce layout est appelé par le layout Coords_Header ci-dessous\n\n')
		elif thlang == u'en':
			file.write(u'\t# Layout where we define the different variables that contain the text with \n')
			file.write(u'\t# the entrance coordinates we want to print in the header.\n')
			file.write(u'\t# We need one variable per entrance.\n')
			file.write(u'\t# This layout is called by the layout Coords_Header below\n\n')

	file.write(u'\tcode tex-map\n')
	file.write(u'\t\t\\def\\thjunk{ }\n')
	file.write(u'\t\t\\def\\thlocation%s{%s    --  Lat. : %s N ; Long. : %s E ; Alt. : %s m}\n' %(cavename.replace(u' ', u'_'), cavename.replace(u' ', u'_'), str(latc), str(longc), str(altc)))
	# We probably need in the future to iterate on the number of entrances... 
	# I do not knwo for the moment if Visual Top take in account different entrences coordinates
	file.write(u'\tendcode\n\n') 
	
	file.write(u'\tendlayout\n\n')


	file.write(u'layout Coords_Header_%s\n\n' %(cavename.replace(u' ', u'_')))
	if icomments:
		if thlang == u'fr': file.write(u'\t# Layout that set the presentation for the entrance coordinates.\n\n')
	
	file.write(u'\tcopy Entrances_coords_%s\n\n' %(cavename.replace(u' ', u'_')))
	if icomments:
		if thlang == u'fr':
			file.write(u'\t# Appelle le layout ci-dessus Entrances_coords où nous avons défini les différentes \n')
			file.write(u'\t# variables qui contiennent le texte avec \n')
			file.write(u'\t# les coordonnées des entrées à écrire dans le header.\n\n')
		elif thlang == u'en':
			file.write(u'\t# it calls the layout above Entrances_coords where we defined the different \n')
			file.write(u'\t# variables that contain the text with \n')
			file.write(u'\t# the entrance coordinates we want to print in the header.\n\n')
	
	file.write(u'\tcode tex-map\n')
	file.write(u'\t\t\\def\\nostring{}\n')
	file.write(u'\t\t\\def\\thsizexl{}\n')
	file.write(u'\t\t\\def\\thsizel{}\n')
	file.write(u'\t\t\\def\\thsizem{}\n')
	file.write(u'\t\t\\ifx\\thsizexl\\nostring\\def\\thsizexl{30}\\else\\fi\n')
	file.write(u'\t\t\\ifx\\thsizel\\nostring\\def\\thsizel{24}\\else\\fi\n')
	file.write(u'\t\t\\ifx\\thsizem\\nostring\\def\\thsizem{12}\\else\\fi\n\n')
		
	file.write(u'\t\t\\ECoordinates={\n')
	file.write(u'\t\t\t\\edef\\tmp{\\thjunk} \\ifx\\tmp\\empty \\else\n')
	file.write(u'\t\t\t\t{\\size[\\thsizem] \\ss\\thjunk\\vss}\n')
	file.write(u'\t\t\t\\fi\n')
	file.write(u'\t\t\t\\edef\\tmp{\\thlocation%s} \\ifx\\tmp\\empty \\else\n' %(cavename.replace(u' ', u'_')))
	file.write(u'\t\t\t\t# The first one should be without hskip\n')
	file.write(u'\t\t\t\t{\\size[\\thsizem]\\hskip2cm \\ss\\thlocation%s\\vss}\n' %(cavename.replace(u' ', u'_')))
	file.write(u'\t\t\t\\fi\n')
	file.write(u'\t\t\t}\n')
	file.write(u'\tendcode\n\n')

	file.write(u'\tendlayout\n\n')

	return