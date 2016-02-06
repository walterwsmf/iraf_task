# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 16:22:13 2016

@author: Walter Martins-Filho
e-mail: walter at on.br
        waltersmartinsf at gmail.com
"""

print 'Data Reduction: Create a masterbias image \n'
print 'Loading Iraf packages .... \n'

from pyraf import iraf #loading iraf package
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
    
#Set original directory
original_path = os.getcwd()
    
#Change your directory to data diretory
os.chdir(data_path)

#list all bias images
bias = glob.glob('bias*.fits')
print 'Loading bias images \nTotal of bias files = ',len(bias),'\nFiles = \n'
print bias
print '\nCreating superbias \n'

#if save_path exist, continue; if not, create.
if not os.path.exists(save_path):
    os.makedirs(save_path)

# copy the files to save_path
os.system('cp bias*.fits '+save_path)
os.system('cp '+bias_list+' '+save_path)

#change to sabe_path
os.chdir(save_path)

#verify if previous superbias exist
if os.path.isfile('superbias.fits') == True:
    os.system('rm superbias.fits')
    
#creating bias list
bias = string.join(bias,',')

#combine the bias image and create the superbias
iraf.imcombine(bias,'superbias.fits')

#print statistics from superbias:
iraf.imstat('superbias.fits')

#clean previos bias files
print '\n Clean bias*.fits images ... \n'
os.system('rm bias*.fits')
print '\n .... done \n'

#Return to original directory
os.chdir(original_path)
