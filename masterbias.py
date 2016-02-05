# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 16:22:13 2016

@author: walter

"""

from pyraf import iraf
from astropy.io import fits
from login import * #loading login.cl parameters for iraf
from ExoSetupTaskParameters import * #loading setup from PyExoDRPL
import glob #package for list files
import os #package for control bash commands

#path for your data directory
data_path = '/home/walter/workspace/exoplanet/data/xo2b/xo2b.b/'
os.chdir(data_path)

#list all bias images
bias = glob.glob('bias*.fits')
print 'Loading bias images \nTotal of bias files = ',len(bias),'\nFiles= \n'
print bias
print '\nCreating superbias \n'

save_path=data_path+'teste_pyraf/'
os.mkdir(save_path)
os.system('ls bias*.fits > bias_list_teste')
iraf.imcombine('@bias_list_teste',save_path+'superbias_teste.fits')

#test: comparing with ExoDRPL output
