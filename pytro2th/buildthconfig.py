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
	  - function called by other programs
	
	
	INPUTS:
		The inputs are in the script file, in the "# Define data to analysis" section. 
		The different arguments are described.
	
"""

###### To DO :  #######
#	- Add a maps.th file
#	- Add a cave-tot.th file
#	- Update cave output structure
#	- 
###### End To DO #######

from __future__ import  division
# This to be sure that the result of the division of integers is a real, not an integer
#from __future__ import unicode_literals

# Import modules
import sys
import os
import numpy as np

########################

def builddictcave(
                  thlang = u'en', icomments = True, icoupe = True, Errfiles = True,
                  thcfile = True, thcfnme = u'config.thc', thcpath = None, 
                  thconfigfile = True, thconfigpath = None, thconfigfnme= u'Test.thconfig'):
	"""
	
	"""
	
	########################
	#    Define parameters
	# thlang: language to set in the files, can be english [en] or french [fr]
	#thlang = 'fr'
	# thcfile: set to True to build a config file, or False if not
	#thcfile = True
	# thcfnme: name of the thc file
	#thcfnme = 'config.thc'
	# thcpath: path where to add the config file.
	#          if None, it will be in the folder from where is run the code
	#thcpath = None
	# thconfigfile: set to True to build a thconfig file, or False if not
	#thconfigfile = True
	# thconfigpath: path where to add the thconfig file.
	#               if None, it will be in the folder from where is run the code
	#thconfigpath = None
	# thconfigfnme: name of the thconfig file
	#thconfigfnme= 'Test.thconfig'
	#icomments: True if we add comments inside the thconfig file,
	#          False if there is no comments inside the thconfig file
	#icomments = True
	#icoupe: True if we want a layout for extended projection in the thconfig
	#       False if not
	#icoupe = True
	
	# Errfiles: True to write on previous files; be careful in that case !!
	#           False if not
	#Errfiles = True


	# sourcefiles: source files
	sourcefile = [u'example.th', u'example.th2', u'example-coupe.th2']
	# xviscale: scale of the xvi file
	#           1000 corresponds to 1/1000
	xviscale = 1000
	# xvigrid: spacing of the grid for the xvi, in meters
	xvigrid = 10
	# cavefnme: cave fnme
	cavefnme = u'Example'
	# coord: coordinate system
	#        Can be set to None
	coord = None
	# scale: scale of the map
	#        500 corresponds to 1/500
	scale = 500 
	
	
	datac = [thlang, thcfile, thcfnme, thcpath, 
	        thconfigfile, thconfigpath, thconfigfnme, 
	        icomments, icoupe, Errfiles]
	dictcave = [sourcefile, xviscale, xvigrid, cavefnme, coord, scale]
	
	return dictcave, data


def writethconfig(pdata, icomments, icoupe, thlang, dictcave,
                  thcfile, pdata2 = None):
	"""
		Function to write a .thconfig file for a cave
		
		INPUTS:
			pdata     : path and name of the .thconfig file
			icomments : True if comments in the file
			            False if no comments in the file
			icoupe    : True for a layout to print an extended elevation map
			            False if not
			thlang    : 'fr' for french
			            'en' for english
			            ... other languages not implemented
			dictcave  : list with [sourcefile, xviscale, xvigrid, cavefnme, coord, scale]
    	    thcfile   : set to True to build a config file, 
    		            or False if not
        	pdata2    : path and name of the config file
			
		OUTPUTS:
			thconfig file
			
		USAGE:
			writethconfig(pdata, icomments, icoupe, thlang, dictcave, thcfile, [pdata2]):
			
	"""
	
	f2w = open(pdata, 'w')
	
	f2w.write(u'encoding utf-8 \n\n')
	f2w.write(u'# File written by pytro2th (Xavier Robert)  \n')
	f2w.write(u'# Copyright (C) 2021 Xavier Robert <xavier.robert@ird.fr> \n')
	f2w.write(u'# This work is under the licence Creatice Commonc CC-by-nc-sa v.4 \n\n')
  
  
	if icomments: 
		f2w.write(u'# 1-SOURCES  \n')
		if thlang == u'fr':
			f2w.write(u'# La ligne source specifie le fichier où sont les données topo \n')
			f2w.write(u'# (Au fichier "nomcavite.th" il faudra avoir une ligne \n')
			f2w.write(u'# "input "nomcavite.th2" pour spécifier le fichier où se trouvent \n')
			f2w.write(u'# les données du dessin, comme ça, ce fichier thconfig appelera  \n')
			f2w.write(u'# nomcavite.th" et a son tour, "nomcavite.th" appelera \n')
			f2w.write(u'# "nomcavite.th2") \n')
		elif thlang == u'en':
			f2w.write(u'# Source\'s line specify the files with the surveyed data \n')
			f2w.write(u'# (With the file "mycave.th" we need to add a line \n')
			f2w.write(u'# "input "nomcavite.th2" to specify the file with the drawing data\n')
			f2w.write(u'# This file thconfig will call "mycave.th"  and then, "mycave.th"\n' )
			f2w.write(u'# will call mycave.th2") \n')
	
	# Do a loop on the input files
	#	To move in the cave-tot.th and only call that last file?
	for cfile in dictcave[0]:
		f2w.write(u'source ' + cfile + u'\n')
	f2w.write(u'\n')
	
	if icomments: 
		if thlang == u'fr':
			f2w.write(u'# Ajoute un fichier de configuration\n')
			f2w.write(u'# Voir https://github.com/robertxa/Th-Config-Xav pour un exemple\n')
		elif thlang == u'en':
			f2w.write(u'# Add config file \n')
			f2w.write(u'# See https://github.com/robertxa/Th-Config-Xav for an example\n')
	if thcfile: 
		f2w.write(u'input ' + pdata2 + u'  \n\n\n')
	else:
		f2w.write(u'#input config.thc  \n\n\n')
  
  
	if icomments: f2w.write(u'# 2-LAYOUT    \n')
	if icomments: 
		if thlang == u'fr': f2w.write(u'# Debut de la définition du Layout "xviexport" \n')
		elif thlang == u'en': f2w.write(u'# Begin the definition of the Layout "xviexport" \n')
	f2w.write(u'layout xviexport \n')
	if icomments: 
		if thlang == u'fr': f2w.write(u'\t# Echelle a laquelle on veut dessiner la topo \n')
		if thlang == u'en': f2w.write(u'\t# Scale to draw the survey \n')
	f2w.write(u'\tscale 1 ' + str(dictcave[1]) + u' \n')
	if icomments: 
		if thlang == u'fr': f2w.write(u'\t# Taille de la grille \n')
		elif thlang == u'en': f2w.write(u'\t# Size of the grid \n')
	f2w.write(u'\tgrid-size ' + str(dictcave[2]) + u' ' + str(dictcave[2]) + u' ' + str(dictcave[2]) + u' m \n')
	if icomments: 
		if thlang == u'fr': f2w.write(u'\t# Mettre la grille en arrière plan \n')
		elif thlang == u'en': f2w.write(u'\t# Set the grid to the background \n')
	f2w.write(u'\tgrid bottom \n')
	f2w.write(u'endlayout \n')
	if icomments: 
		if thlang == u'fr': f2w.write(u'# Fin de la définition du layout "xviexport"  \n')
		if thlang == u'en': f2w.write(u'# End of the definition of the layout "xviexport"  \n')
	f2w.write(u'\n\n')
	
	writelayout(f2w, dictcave, icomments, thlang)
	if icoupe:
		f2w.write(u'\n\n')
		writelayout(f2w, dictcave, icomments, thlang, icoupe)
	
	f2w.write(u'\n\n')
	f2w.write(u'# 3-EXPORTS   \n')
	f2w.write(u'export map -fmt xvi -layout xviexport -o '+ dictcave[3] + u'-map.xvi\n')
	if icoupe: f2w.write(u'export map -projection extended -fmt xvi -layout xviexport -o '+ dictcave[3] + u'-coupe.xvi\n\n')
 
	f2w.write(u'export map -o '+ dictcave[3] + u'-plan.pdf -layout my_layout\n')
	if icoupe: f2w.write(u'export map -projection extended -layout my_layout-coupe -o '+ dictcave[3] + u'-coupe.pdf\n')
	f2w.write(u'export model -o '+ dictcave[3] + u'.lox\n\n')
 
	f2w.write(u'# Export des fichiers ESRI\n')
	f2w.write(u'export map -proj plan -fmt esri -o '+ dictcave[3] + u' -layout my_layout\n')
 
	f2w.write(u'# Export des fichiers kml\n')
	f2w.write(u'export map -proj plan -fmt kml -o '+ dictcave[3] + u'.kml -layout my_layout\n\n')

	
	f2w.closed
	
	print(u'\tFile ' + pdata + u' written...')
	
	return


def writelayout(fw, dictcave, icomments, thlang, icoupe = None):
	"""
		Function to write a layout in a .thconfig file
		
		INPUTS:
			fw: variable that define the file to write in
			dictcave  : list [sourcefile, xviscale, xvigrid, cavefnme, coord, scale]
			icomments : True if comments in the file
			            False if no comments in the file
			thlang    : 'fr' for french
			            'en' for english
			            ... other languages not implemented
			icoupe    : True to tell there is an elevation map
			            if None no layout for extended elevation map
		OUTPUTS:
			None
		USAGE:
			writelayout(fw, dictcave, icomments, thlang, [icoupe])
		
		Author: Xavier Robert, Lima 2016/06/27
		
	"""

	if not icoupe:
		fw.write(u'layout my_layout\n\n')
	else:
		fw.write(u'layout my_layout-coupe\n\n')

	fw.write(u'\t#copy northarrowMG \n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Appelle le fichier de configuration (Layout config dans le fichier config.thc file)\n')
		elif thlang == u'en':
			fw.write(u'\n\t# Call the config settings (Layout config inside the config.thc file)\n')
	fw.write(u'\tcopy drawingconfig \n')

	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Titre  \n')
		elif thlang == u'en':
			fw.write(u'\n\t# Title  \n')
	fw.write(u'\tdoc-title "' + str(dictcave[3]) + '"\n')
  
	if not icoupe:	
		# print this lines for cs systems only for the plan view, not for the extended elevation view
		if icomments:
			if thlang == u'fr':
				fw.write(u'\n\t# Pour faire la topo dans le système UTM  \n')
				fw.write(u'\t# Décommenter la ligne, et remplacer xx par la zone UTM\n')
			elif thlang == u'en':
				fw.write(u'\n\t# To draw the map survey in the UTM system  \n')
				fw.write(u'\t# Uncomment the line, and remplace xx by the UTM zone used\n')
		if dictcave[4] == None:
			fw.write(u'\t#cs UTMxx\n')
		else:
			fw.write(u'\tcs ' + dictcave[4] + ' \n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# "base-scale" specifie l\'échelle à laquelle nous avons\n')
			fw.write(u'\t# dessiné nos croquis. Par defaut, c\'est 1/200.\n')
			fw.write(u'\t# Si on a utilise une autre échelle, \n')
			fw.write(u'\t# il faut enlever le "#" et spécifier l échelle vraiment\n')
			fw.write(u'\t# employée, c\'est le cas apres avoir dessiné la topo\n')
			fw.write(u'\t# sur un cheminement exporté avec le layout "xviexport"\n')
			fw.write(u'\t# (voir en bas)\n')
		elif thlang == u'en':
			fw.write(u'\n\t# "base-scale" is the scale we use to draw the survey\n')
			fw.write(u'\t#  (see xviexport layout). Defaut is 1/200.\n')
			fw.write(u'\t# If we use an other scale,, we have to uncomment this \n')
			fw.write(u'\t# line and specify the drwing scale\n') 
	fw.write(u'\tbase-scale 1 ' + str(dictcave[1]) + '\n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# "scale" : specification de l\'échelle,\n')
			fw.write(u'\t# pour imprimer la topo. La combination entre scale et base-scale\n')
			fw.write(u'\t# controlle le gros des lignes, rotation, etc, convenable\n')
			fw.write(u'\t# pour faire l\'amplification-reduction entre dessin(s) et\n')
			fw.write(u'\t# le resultat de l imprimante\n')
			fw.write(u'\t# C\'est tres important de s\'assurer que la configuration de\n')
			fw.write(u'\t# l\'imprimante ne spécifie pas l\'option "Fit in page"\n')
			fw.write(u'\t# ou similaire, sinon, l\'échelle sera changée pendant\n')
			fw.write(u'\t# l\'impression\n')
		elif thlang == u'en':
			fw.write(u'\n\t# "scale" : Scale we want for the final output \n')
			fw.write(u'\t# to print the topography')
			fw.write(u'\t# Be careful with the printer configuration\n')
			fw.write(u'\t# The option "Fit in page" or similar\n')
			fw.write(u'\t# will change the scale of the printed topography\n')
	fw.write(u'\t#scale 1 1000\n')
	fw.write(u'\tscale 1 ' + str(dictcave[5]) + u'\n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Echelle graphique de 100 m d\'ampleur\n')
		elif thlang == u'en':
			fw.write(u'\n\t# Length of the scale bar (Here, 100 m)\n')
	fw.write(u'\t#scale-bar 100 m\n')
	fw.write(u'\tscale-bar ' + str(dictcave[5]/10) + u' m\n')
  
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Pour faire une rotation\n')
		elif thlang == u'en':
			fw.write(u'\n\t# To rotate the map\n')
	fw.write(u'\t#rotate 2.25\n')
  
	fw.write(u'\t#origin 12 22 0 m\n')
	fw.write(u'\t#origin-label 100 K\n')
  
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Une couleur de fond, 85% blanc = 15% noir\n')
		elif thlang == u'en':
			fw.write(u'\n\t# Background color, 85% white = 15% black\n')
	fw.write(u'\t#color map-bg 85\n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Une couleur de topo (RVB)\n')
		elif thlang == u'en':
			fw.write(u'\n\t# Map color (RVB)\n')
	fw.write(u'\tcolor map-fg [100 100 80]\n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# la topo est transparente (on peut voir les galeries sousjacentes)\n')
			fw.write(u'\t# Par défaut, donc, pas vraiment besoin de specifier\n')
		elif thlang == u'en':
			fw.write(u'\n\t# To impose transparency for the topography\n' )
			fw.write(u'\t(# We can thus see the lower tunnels)\n')
			fw.write(u'\t# Option on by default, so not necessary\n')
	fw.write(u'\ttransparency on\n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Pourcentage de transparence, marche seulement si transparency est "on"\n')
		elif thlang == u'en':
			fw.write(u'\n\t# Pourcentage of transparency, only if transparency is "on"\n')
	fw.write(u'\topacity 75\n')
    
	if thlang == u'fr':
		if icomments:
			fw.write(u'\n\t# Un commentaire à ajouter au titule,\n')
		if not icoupe:
			fw.write(u'\tmap-comment "Plan, Projection UTM32, Samoëns, 74, France"\n')
		else:
			fw.write(u'\tmap-comment "Coupe développée, Samoëns, 74, France"\n')
		
	elif thlang == u'en':
		if icomments:
			fw.write(u'\n\t# Add a comment in the header,\n')
		if not icoupe:
			fw.write(u'\tmap-comment "Plan, Projection UTM32, Samoëns, 74, France"\n')
		else:
			fw.write(u'\tmap-comment "Extended elevation, Samoëns, 74, France"\n')
  
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Afficher les statistiques d\'explo par équipe/nom. C\'est lourd\n')
			fw.write(u'\t# si la cavite est importante et qu\'il y a beaucoup d\'explorateurs\n')
		elif thlang == u'en':
			fw.write(u'\n\t# Print exploration stats (team/name). it is heavy\n')
			fw.write(u'\t# if the cave is long with lots of explorers\n')
	fw.write(u'\tstatistics explo-length off\n')
  
	if icomments:
		if thlang == 'fr':
			fw.write('\n\t# Afficher le développement et profondeur de la cavité\n')
		elif thlang == 'en':
			fw.write('\n\t# Print length and depth\n')
	fw.write('\tstatistics topo-length off\n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Nous voulons une légende pour expliquer les symboles.\n') 
			fw.write(u'\n\t#\t"on" imprimera seulement la légende des symboles dessinés sur la topo\n')
			fw.write(u'\n\t#\tSi l\'on veut pour tous les symboles, utilisés ou pas, il faut indiquer "all".\n')
			fw.write(u'\t# "legend off" = pas de légende\n')
		elif thlang == u'en':
			fw.write(u'\n\t# Print a Legend for the symbols we use\n')
			fw.write(u'\t# It is posible to print only the symbols we use (here),\n')
			fw.write(u'\t# or all of them, used or not with "legend all".\n')
			fw.write(u'\t# "legend off" = no legende\n')
	fw.write(u'\tlegend off\n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Afficher un copyright\n')
		elif thlang == u'en':
			fw.write(u'\n\t# print a copyright\n')
	fw.write(u'\tstatistics copyright all\n')
  
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Par defaut, la légende est de 14 cm de largeur\n')
		elif thlang == u'en':
			fw.write(u'\n\t# Default width legend is 14 cm\n')
	fw.write(u'\t#legend-width 14 cm\n')
  
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Spécification de la position de la manchette : interieur\n')
			fw.write(u'\t# occuppée par le titule, auteurs, etc. Nous pouvons indiquer\n')
			fw.write(u'\t# les cordonnées du point de la topo ou l\'on veut la manchette :\n')
			fw.write(u'\t# 0 0, c\'est en bas, à gauche\n')
			fw.write(u'\t# 100 100, c\'est en haut, à droite\n')
			fw.write(u'\t# La manchette a des "points cardinaux" : n, s, ne, sw, etc.\n')
			fw.write(u'\t# Il faut spécifier un de ces points \n')
		elif thlang == u'en':
			fw.write(u'\n\t# Position of the Header (title, authors,...) \n')
			fw.write(u'\t# We indicate the coordinates of the point where we want it \n')
			fw.write(u'\t# 0 0, is bottom left \n')
			fw.write(u'\t# 100 100, is top right \n')
			fw.write(u'\t# The header has cardinal points: n, s, ne, sw, etc. \n')
			fw.write(u'\t# We have to specify one of these points \n')
	fw.write(u'\tmap-header 0 30 nw\n')
  
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Arrière plan de la manchette\n')
		elif thlang == u'en':
			fw.write(u'\n\t# header\'s background\n')
	fw.write(u'\tmap-header-bg off\n')
	fw.write(u'\n\tlayers on\n')
  
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Options pour afficher le squelette topo,\n')
			fw.write(u'\t# les points et le nom des stations topos\n')
		elif thlang == u'en':
			fw.write(u'\n\t# Options to print the legs of the survey,\n')
			fw.write(u'\t# stations points and stations names\n')
	fw.write(u'\tsymbol-hide line survey\n')
	fw.write(u'\t#debug station-names\n')
  
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Spécifier qu\'il faut imprimer une grille\n')
			fw.write(u'\t# au dessous de la topo  \n')
		elif thlang == u'en':
			fw.write (u'\n\t# If we want a grid in background  \n')
	fw.write(u'\t#grid bottom\n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Spécifier le pas de la grille, ici 100x100x100 metres\n')
			fw.write(u'\t# (Trois dimensions, oui, ça sert pour la coupe aussi) \n')
		elif thlang == u'en':
			fw.write(u'\n\t# Step of the grid in 3-D \n')
	fw.write(u'\t#grid-size 100 100 100 m\n')
	if icomments:
		if thlang == u'fr':
			fw.write(u'\n\t# Si nous ne voulons pas de grille :\n')
		elif thlang == u'en':
			fw.write(u'\n\t# if we do not want any grid:\n')
	fw.write(u'\tgrid off\n')
  
	fw.write(u'\n\t# Titre          \n')
	fw.write(u'\tcode tex-map\n')
	if icomments:
		if thlang == u'en':
			fw.write(u'\t\t% Output map title as determined by Therion 5.3 is stored in cavename. \n')
			fw.write(u'\t\t% It will be empty if there are multiple maps selected for any one projection\n')
			fw.write(u'\t\t% AND there are multiple source surveys identified in the thconfig file \n')
			fw.write(u'\t\t% i.e. Therion can not infer a unique title from the input data given.\n')
			fw.write(u'\t\t% This code allows you to define an output map title {cavename} if it happens to be empty\n')
		elif thlang == u'fr':
			fw.write(u'\t\t% Le titre de la carte determiné par Therion 5.3 est enregistré dans la variable cavename. \n')
			fw.write(u'\t\t% Elle est vide lorsque plusieurs maps sont sélectionnées\n')
			fw.write(u'\t\t% et s\'il y a différentes données topograhiques dans le thconfig \n')
			fw.write(u'\t\t% i.e. Therion ne peut donner un titre unique à partir des inputs.\n')
			fw.write(u'\t\t% Ce code permet alors de définir un titre {cavename} dans le cas où il est vide\n')
	fw.write(u'\t\t\edef\temp{\\the\cavename}   ')
	if thlang == u'fr': fw.write(u'% cavename pour Therion\n')
	if thlang == u'en': fw.write(u'% cavename from Therion\n')
	fw.write(u'\t\t\edef\\nostring{}            ')
	if thlang == u'fr': fw.write(u' % string vide\n')
	if thlang == u'en': fw.write(u' % empty string\n')
	fw.write(u'\t\t\ifx\\temp\\nostring          ')
	if thlang == u'fr': fw.write(u' % test si cavename est vide\n')
	if thlang == u'en': fw.write(u' % test if cavename is empty\n')
	if thlang == u'fr': fw.write(u'\t\t\t% s\'il est vide, réassigne cavename pour décrire les maps sélectionnées comme un groupe\n')
	if thlang == u'en': fw.write(u'\t\t\t% if empty reassign cavename to describe selected maps as a group\n')
	fw.write(u'\t\t\t\cavename={' + dictcave[3] + u'} 		\n')
	fw.write(u'\t\t\else ')
	if thlang == u'fr': fw.write(u'% Si non, alors garde la valeur de Therion, ou assigne un cavename ici pour l\'écraser\n')
	if thlang == u'en': fw.write(u'% if not empty keep the value set by therion, or assign an override cavename here\n')
	fw.write(u'\t\t\\fi\n')
	fw.write(u'\tendcode  \n\n')  
	fw.write(u'endlayout\n')
	
	return
	
def writethc(pdata):
	"""
		Function to write the config.thc file
		
		INPUTS:
			pdata : path + name of the config.thc file
			
		OUTPUTS:
			new contig.thc file
			
		USAGE:
			writethc(pdata)
		
		Author: Xavier Robert, Lima 2016/06/27
		
		Licence: CCby-nc
	"""
	# Open the file
	f1w = open(pdata,'w')
	
	f1w.write(u'encoding utf-8 \n\n') 
	f1w.write(u'# File to set up specific settings for Therion drawing outputs \n')
	f1w.write(u'# In your *.thconfig file, you need to call this file with: \n')
	f1w.write(u'#    input <path/to/the/file/>config.thc \n')
	f1w.write(u'# and then, in each layout, you need to call the corresponding layout: \n')
	f1w.write(u'#    copy drawingconfig \n\n\n')
	f1w.write(u'# change the name for the legend\n')
	f1w.write(u'text en "line u:rope" "rope" #text to appear in legend\n')
	f1w.write(u'text fr "line u:rope" "corde" #text to appear in legend \n')
	f1w.write(u'text en "line u:fault" "fault" #text to appear in legend\n')
	f1w.write(u'text fr "line u:fault" "faille" #text to appear in legend \n')
	f1w.write(u'text en "line u:strata" "strata" #text to appear in legend\n')
	f1w.write(u'text fr "line u:strata" "strate" #text to appear in legend \n\n')
	f1w.write(u'layout drawingconfig\n')
	f1w.write(u'# Layout to draw the map and extended view.\n\n')
	f1w.write(u'\t# Set the language\n')
	f1w.write(u'\tlanguage fr\n')
	f1w.write(u'\t# Auteur \n')
	f1w.write(u'\tdoc-author "Xavier Robert"\n')
	f1w.write(u'\t# Set the symology you want to use: UIS, ASF (Australie) CCNP (Etats Units) ou\n')
	f1w.write(u'\t# SKB (tchecoslovakia) \n')
	f1w.write(u'\t#symbol-set UIS\n')
	f1w.write(u'\t# Change the type or colors of symbols:\n')
	f1w.write(u'\tsymbol-assign point station:temporary SKBB\n')
	f1w.write(u'\tsymbol-color point water-flow [0 0 100]\n')
	f1w.write(u'\tsymbol-color line water-flow [0 0 100]\n')
	f1w.write(u'\tsymbol-color point ice [0 0 100]\n')
	f1w.write(u'\tsymbol-color line wall:ice [0 0 100]\n')
	f1w.write(u'\tsymbol-color point ice-pillar [0 0 100]\n')
	f1w.write(u'\tsymbol-color area ice [0 0 100]\n')
	f1w.write(u'\tsymbol-color point snow [0 0 100]\n')
	f1w.write(u'\tsymbol-color point spring [0 0 100]\n')
	f1w.write(u'\tsymbol-color point root [0 100 0]\n')
	f1w.write(u'\tsymbol-color point vegetable-debris [0 100 0]\n')
	f1w.write(u'\tsymbol-color point altitude [100 50 0]\n\n')
	f1w.write(u'\tcode metapost\n\n')
	f1w.write(u'\t\t# to change blocs size\n')
	f1w.write(u'\t\tdef a_blocks (expr p) =\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tpickup PenC;\n')
	f1w.write(u'\t\t\tpath q, qq; q = bbox p;\n')
	f1w.write(u'\t\t\tpicture tmp_pic; \n')
	f1w.write(u'\t\t\tuu := max(u, (xpart urcorner q - xpart llcorner q)/100, (ypart urcorner q - ypart     llcorner q)/100);\n')
	f1w.write(u'\t\t\ttmp_pic := image(\n')
	f1w.write(u'\t\t\tfor i = xpart llcorner q step 1.0uu until xpart urcorner q:\n')
	f1w.write(u'\t\t\t\tfor j = ypart llcorner q step 1.0uu until ypart urcorner q:\n')
	f1w.write(u'\t\t\t\t\tqq := punked (((-.3uu,-.3uu)--(.3uu,-.3uu)--(.3uu,.3uu)--(-.3uu,.3uu)--cycle) \n')
	f1w.write(u'\t\t\t\t\trandomized (uu/2))\n')
	f1w.write(u'\t\t\t\t\t\trotated uniformdeviate(360)\n')
	f1w.write(u'\t\t\t\t\t\tshifted ((i,j) randomized 1.0uu);\n')
	f1w.write(u'\t\t\t\t\tif xpart (p intersectiontimes qq) < 0:\n')
	f1w.write(u'\t\t\t\t\t\tthclean qq;\n')
	f1w.write(u'\t\t\t\t\t\tthdraw qq;\n')
	f1w.write(u'\t\t\t\t\tfi;\n')
	f1w.write(u'\t\t\t\tendfor;  \n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\t\t);\n')
	f1w.write(u'\t\t\tclip tmp_pic to p;\n')
	f1w.write(u'\t\t\tdraw tmp_pic;\n')
	f1w.write(u'\t\tenddef;\n\n')
	f1w.write(u'\t\t#  To change sand aspects\n')
	f1w.write(u'\t\tdef a_sands (expr p) =\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tpickup PenC;\n')
	f1w.write(u'\t\t\tpath q; q = bbox p;\n')
	f1w.write(u'\t\t\tpicture tmp_pic;\n')
	f1w.write(u'\t\t\ttmp_pic := image(\n')
	f1w.write(u'\t\t\tfor i = xpart llcorner q step 0.1u until xpart urcorner q:\n')
	f1w.write(u'\t\t\t\tfor j = ypart llcorner q step 0.1u until ypart urcorner q:\n')
	f1w.write(u'\t\t\t\t\tdraw origin shifted ((i,j) randomized 0.1u) withpen PenC;\n')
	f1w.write(u'\t\t\t\tendfor;\n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\t\t);\n')
	f1w.write(u'\t\t\t#clip tmp_pic to p;\n')
	f1w.write(u'\t\t\tdraw tmp_pic;\n')
	f1w.write(u'\t\tenddef;\n\n\n\n')
	f1w.write(u'\t\t####### Metapost-changes ############\n\n\n')
	f1w.write(u'\t\t# To change pebbles aspects\n')
	f1w.write(u'\t\tdef a_pebbles_SKBB (expr p) =\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tpickup PenC;\n')
	f1w.write(u'\t\t\tpath q, qq; q = bbox p;\n')
	f1w.write(u'\t\t\tpicture tmp_pic; \n')
	f1w.write(u'\t\t\ttmp_pic := image(\n')
	f1w.write(u'\t\t\tfor i = xpart llcorner q step .1u until xpart urcorner q:\n')
	f1w.write(u'\t\t\t\tfor j = ypart llcorner q step .5u until ypart urcorner q:\n')
	f1w.write(u'\t\t\t\t\tqq := (superellipse((.07u,0),(0,.03u), (-.07u,0),(0,.-.03u),.75))\n')
	f1w.write(u'\t\t\t\t\t%randomized (u/25)\n')
	f1w.write(u'\t\t\t\t\trotated uniformdeviate(360) \n')
	f1w.write(u'\t\t\t\t\tshifted ((i,j) randomized 0.27u);\n')
	f1w.write(u'\t\t\t\t\tif xpart (p intersectiontimes qq) < 0:\n')
	f1w.write(u'\t\t\t\t\t\tthdraw qq;\n')
	f1w.write(u'\t\t\t\t\tfi;\n')
	f1w.write(u'\t\t\t\tendfor;  \n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\t\t);\n')
	f1w.write(u'\t\t\tclip tmp_pic to p;\n')
	f1w.write(u'\t\t\tdraw tmp_pic;\n')
	f1w.write(u'\t\tenddef;\n\n')
	f1w.write(u'\t\t# To change slopes aspects\n')
	f1w.write(u'\t\tdef l_slope (expr P,S)(text Q) = \n')
	f1w.write(u'\t\t\t%show Q;\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tnumeric dirs[];\n')
	f1w.write(u'\t\t\tnumeric lengths[];\n')
	f1w.write(u'\t\t\tfor i=Q:\n')
	f1w.write(u'\t\t\t\tdirs[redpart i]:=greenpart i;\n')
	f1w.write(u'\t\t\t\tlengths[redpart i]:=bluepart i;\n')
	f1w.write(u'\t\t\tendfor;  \n')
	f1w.write(u'\t\t\tli:=length(P); % last\n')
	f1w.write(u'\t\t\talw_perpendicular:=true;\n')
	f1w.write(u'\t\t\tfor i=0 upto li:\n')
	f1w.write(u'\t\t\tif unknown dirs[i]: dirs[i]:=-1; \n')
	f1w.write(u'\t\t\telse: \n')
	f1w.write(u'\t\t\t\tif dirs[i]>-1:\n')
	f1w.write(u'\t\t\t\t\tdirs[i]:=((90-dirs[i]) - angle(thdir(P,i))) mod 360;\n')
	f1w.write(u'\t\t\t\t\talw_perpendicular:=false;\n')
	f1w.write(u'\t\t\t\tfi;\n')
	f1w.write(u'\t\t\tfi;\n')
	f1w.write(u'\t\t\tif unknown lengths[i]: lengths[i]:=-1; fi;\n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\t\t%for i=0 upto li: show dirs[i]; endfor;\n')
	f1w.write(u'\t\t\tni:=0; % next\n')
	f1w.write(u'\t\t\tpi:=0; % previous\n')
	f1w.write(u'\t\t\tfor i=0 upto li:\n')
	f1w.write(u'\t\t\t\td:=dirs[i];\n')
	f1w.write(u'\t\t\t\tif d=-1:\n')
	f1w.write(u'\t\t\t\t\tif (i=0) or (i=li):\n')
	f1w.write(u'\t\t\t\t\t\tdirs[i] := angle(thdir(P,i) rotated 90) mod 360;\n')
	f1w.write(u'\t\t\t\t\t\tpi:=i;\n')
	f1w.write(u'\t\t\t\t\telse:\n')
	f1w.write(u'\t\t\t\t\t\tif ni<=i:\n')
	f1w.write(u'\t\t\t\t\t\t\tfor j=i upto li:\n')
	f1w.write(u'\t\t\t\t\t\t\t\tni:=j;\n')
	f1w.write(u'\t\t\t\t\t\t\t\texitif dirs[j]>-1;\n')
	f1w.write(u'\t\t\t\t\t\t\tendfor;\n')
	f1w.write(u'\t\t\t\t\t\tfi;\n')
	f1w.write(u'\t\t\t\t\t\tw:=arclength(subpath(pi,i) of P) / \n')
	f1w.write(u'\t\t\t\t\t\tarclength(subpath(pi,ni) of P);\n')
	f1w.write(u'\t\t\t\t\t\tdirs[i]:=w[dirs[pi],dirs[ni]];\n')
	f1w.write(u'\t\t\t\t\t\t%if (dirs[i]-angle(thdir(P,i))) mod 360>180:\n')
	f1w.write(u'\t\t\t\t\t\t%dirs[i]:=w[dirs[ni],dirs[pi]];\n')
	f1w.write(u'\t\t\t\t\t\t%message("*******");\n')
	f1w.write(u'\t\t\t\t\t\t%fi;\n')
	f1w.write(u'\t\t\t\t\tfi;\n')
	f1w.write(u'\t\t\t\telse:\n')
	f1w.write(u'\t\t\t\t\tpi:=i;\n')
	f1w.write(u'\t\t\t\tfi;\n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\t\t%for i=0 upto li: show dirs[i]; endfor;\n')
	f1w.write(u'\t\t\tni:=0; % next\n')
	f1w.write(u'\t\t\tpi:=0; % previous\n')
	f1w.write(u'\t\t\tfor i=0 upto li:\n')
	f1w.write(u'\t\t\t\tl:=lengths[i];\n')
	f1w.write(u'\t\t\t\tif l=-1:\n')
	f1w.write(u'\t\t\t\t\tif (i=0) or (i=li):\n')
	f1w.write(u'\t\t\t\t\t\tlengths[i] := 1cm; % should never happen!\n')
	f1w.write(u'\t\t\t\t\t\tthwarning("slope width at the end point not specified");\n')
	f1w.write(u'\t\t\t\t\t\tpi:=i;\n')
	f1w.write(u'\t\t\t\t\telse:\n')
	f1w.write(u'\t\t\t\t\t\tif ni<=i:\n')
	f1w.write(u'\t\t\t\t\t\t\tfor j=i+1 upto li:\n')
	f1w.write(u'\t\t\t\t\t\t\t\tni:=j;\n')
	f1w.write(u'\t\t\t\t\t\t\t\texitif lengths[j]>-1;\n')
	f1w.write(u'\t\t\t\t\t\t\tendfor;  \n')
	f1w.write(u'\t\t\t\t\t\tfi;\n')
	f1w.write(u'\t\t\t\t\t\tw:=arclength(subpath(pi,i) of P) /   \n')
	f1w.write(u'\t\t\t\t\t\tarclength(subpath(pi,ni) of P);\n')
	f1w.write(u'\t\t\t\t\t\tlengths[i]:=w[lengths[pi],lengths[ni]];\n')
	f1w.write(u'\t\t\t\t\t\tpi:=i;\n')
	f1w.write(u'\t\t\t\t\tfi;\n')
	f1w.write(u'\t\t\t\telse:\n')
	f1w.write(u'\t\t\t\t\tpi:=i;\n')
	f1w.write(u'\t\t\t\tfi;\n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\t\t%for i=0 upto li: show lengths[i]; endfor;\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tboolean par;\n')
	f1w.write(u'\t\t\tcas := 0.3u;\n')
	f1w.write(u'\t\t\tkrok := 0.7u;\n')
	f1w.write(u'\t\t\tdlzka := (arclength P);\n')
	f1w.write(u'\t\t\tif dlzka>3u: dlzka:=dlzka-0.6u fi;\n')
	f1w.write(u'\t\t\tmojkrok:=adjust_step(dlzka,1.4u) / 5;\n')
	f1w.write(u'\t\t\tpickup PenD;\n')
	f1w.write(u'\t\t\tpar := false;\n')
	f1w.write(u'\t\t\tforever:\n')
	f1w.write(u'\t\t\t\tt := arctime cas of P;\n')
	f1w.write(u'\t\t\t\tif t mod 1>0:  % not a key point\n')
	f1w.write(u'\t\t\t\t\tw := (arclength(subpath(floor t,t) of P) / \n')
	f1w.write(u'\t\t\t\t\tarclength(subpath(floor t,ceiling t) of P));\n')
	f1w.write(u'\t\t\t\t\tif alw_perpendicular:\n')
	f1w.write(u'\t\t\t\t\t\ta := 90;\n')
	f1w.write(u'\t\t\t\t\telse:\n')
	f1w.write(u'\t\t\t\t\t\ta := w[dirs[floor t],dirs[ceiling t]];\n')
	f1w.write(u'\t\t\t\t\tfi;\n')
	f1w.write(u'\t\t\t\t\tl := w[lengths[floor t],lengths[ceiling t]];\n')
	f1w.write(u'\t\t\t\telse:\n')
	f1w.write(u'\t\t\t\t\tif alw_perpendicular:\n')
	f1w.write(u'\t\t\t\t\t\ta := 90;\n')
	f1w.write(u'\t\t\t\t\telse:\n')
	f1w.write(u'\t\t\t\t\t\ta:= dirs[t];\n')
	f1w.write(u'\t\t\t\t\tfi; \n')
	f1w.write(u'\t\t\t\t\tl:=lengths[t];\n')
	f1w.write(u'\t\t\t\tfi;    \n')
	f1w.write(u'\t\t\t\ta := a + angle(thdir(P,t));    \n')
	f1w.write(u'\t\t\t\tthdraw (point t of P) -- \n')
	f1w.write(u'\t\t\t\t((point t of P) + if par: 0.333 * fi l * unitvector(dir(a)));\n')
	f1w.write(u'\t\t\t\tcas := cas + mojkrok;\n')
	f1w.write(u'\t\t\t\tpar := not par;\n')
	f1w.write(u'\t\t\t\texitif cas > dlzka + .3u + (krok / 3);  % for rounding errors\n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\t\tif S = 1: pickup PenC; draw P fi;\n')
	f1w.write(u'\t\t\t\t%pickup pencircle scaled 3pt;\n')
	f1w.write(u'\t\t\t\t%for i=0 upto li: draw point i of P; endfor;\n')
	f1w.write(u'\t\tenddef; \n\n')
	f1w.write(u'\t\t# To change color of Sump\n')
	f1w.write(u'\t\tdef a_sump (expr p) =\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tthfill p withcolor (0.0, 0.0, 0.3);\n')
	f1w.write(u'\t\tenddef;\n\n')
	f1w.write(u'\t\t# To change color of Water area    \n')
	f1w.write(u'\t\tdef a_water (expr p) =\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tthfill p withcolor (0.0, 0.0, 0.1);\n')
	f1w.write(u'\t\tenddef;\n\n')
	f1w.write(u'\t\t# Northarrow more funnier !\n')
	f1w.write(u'\t\tdef s_northarrow (expr rot) =\n')
	f1w.write(u'\t\t\tbegingroup\n')
	f1w.write(u'\t\t\t\tinterim defaultscale:=0.7; % scale your north arrow here\n')
	f1w.write(u'\t\t\t\tT:=identity scaled defaultscale rotated -rot;\n')
	f1w.write(u'\t\t\t\tinterim linecap:=squared;\n')
	f1w.write(u'\t\t\t\tinterim linejoin:=rounded;\n')
	f1w.write(u'\t\t\t\tthfill (-.5cm,-.1cm)--(0,2.5cm)--(.5cm,-.1cm)--cycle;\n')
	f1w.write(u'\t\t\t\tpickup pencircle scaled (0.08cm * defaultscale);\n')
	f1w.write(u'\t\t\t\tthdraw (0,0)--(0,-2.5cm);\n')
	f1w.write(u'\t\t\t\tpickup pencircle scaled (0.16cm * defaultscale);\n')
	f1w.write(u'\t\t\t\tp:=(0.4cm,0.6cm);\n')
	f1w.write(u'\t\t\t\tthdraw ((p--(p yscaled -1)--(p xscaled -1)--(p scaled -1)) shifted (0,-1.0cm));\n')
	f1w.write(u'\t\t\t\tlabel.rt(thTEX("mg") scaled 1.6, (.6cm,-1.6cm)) transformed T;\n')
	f1w.write(u'\t\t\tendgroup;\n')
	f1w.write(u'\t\tenddef; \n\n')
	f1w.write(u'\t\t# Change Scale bar type\n')
	f1w.write(u'\t\tdef s_scalebar (expr l, units, txt) =\n')
	f1w.write(u'\t\t\tbegingroup\n')
	f1w.write(u'\t\t\t\tinterim warningcheck:=0;\n')
	f1w.write(u'\t\t\t\ttmpl:=l / Scale * cm * units / 2;\n')
	f1w.write(u'\t\t\t\ttmpx:=l / Scale * cm * units / 5;\n')
	f1w.write(u'\t\t\t\ttmph:=5bp; % bar height\n')
	f1w.write(u'\t\t\tendgroup;\n')
	f1w.write(u'\t\t\tpickup PenC;\n')
	f1w.write(u'\t\t\tdraw (-tmpl,0)--(tmpl,0)--(tmpl,-tmph)--(-tmpl,-tmph)--cycle;\n')
	f1w.write(u'\t\t\tp:=(0,0)--(tmpx,0)--(tmpx,-tmph)--(0,-tmph)--cycle;\n')
	f1w.write(u'\t\t\tfor i:=-2.5 step 2 until 2:\n')
	f1w.write(u'\t\t\t\tfill p shifted (i * tmpx,0);\n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\t\tbegingroup\n')
	f1w.write(u'\t\t\t\tinterim labeloffset:=3.5bp;\n')
	f1w.write(u'\t\t\t\tfor i:=0 step (l/5) until (l-1):\n')
	f1w.write(u'\t\t\t\t\ttmpx:=tmpl * (i * 2 / l - 1);\n')
	f1w.write(u'\t\t\t\t\tlabel.bot(thTEX(decimal (i)),(tmpx,-tmph));\n')
	f1w.write(u'\t\t\t\tendfor;\n')
	f1w.write(u'\t\t\t\tlabel.bot(thTEX(decimal (l) & "\thinspace" & txt),(tmpl,-tmph));\n')
	f1w.write(u'\t\t\t\t% To write the scale "1:scale"; Comment it ?\n')
	f1w.write(u'\t\t\t\t%label.top(thTEX("Echelle 1 : " & decimal (Scale*100)),(0,0));\n')
	f1w.write(u'\t\t\tendgroup;\n')
	f1w.write(u'\t\tenddef; \n\n')
	f1w.write(u'\t\t# Change the altitude definition\n')
	f1w.write(u'\t\t#     This label requires to specify the position of text relative to point with \n')
	f1w.write(u'\t\t#     help of -align in the options box. \n')
	f1w.write(u'\t\t#     ex: -align bottom-right/top-left/top-right/bottom-left/top/bottom/left/right...\n')
	f1w.write(u'\t\tdef p_altitude (expr pos) =\n')
	f1w.write(u'\t\t\tT:=identity shifted pos;\n')
	f1w.write(u'\t\t\tpickup PenD;\n')
	f1w.write(u'\t\t\tp:=(-.3u,0)--(.3u,0);\n')
	f1w.write(u'\t\t\tthdraw p; thdraw p rotated 90;\n')
	f1w.write(u'\t\t\tp:=fullcircle scaled .2u;\n')
	f1w.write(u'\t\t\tthclean p; thdraw p;\n')
	f1w.write(u'\t\tenddef;\n')
	f1w.write(u'\t\tvardef p_label@#(expr txt,pos,rot,mode) =\n')
	f1w.write(u'\t\t\tif mode=1:\n')
	f1w.write(u'\t\t\t\tthdrawoptions(withcolor .8red + .4blue);\n')
	f1w.write(u'\t\t\t\tp_altitude(pos);\n')
	f1w.write(u'\t\t\t\t% append "m" to label\n')
	f1w.write(u'\t\t\t\tpicture txtm;\n')
	f1w.write(u'\t\t\t\ttxtm:=image(\n')
	f1w.write(u'\t\t\t\t\tdraw txt;\n')
	f1w.write(u'\t\t\t\t\tinterim labeloffset:=0;\n')
	f1w.write(u'\t\t\t\t\tlabel.urt(btex \thaltitude m etex, lrcorner txt);\n')
	f1w.write(u'\t\t\t\t);\n')
	f1w.write(u'\t\t\t\t% give extra offset in case of l/r/t/b alignment\n')
	f1w.write(u'\t\t\t\tpair ctmp;\n')
	f1w.write(u'\t\t\t\tctmp:=center thelabel@#("x", (0,0));\n')
	f1w.write(u'\t\t\t\tif (xpart ctmp * ypart ctmp)=0:\n')
	f1w.write(u'\t\t\t\t\tinterim labeloffset:=(.4u);\n')
	f1w.write(u'\t\t\t\telse: % diagonal alignment\n')
	f1w.write(u'\t\t\t\t\tinterim labeloffset:=(.2u);\n')
	f1w.write(u'\t\t\t\tfi;\n')
	f1w.write(u'\t\t\t\t% draw label\n')
	f1w.write(u'\t\t\t\tlab:=thelabel@#(txtm, pos);\n')
	f1w.write(u'\t\t\t\tdraw lab _thop_; % use color\n')
	f1w.write(u'\t\t\t\tthdrawoptions();\n')
	f1w.write(u'\t\t\t\tbboxmargin:=0.8bp;\n')
	f1w.write(u'\t\t\t\twrite_circ_bbox((bbox lab) smoothed 2);\n')
	f1w.write(u'\t\t\telse:\n')
	f1w.write(u'\t\t\t\tif mode=7: interim labeloffset:=(u/8) fi;\n')
	f1w.write(u'\t\t\t\tlab:=thelabel@#(txt, pos);\n')
	f1w.write(u'\t\t\t\tif mode>1: pickup PenD fi;\n')
	f1w.write(u'\t\t\t\tif mode=2: process_uplabel;\n')
	f1w.write(u'\t\t\t\telseif mode=3: process_downlabel;\n')
	f1w.write(u'\t\t\t\telseif mode=4: process_updownlabel;\n')
	f1w.write(u'\t\t\t\telseif mode=5: process_circledlabel;\n')
	f1w.write(u'\t\t\t\telseif mode=6: process_boxedlabel;\n')
	f1w.write(u'\t\t\t\telseif mode=7: process_label(pos,rot);  % station name\n')
	f1w.write(u'\t\t\t\telseif mode=8: process_filledlabel(pos, rot);\n')
	f1w.write(u'\t\t\t\telse: process_label(pos,rot); fi;\n')
	f1w.write(u'\t\t\tfi;\n')
	f1w.write(u'\t\tenddef;\n\n')
	f1w.write(u'\t\t# For point height with P or C prefixe \n')
	f1w.write(u'\t\t# use “point 0 0 height -value [+10 m]” \n')
	f1w.write(u'\t\t# or “point 0 0 height -value [-85 m]” \n')
	f1w.write(u'\t\t# in your data to get E10 or P85\n')
	f1w.write(u'\t\tverbatimtex \def\thheightpos{E}\def\thheightneg{P} etex \n\n')
	f1w.write(u'\t\t# definition of new lines/symbols\n\n')
	f1w.write(u'\t\t#    Line symbol for strata for cross sections. It works exactly as line section \n')
	f1w.write(u'\t\t#    symbol but you should use -clip off option:\n')
	f1w.write(u'\t\tdef l_u_strata (expr P) =\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tpath Q; Q = punked P;\n')
	f1w.write(u'\t\t\tfor t = 0 upto length P - 1:\n')
	f1w.write(u'\t\t\t\tpair zz[];\n')
	f1w.write(u'\t\t\t\tzz1 := point t of P;\n')
	f1w.write(u'\t\t\t\tzz2 := point t+1 of P;\n')
	f1w.write(u'\t\t\t\tzz3 := postcontrol t of P;\n')
	f1w.write(u'\t\t\t\tzz4 := precontrol t+1 of P;\n')
	f1w.write(u'\t\t\t\tlinecap:=0;\n')
	f1w.write(u'\t\t\t\tif (length(zz3-1/3[zz1,zz2]) > 0.1pt) or (length(zz4-2/3[zz1,zz2]) > 0.1pt):\n')
	f1w.write(u'\t\t\t\t\tzz5 = whatever[zz1,zz2];\n')
	f1w.write(u'\t\t\t\t\t(zz3-zz5) = whatever * (zz1-zz2) rotated 90;\n')
	f1w.write(u'\t\t\t\t\tpickup pencircle scaled 1 mm;\n')
	f1w.write(u'\t\t\t\t\tdraw zz1--zz5 dashed evenly;\n')
	f1w.write(u'\t\t\t\t\tpickup PenA;\n')
	f1w.write(u'\t\t\t\t\tdraw zz1--zz5 withcolor background;\n')
	f1w.write(u'\t\t\t\t\tzz6 = whatever[zz1,zz2];\n')
	f1w.write(u'\t\t\t\t\t(zz4-zz6) = whatever * (zz1-zz2) rotated 90;\n')
	f1w.write(u'\t\t\t\t\tpickup pencircle scaled 1 mm;\n')
	f1w.write(u'\t\t\t\t\tdraw zz2--zz6 dashed evenly;\n')
	f1w.write(u'\t\t\t\t\tpickup PenA;\n')
	f1w.write(u'\t\t\t\t\tdraw zz2--zz6 withcolor background;\n')
	f1w.write(u'\t\t\t\telse:\n')
	f1w.write(u'\t\t\t\t\tpickup pencircle scaled 1 mm;\n')
	f1w.write(u'\t\t\t\t\tdraw zz1--zz2 dashed evenly;\n')
	f1w.write(u'\t\t\t\t\tpickup PenA;\n')
	f1w.write(u'\t\t\t\t\tdraw zz1--zz2 withcolor background;\n')
	f1w.write(u'\t\t\t\tfi;\n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\tenddef;\n\n')
	f1w.write(u'\t\t# Line symbol for fault. It works exactly as line section symbol but you should use -clip off option:\n')
	f1w.write(u'\t\tdef l_u_fault (expr P) =\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tpath Q; Q = punked P;\n')
	f1w.write(u'\t\t\tpickup PenA;\n')
	f1w.write(u'\t\t\tfor t = 0 upto length P - 1:\n')
	f1w.write(u'\t\t\t\tpair zz[];\n')
	f1w.write(u'\t\t\t\tzz1 := point t of P;\n')
	f1w.write(u'\t\t\t\tzz2 := point t+1 of P;\n')
	f1w.write(u'\t\t\t\tzz3 := postcontrol t of P;\n')
	f1w.write(u'\t\t\t\tzz4 := precontrol t+1 of P;\n')
	f1w.write(u'\t\t\t\tif (length(zz3-1/3[zz1,zz2]) > 0.1pt) or (length(zz4-2/3[zz1,zz2]) > 0.1pt):\n')
	f1w.write(u'\t\t\t\t\tzz5 = whatever[zz1,zz2];\n')
	f1w.write(u'\t\t\t\t\t(zz3-zz5) = whatever * (zz1-zz2) rotated 90;\n')
	f1w.write(u'\t\t\t\t\tdraw zz1--zz5 dashed evenly;\n')
	f1w.write(u'\t\t\t\t\tzz6 = whatever[zz1,zz2];\n')
	f1w.write(u'\t\t\t\t\t(zz4-zz6) = whatever * (zz1-zz2) rotated 90;\n')
	f1w.write(u'\t\t\t\t\tdraw zz2--zz6 dashed evenly;\n')
	f1w.write(u'\t\t\t\telse:\n')
	f1w.write(u'\t\t\t\t\tdraw zz1--zz2 dashed evenly;\n')
	f1w.write(u'\t\t\t\tfi;\n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\tenddef;\n\n')
	f1w.write(u'\t\t# code to define a doline\n')
	f1w.write(u'\t\tdef l_u_doline (expr P) =\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tlaenge:= arclength P;\n')
	f1w.write(u'\t\t\tsymsize:=adjust_step(laenge,2u);\n')
	f1w.write(u'\t\t\ttriangle_width:=symsize/10;\n')
	f1w.write(u'\t\t\tcur:=(symsize-triangle_width)/2;\n')
	f1w.write(u'\t\t\tpickup PenC;\n')
	f1w.write(u'\t\t\tforever:\n')
	f1w.write(u'\t\t\t\tt1 := arctime (cur) of P;\n')
	f1w.write(u'\t\t\t\tt  := arctime (cur + triangle_width/2) of P;\n')
	f1w.write(u'\t\t\t\tt2 := arctime (cur + triangle_width) of P;\n')
	f1w.write(u'\t\t\t\tthfill (subpath (t1,t2) of P) -- \n')
	f1w.write(u'\t\t\t\t((point t of P) + symsize/2 * unitvector(thdir(P,t) rotated 90)) -- \n')
	f1w.write(u'\t\t\t\tcycle;\n')
	f1w.write(u'\t\t\t\tthdraw (point t2 of P) --((point t of P) + symsize/2 * unitvector(thdir(P,t) rotated 90)) -- \n')
	f1w.write(u'\t\t\t\t(point t1 of P) withcolor (0.5, 0, 0);\n')
	f1w.write(u'\t\t\t\tcur := cur + symsize;\n')
	f1w.write(u'\t\t\t\texitif cur > laenge - (1*symsize/3); % for rounding errors\n')
	f1w.write(u'\t\t\t\tt1:=arctime (cur) of P;\n')
	f1w.write(u'\t\t\tendfor;\n')
	f1w.write(u'\t\tenddef;\n\n')
	f1w.write(u'\t\t# Modifier l aspect et les données des statistiques de longueur affichees\n')
	f1w.write(u'\t\t#code tex-map\n')
	f1w.write(u'\t\t#	\cavelength{1330\thinspace{}m} \n')
	f1w.write(u'\t\t#	+ 150\thinspace{}m estimes}\n')
	f1w.write(u'\t\t#	\cavedepth{243\thinspace{}m}\n\n')
	f1w.write(u'\tendcode\n\n')
	f1w.write(u'endlayout \n\n\n')
	
	f1w.write(u'#------------------------------\n')
	f1w.write(u'layout layoutmapborder  \n')
	f1w.write(u'# If you want to draw a frame around the map\n')
	f1w.write(u'\tcode tex-map\n')
	f1w.write(u'\t\t\\framethickness=0.5mm\n')
	f1w.write(u'endlayout\n\n\n')

	f1w.write(u'#CODE TO CUSTOMISE ATLAS OUTPUT\n')
	f1w.write(u'#------------------------------\n')
	f1w.write(u'layout LayoutAtlasNorthArrow\n')
	f1w.write(u'#This code is a redefinition of the default atlas definition\n')
	f1w.write(u'#that includes both north arrow & scale bar beside the navigation pane\n\n')
	f1w.write(u'code tex-atlas\n')
	f1w.write(u'\t\def\dopage{%\n')
	f1w.write(u'\t\t\\vbox{\centerline{\\framed{\mapbox}}\n')
	f1w.write(u'\t\t\t\\bigskip\n')
	f1w.write(u'\t\t\t\line{%\n')
	f1w.write(u'\t\t\t\t\\vbox to \ht\\navbox{\n')
	f1w.write(u'\t\t\t\t\t\hbox{\size[20]\the\pagelabel\n')
	f1w.write(u'\t\t\t\t\t\ifpagenumbering\space(\the\pagenum)\\fi\n')
	f1w.write(u'\t\t\t\t\t\space\size[16]\the\pagename}\n')
	f1w.write(u'\t\t\t\t\t\ifpagenumbering\n')
	f1w.write(u'\t\t\t\t\t\t\medskip\n')
	f1w.write(u'\t\t\t\t\t\t\hbox{\qquad\qquad\n')
	f1w.write(u'\t\t\t\t\t\t\\vtop{%\n')
	f1w.write(u'\t\t\t\t\t\t\t\hbox to 0pt{\hss\showpointer\pointerN\hss}\n')
	f1w.write(u'\t\t\t\t\t\t\t\hbox to 0pt{\llap{\showpointer\pointerW\hskip0.7em}%\n')	
	f1w.write(u'\t\t\t\t\t\t\t\\raise1pt\\hbox to 0pt{\\hss$\\updownarrow$\\hss}%\n')
	f1w.write(u'\t\t\t\t\t\t\t\\raise1pt\hbox to 0pt{\hss$\leftrightarrow$\hss}%\n')
	f1w.write(u'\t\t\t\t\t\t\t\\rlap{\hskip0.7em\showpointer\pointerE}}\n')
	f1w.write(u'\t\t\t\t\t\t\t\hbox to 0pt{\hss\showpointer\pointerS\hss}\n')
	f1w.write(u'\t\t\t\t\t\t}\qquad\qquad\n')
	f1w.write(u'\t\t\t\t\t\t\\vtop{\n')
	f1w.write(u'\t\t\t\t\t\t\t\\def\\arr{$\\uparrow$}\n')
	f1w.write(u'\t\t\t\t\t\t\t\showpointerlist\pointerU\n')
	f1w.write(u'\t\t\t\t\t\t\t\def\\arr{$\downarrow$}\n')
	f1w.write(u'\t\t\t\t\t\t\t\showpointerlist\pointerD\n')
	f1w.write(u'\t\t\t\t\t\t}\n')
	f1w.write(u'\t\t\t\t\t}\n')
	f1w.write(u'\t\t\t\t\t\\fi\n')
	f1w.write(u'\t\t\t\t\t\\vss\n')
	f1w.write(u'\t\t\t\t}\n')
	f1w.write(u'\t\t\t\t\hss\n')
	f1w.write(u'\t\t\t\t\\vbox to \ht\\navbox{\n')
	f1w.write(u'\t\t\t\t\t\ifnortharrow\hbox to 0pt{\hss\\northarrow\qquad}\\fi\n')
	f1w.write(u'\t\t\t\t\t\\vss\n')
	f1w.write(u'\t\t\t\t\t\ifscalebar\hbox to 0pt{\hss\scalebar\qquad}\\fi\n')
	f1w.write(u'\t\t\t\t}\n')
	f1w.write(u'\t\t\t\t\\box\\navbox\n')
	f1w.write(u'\t\t\t}\n')
	f1w.write(u'\t\t}\n')
	f1w.write(u'\t}\n\n')
	f1w.write(u'endlayout LayoutAtlasNorthArrow\n\n\n')
	
	f1w.write(u'#------------------------------\n')
	f1w.write(u'layout layoutcontinuation  \n')
	f1w.write(u'\t# If you want to write all the continuations\n')
	f1w.write(u'\tcode metapost\n')
	f1w.write(u'\t\tdef p_continuation(expr pos,theta,sc,al) =\n')
	f1w.write(u'\t\t\t% draw default continuation symbol\n')
	f1w.write(u'\t\t\tp_continuation_UIS(pos,theta,sc,al);\n')
	f1w.write(u'\t\t\t% if text attribute is set\n')
	f1w.write(u'\t\t\tif known(ATTR__text) and picture(ATTR__text):\n')
	f1w.write(u'\t\t\t\t% set labeling color to light orange\n')
	f1w.write(u'\t\t\t\tpush_label_fill_color(1.0, 0.9, 0.8);\n')
	f1w.write(u'\t\t\t\t% draw filled label with text next to ?\n')
	f1w.write(u'\t\t\t\tp_label.urt(ATTR__text,(.5u,-.25u) transformed T,0.0,8);\n')
	f1w.write(u'\t\t\t\t% restore original labeling color\n')
	f1w.write(u'\t\t\t\tpop_label_fill_color;\n')
	f1w.write(u'\t\t\tfi;\n')
	f1w.write(u'\t\tenddef;\n')
	f1w.write(u'\tendcode\n')
	f1w.write(u'endlayout layoutcontinuation\n\n\n')

	f1w.write(u'#------------------------------\n')
	f1w.write(u'layout northarrowMG\n\n')
	f1w.write(u'\tcode metapost\n')
	f1w.write(u'\t\t# If you want to get both, magnetic and geographic north,\n')
	f1w.write(u'\t\t# with \cartodate ?\n')
	f1w.write(u'\t\tdef s_northarrow (expr rot) =\n')
	f1w.write(u'\t\t\t%valscal=1.2; % scale your north arrow here\n')
	f1w.write(u'\t\t\tvalscal=0.7; % scale your north arrow here\n')
	f1w.write(u'\t\t\tdecl:=MagDecl; % set the magnetic declination\n')
	f1w.write(u'\t\t\tT:=identity;\n')
	f1w.write(u'\t\t\tpicture tmp_pic;\n')
	f1w.write(u'\t\t\ttmp_pic = image (\n')
	f1w.write(u'\t\t\t\tpickup pencircle scaled .3;\n')
	f1w.write(u'\t\t\t\tthfill fullcircle scaled 4cm withcolor 1white;\n')
	f1w.write(u'\t\t\t\tthdraw fullcircle scaled 3.1cm;\n')
	f1w.write(u'\t\t\t\tthdraw fullcircle scaled 4.05cm;\n')
	f1w.write(u'\t\t\t\tpickup pencircle scaled .1;\n')
	f1w.write(u'\t\t\t\tthdraw fullcircle scaled 3cm;\n')
	f1w.write(u'\t\t\t\tthdraw fullcircle scaled 4cm;\n')
	f1w.write(u'\t\t\t\tpickup pencircle scaled .2;\n')
	f1w.write(u'\t\t\t\tthdraw (dir(45)*2.025cm)--(dir(45)*3.7cm);\n')
	f1w.write(u'\t\t\t\tthdraw (dir(135)*2.025cm)--(dir(135)*3.7cm);\n')
	f1w.write(u'\t\t\t\tthdraw (dir(225)*2.025cm)--(dir(225)*3.7cm);\n')
	f1w.write(u'\t\t\t\tthdraw (dir(315)*2.025cm)--(dir(315)*3.7cm);\n')
	f1w.write(u'\t\t\t\tpickup pencircle scaled .1;\n')
	f1w.write(u'\t\t\t\tfor whereto=0 step 15 until 345:\n')
	f1w.write(u'\t\t\t\t\tthdraw dir(whereto)*.65cm--dir(whereto)*.9cm;\n')
	f1w.write(u'\t\t\t\t\tthdraw dir(whereto)*1.4cm--dir(whereto)*1.5cm;\n')
	f1w.write(u'\t\t\t\tendfor;\n')
	f1w.write(u'\t\t\t\tfor whereto=0 step 5 until 355:\n')
	f1w.write(u'\t\t\t\t\tthdraw dir(whereto)*.65cm--dir(whereto)*.8cm;\n')
	f1w.write(u'\t\t\t\t\tthdraw dir(whereto)*1.45cm--dir(whereto)*1.5cm;\n')
	f1w.write(u'\t\t\t\tendfor; \n')
	f1w.write(u'\t\t\t\tfor whereto=0 step 1 until 359:\n')
	f1w.write(u'\t\t\t\t\tthdraw dir(whereto)*1.94cm--dir(whereto)*2cm;\n')
	f1w.write(u'\t\t\t\tendfor; \n')
	f1w.write(u'\t\t\t\tpickup pencircle scaled 1;\n')
	f1w.write(u'\t\t\t\tthdraw fullcircle scaled 1cm;\n')
	f1w.write(u'\t\t\t\tthdraw fullcircle scaled 1.1cm;\n')
	f1w.write(u'\t\t\t\tthdraw fullcircle scaled 1.3cm withpen pencircle scaled .3;\n')
	f1w.write(u'\t\t\t\tvald=90-decl;\n')
	f1w.write(u'\t\t\t\ttexrot=0-decl;\n')
	f1w.write(u'\t\t\t\tdrawarrow(dir(vald)*-2cm--dir(vald)*2cm) withpen pencircle scaled .2;\n')
	f1w.write(u'\t\t\t\t% Add the date of the last drawing\n')
	f1w.write(u'\t\t\t\tthdraw image(label.top(btex $mg$ etex, (0,0)) scaled .5 rotated texrot;) shifted (dir(vald)*2.04cm);			\n')
	f1w.write(u'\t\t\t\tthfill (1.06cm,1.06cm)--(0,.2cm)--(-1.06cm,1.06cm)--(-.2cm,0)--(-1.06cm,-1.06cm)--(0,-.2cm)--(1.06cm,-1.06cm)--(.2cm,0)--cycle;\n')
	f1w.write(u'\t\t\t\tthfill (-.2cm,.2cm)--(0,2cm)--(0,0)--cycle;\n')
	f1w.write(u'\t\t\t\tthfill (.2cm,-.2cm)--(0,-2cm)--(0,0)--cycle;\n')
	f1w.write(u'\t\t\t\tthfill (.2cm,.2cm)--(2cm,0)--(0,0)--cycle;\n')
	f1w.write(u'\t\t\t\tthfill (-.2cm,-.2cm)--(-2cm,0)--(0,0)--cycle;\n')
	f1w.write(u'\t\t\t\tthfill (.2cm,.2cm)--(-0,2cm)--(0,0)--cycle withcolor 1white;\n')
	f1w.write(u'\t\t\t\tthfill (.2cm,-.2cm)--(2cm,0)--(0,0)--cycle withcolor 1white;\n')
	f1w.write(u'\t\t\t\tthfill (-.2cm,-.2cm)--(0,-2cm)--(0,0)--cycle withcolor 1white;\n')
	f1w.write(u'\t\t\t\tthfill (-.2cm,.2cm)--(-2cm,0)--(0,0)--cycle withcolor 1white;	\n')		
	f1w.write(u'\t\t\t\tpickup pencircle scaled .2;\n')
	f1w.write(u'\t\t\t\tthdraw (-.2cm,.2cm)--(0,2cm)--(.2cm,.2cm)--(2cm,0cm)--(.2cm,-.2cm)--(0,-2cm)--(-.2cm,-.2cm)--(-2cm,0)--cycle;\n')
	f1w.write(u'\t\t\t\tthfill fullcircle scaled .56cm withcolor 1white;\n')
	f1w.write(u'\t\t\t\tpickup pencircle scaled .1;\n')
	f1w.write(u'\t\t\t\tthdraw (.28cm,0)..(0,.28cm)..(-.28cm,0)..(0,-.28cm)..cycle;\n')
	f1w.write(u'\t\t\t\tpickup pencircle scaled .4;\n')
	f1w.write(u'\t\t\t\tthdraw (.2cm,0)..(0,.2cm)..(-.2cm,0)..(0,-.2cm)..cycle;\n')
	f1w.write(u'\t\t\t\tlabel.bot(btex $N$ etex, (0,2.6cm));\n')
	f1w.write(u'\t\t\t\tlabel.lft(btex $E$ etex, (2.6cm,0));\n')
	f1w.write(u'\t\t\t\tlabel.rt(btex $W$ etex, (-2.6cm,0));\n')
	f1w.write(u'\t\t\t\tlabel.top(btex $S$ etex, (0,-2.6cm));\n')
	f1w.write(u'\t\t\t);\n')
	f1w.write(u'\t\t\tthdraw tmp_pic scaled valscal rotatedaround(origin, -rot);\n')
	f1w.write(u'\t\tenddef;\n')
	f1w.write(u'\tendcode\n')
	f1w.write(u'endlayout northarrowMG\n')
	
	# add your piece of code here and before the closing
	# .
	# .
	# .
		
	# close the config.thc file
	f1w.closed
	
	print(u'\tFile ' + pdata + u' written...')
	
	return

	
def checkfiles(pdata, Errorfiles):
	"""
		Function to check if the file exists
		Raise error if file exists
	"""
	# Check if file exists, if not, raise an error
	if os.path.isfile(pdata) == True :
		if Errorfiles:
			raise NameError(u'ERROR : File {FileNa} does exist'.format(FileNa=str(pdata)))
			#sys.exit('ERROR : File {FileNa} does exist'.format(FileNa=str(pdata)))
		else:
			print(u'WARNING: I have erased file %s' % pdata)


#######
if __name__ == "__main__":

	# build dictionnaries
	dictcave, datac = builddictcave()
	thlang = datac[0]
	thcfile = datac[1]
	thcfnme = datac[2]
	thcpath = datac[3] 
	thconfigfile = datac[4]
	thconfigpath = datac[5]
	thconfigfnme = datac[6]
	icomments = datac[7]
	icoupe = datac[8]
	Errfiles = datac[9]
	
	# check if the files exists
	if thcfnme[-4:] != u'.thc':
		thcfnme = thcfile + u'.thc'
	if  thcpath is not None :
		if thcpath[-1] != u'/':
			thcpath = thcpath + u'/'
		if not Errfiles :
			checkfiles(thcpath + thcfnme)
		else:
			print(u'WARNING: I will erase previous ' + thcpath + thcfnme + u' files !')
	else:
		if not Errfiles :
			checkfiles(thcfnme)
		else:
			print(u'WARNING: I will erase previous ' + thcfnme + u' files !')
	
	if thconfigfnme[-9:] != u'.thconfig':
		thconfigfnme = thconfigfnme + u'.thconfig'
	if thconfigpath is not None :
		if thconfigpath[-1] != u'/':
			thconfigpath = thcpath + u'/'
		if not Errfiles:
			checkfiles(thconfigpath + thconfigfnme)
		else:
			print(u'WARNING: I will erase previous ' + thconfigpath + thconfigfnme + u' files !')
	else:
		if not Errfiles :
			checkfiles(thconfigfnme)	
		else:
			print(u'WARNING: I will erase previous ' + thconfigfnme + u' files !')
	
	# build thc file
	if thcfile :
		if  thcpath is not None :
			writethc(thcpath + thcfnme)
		else:
			writethc(thcfnme)
	
	# build thconfig file
	if thconfigfile :
		# write the file
		if thconfigpath is not None:
			if thcpath is not None:
				writethconfig(thconfigpath + thconfigfnme, icomments, icoupe, thlang,
				              dictcave,
		                      thcfile, thcpath + thcfnme)
			else:
				writethconfig(thconfigpath + thconfigfnme, icomments, icoupe, thlang,
				              dictcave,
		    	              thcfile, thcfnme)
		else:
			if thcpath is not None:
				writethconfig(thconfigfnme, icomments, icoupe, thlang,
				              dictcave,
		                      thcfile, thcpath + thcfnme)
			else:
				writethconfig(thconfigfnme, icomments, icoupe, thlang,
				              dictcave,
		    	              thcfile, thcfnme)

	

# END
