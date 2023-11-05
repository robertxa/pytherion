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
#    -  
###### End To DO #######

from __future__ import  division
# This to be sure that the result of the division of integers is a real, not an integer

# Import modules
import sys
import os
import copy




#from unittest import TestCase

#import funniest

#class TestJoke(TestCase):
#    def test_is_string(self):
#        s = funniest.joke()
#        self.assertTrue(isinstance(s, basestring))





from utils.buildparam import builddictcave
from utils.buildthconfig import *

if __name__ == "__main__":

	# build dictionnaries
	dictcave, data = builddictcave()
	thlang = data[0]
	thcfile = data[1]
	thcfnme = data[2]
	thcpath = data[3] 
	thconfigfile = data[4]
	thconfigpath = data[5]
	thconfigfnme = data[6]
	icomments = data[7]
	icoupe = data[8]
	Errfiles = data[9]
	
	# check if the files exists
	if thcfnme[-4:] != '.thc':
		thcfnme = thcfile + '.thc'
	if  thcpath != None :
		if thcpath[-1] != '/':
			thcpath = thcpath + '/'
		if not Errfiles :
			checkfiles(thcpath + thcfnme)
		else:
			print('WARNING: I will erase previous ' + thcpath + thcfnme +' files !')
	else:
		if not Errfiles :
			checkfiles(thcfnme)
		else:
			print('WARNING: I will erase previous ' + thcfnme +' files !')
	
	if thconfigfnme[-9:] != '.thconfig':
		thconfigfnme = thconfigfnme +'.thconfig'
	if thconfigpath != None :
		if thconfigpath[-1] != '/':
			thconfigpath = thcpath + '/'
		if not Errfiles:
			checkfiles(thconfigpath + thconfigfnme)
		else:
			print('WARNING: I will erase previous ' + thconfigpath + thconfigfnme + ' files !')
	else:
		if not Errfiles :
			checkfiles(thconfigfnme)	
		else:
			print('WARNING: I will erase previous ' + thconfigfnme + ' files !')
	
	# build thc file
	if thcfile :
		if  thcpath != None :
			writethc(thcpath + thcfnme)
		else:
			writethc(thcfnme)
	
	# build thconfig file
	if thconfigfile :
		# write the file
		if thconfigpath != None:
			if thcpath != None:
				writethconfig(thconfigpath + thconfigfnme, icomments, icoupe, thlang,
				              dictcave,
		                      thcfile, thcpath + thcfnme)
			else:
				writethconfig(thconfigpath + thconfigfnme, icomments, icoupe, thlang,
				              dictcave,
		    	              thcfile, thcfnme)
		else:
			if thcpath != None:
				writethconfig(thconfigfnme, icomments, icoupe, thlang,
				              dictcave,
		                      thcfile, thcpath + thcfnme)
			else:
				writethconfig(thconfigfnme, icomments, icoupe, thlang,
				              dictcave,
		    	              thcfile, thcfnme)

	

# END
