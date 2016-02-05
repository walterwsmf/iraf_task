# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 12:27:29 2016

@author: walter
"""

#Example code for work with fits image using pyraf modules
from pyraf import iraf #iraf package
import glob #package for list data from your directory
import os #package for control OS and bash commands

def run_imstat(input):
    """
    Call imstatistics for a list of images and show in terminal
    """
    #iraf.images()
    for image in input:
        iraf.imstat(image)

#path for your data directory
data_path = '/home/walter/workspace/exoplanet/data/xo2b/xo2b.b/'
#data_path=input('Input your data path = ')
#print 'Set data path as = '+data_path+'\n'

#******************* Main code ***********************************************
os.chdir(data_path)
list = glob.glob('*.fits')
print list
run_imstat(list)
#****************** END CODE *************************************************