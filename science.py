# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 21:08:38 2016

@author: Walter Martins-Filho
e-mail: walter at on.br
        waltersmartinsf at gmail.com
"""

print 'Data Reduction: Reduce Science images! \n'
print 'Loading Iraf packages .... \n'

from pyraf import iraf
from login import * #loading login.cl parameters for iraf
from ExoSetupTaskParameters import * #loading setup from PyExoDRPL
import glob #package for list files
import os #package for control bash commands
import yaml #input data without any trouble
import string #transform a list in a string of caracters
print '.... done. \n'

#******************************************************************************
#**************** BEGIN INPUT PATH FILE ***************************************
#******************************************************************************
#path for your data directory, path for your data save, and names for the lists
#Import with yaml file: input path and prefix information for files
input_file = glob.glob('input_path*.yaml')
if input_file:
    if len(input_file) == 1:
        print 'reading input file ... \n'
        file = yaml.load(open(input_file[0])) #creating our dictionary of input variables
        data_path = file['data_path']
        save_path = file['save_path']
        planet = file['exoplanet']
        print '....  done! \n'
    if len(input_file) > 1:
        print 'reading input file ... \n'
        print '.... there is more than 1 input_path*.yaml.\n \nPlease, remove the others files that you do not need. \n'
        raise SystemExit
else:
    print 'There is no input_path*.yaml. \nPlease, create a input file describe in INPUT_PARAMETERS.'
    raise SystemExit
#******************************************************************************
#******************* END INPUT PATH FILE **************************************
#******************************************************************************

#set original directory
original_path = os.getcwd()

#Change your directory to data diretory
os.chdir(data_path)

#list all flat images
exoplanet = glob.glob(planet+'*.fits')
print '\nLoading exoplanet images \nTotal of flat files = ',len(exoplanet),'\nFiles = \n'
print exoplanet

#if save_path exist, continue; if not, create.
if not os.path.exists(save_path): 
    os.makedirs(save_path)

#create a list of bias images and copy images to save_path
print '\nCopy science images to save_path directory to main reduction: ....'
os.system('cp '+planet+'*.fits '+save_path)
print '\n .... done. \n'
#change to save_path
os.chdir(save_path)