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
#from astropy.io import fits
from login import * #loading login.cl parameters for iraf
from ExoSetupTaskParameters import * #loading setup from PyExoDRPL
import glob #package for list files
import os #package for control bash commands
print '.... done. \n'

#path for your data directory, path for your data save, and names for the lists
data_path = '/home/walter/workspace/exoplanet/data/xo2b/xo2b.b/'
save_path=data_path+'teste_pyraf/'
flat_list = 'flat_list'
original_path = os.getcwd()

#Change your directory to data diretory
os.chdir(data_path)

#list all flat images
flat = glob.glob('flat*.fits')
print 'Loading flat images \nTotal of bias files = ',len(bias),'\nFiles = \n'
print flat
print '\nCreating superflat \n'

#if save_path exist, continue; if not, create.
if not os.path.exists(save_path): 
    os.makedirs(save_path)

#create a list of bias images
os.system('ls flat*.fits > '+flat_list)

#Remove superbias from all flat images
#iraf.imarith('@'+flat_list)