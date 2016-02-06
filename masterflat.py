# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 19:07:09 2016

@author: Walter Martins-Filho
e-mail: walter at on.br
        waltersmartinsf at gmail.com
"""

print 'Data Reduction: Create a masterflat image \n'
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
        flat_list = file['flat_list']
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
flat = glob.glob('flat*.fits')
print 'Loading flat images \nTotal of flat files = ',len(flat),'\nFiles = \n'
print flat

#if save_path exist, continue; if not, create.
if not os.path.exists(save_path): 
    os.makedirs(save_path)

#create a list of bias images and copy images to save_path
os.system('cp flat*.fits '+save_path)
os.system('cp '+flat_list+' '+save_path)

#creating the names of flat with bias subctracted
bflat = []
for i in flat:
    bflat.append('B'+i)
print '\n Names os flat images with bias subtracted: \n \n',bflat 

#change for save_path directory
os.chdir(save_path)

#verify if previous superbias exist
if os.path.isfile('superflat.fits') == True:
    os.system('rm superflat.fits')
#verify if exits previous bflat*.fits files and remove then.
for i in bflat:
    if os.path.isfile(i) == True:
        os.system('rm '+i)
        
print '\nCreating superflat ... \n'

#create the list of flat images  and bflat images
flat = string.join(flat,',')
bflat = string.join(bflat,',')

print '\n Subtracting bias from flat images and creating bflat images... \n'
#iraf.imarith()
iraf.imarith(flat,'-','superbias.fits',bflat)
#print statistics from bflat*.fits images
iraf.imstat(bflat)
print '\n ...done \n'

print '\n Combining bflat images... \n'
iraf.imcombine(bflat,'superflat.fits')
iraf.imstat('superflat.fits')

#clean previos bias files
os.system('rm flat*.fits')

#Return to original directory
os.chdir(original_path)