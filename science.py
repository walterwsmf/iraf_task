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
import sys #package for control the system parameters opf python
import yaml #input data without any trouble
import string #transform a list in a string of caracters
print '.... done. \n'

#******************************************************************************
#***************** Usefull functions ******************************************
#******************************************************************************
#BAR Progress function to visualize the progress status:
def update_progress(progress):
    """
    Progress Bar to visualize the status of a procedure
    ___
    INPUT:
    progress: percent of the data

    ___
    Example:
    print ""
    print "progress : 0->1"
    for i in range(100):
        time.sleep(0.1)
        update_progress(i/100.0)
    """
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
#******************************************************************************
#************ END of Usefull functions ****************************************
#******************************************************************************

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
print '\nLoading exoplanet images \nTotal of '+planet+'*.fits  files = ',len(exoplanet),'\nFiles = \n'
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

#create the names for exoplanet science mages with bias subtracted
bexoplanet = []
for i in exoplanet:
    bexoplanet.append('B'+i)
    #verify if previous superbias exist
    if os.path.isfile('B'+i) == True:
        os.system('rm B'+i)

print '\n Will be create this images: \n'
print bexoplanet

#exoplanet = string.join(exoplanet,',') #create the list string of exoplanet science images
#bexoplanet = string.join(bexoplanet,',')#create the list string of bexoplanet science images

print '\nSubtracting superbias.fits from all '+planet+'*.fits images ....\n'
for i in range(len(exoplanet)):
    iraf.imarith(exoplanet[i],'-','superbias.fits',bexoplanet[i])
    update_progress((i+1.)/len(bexoplanet))

print '\n.... cleaning '+planet+'*.fits images\n'
os.system('rm '+planet+'*.fits')

print '\n Statistics of B'+planet+'*.fits images: \n'
for i in range(len(bexoplanet)):
    iraf.imstat(bexoplanet[i])

print '\nFlatfielding the B'+planet+'*.fits ....\n'
#create the names for exoplanet science images with bias subtracted and flatfielding
abexoplanet = []
for i in bexoplanet:
    abexoplanet.append('A'+i)
    #verify if previous superbias exist
    if os.path.isfile('A'+i) == True:
        os.system('rm A'+i)

print '\n Will be create this images: \n'
print abexoplanet
#flatifielding images
for i in range(len(abexoplanet)):
    iraf.imarith(bexoplanet[i],'/','superflat.fits',abexoplanet[i])
    update_progress((i+1.)/len(abexoplanet))

print '\n.... cleaning B'+planet+'*.fits images\n'
os.system('rm B'+planet+'*.fits')

print '\n Statistics of AB'+planet+'*.fits images: \n'
for i in range(len(abexoplanet)):
    iraf.imstat(abexoplanet[i])

#change to save_path
os.chdir(save_path)
