"""
Created on Sun Feb 14 21:01:54 2016

@author: Walter Martins-Filho
e-mail: walter at on.br
        waltersmartinsf at gmail.com
"""
#******************************************************************************
#Main Goal: include the time_info in the header of the images.
#******************************************************************************

print '\n Including time information in the header \n'
print '\n Loading packages .... \n'

from pyraf import iraf #IRAF
from login import * #IRAF configurations
from astropy.io import fits #import and export fits images
import glob #package for list files
import os #package for control bash commands
import useful_functions as use #useful functions
import yaml #input data without any trouble
from string import split #use to unconcanated a string in parts
from pandas import DataFrame, read_csv #work with dataframes
from photutils import CircularAperture #Photometry routines
print '\n.... Done.'

#input data
print '\nReading input*.yaml file ....\n'
#******************************************************************************
#**************** BEGIN INPUT PATH FILE ***************************************
#******************************************************************************
#path for your data directory, path for your data save, and names for the lists
#Import with yaml file: input path and prefix information for files
input_file = glob.glob('input*.yaml')
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


print 'YAML information:'
input_file = file
print input_file

#set original directory
original_path = os.getcwd()

#Change your directory to save diretory
os.chdir(save_path)

##list all  science AB images
exoplanet = glob.glob('AB'+planet+'*.fits')
print '\nLoading exoplanet images \nTotal of '+planet+'*.fits  files = ',len(exoplanet),'\nFiles = \n'
print exoplanet



os.chdir(original_path)
