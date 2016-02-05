# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 16:22:13 2016

@author: Walter Martins-Filho
e-mail: walter at on.br
        waltersmartinsf at gmail.com
"""

print 'Data Reduction: Create a masterbias image \n'
print 'Loading Iraf packages .... \n'
from pyraf import iraf
from astropy.io import fits
from login import * #loading login.cl parameters for iraf
from ExoSetupTaskParameters import * #loading setup from PyExoDRPL
import glob #package for list files
import os #package for control bash commands
print '.... done. \n'

#path for your data directory, path for your data save, and names for the lists
data_path = '/home/walter/workspace/exoplanet/data/xo2b/xo2b.b/'
save_path=data_path+'teste_pyraf/'
bias_list = 'bias_list'
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

#create a list of bias images
os.system('ls bias*.fits > '+bias_list)

#combine the bias image and create the superbias
iraf.imcombine('@'+bias_list,save_path+'superbias.fits')

#Return to original directory
os.chdir(original_path)
