# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 21:01:54 2016

@author: Walter Martins-Filho
e-mail: walter at on.br
        waltersmartinsf at gmail.com

#******************************************************************************
Main Goal:
            Obtain the Sideral Time and the Heliocentric Jullian Date from the
            header of the image
#******************************************************************************
"""
print 'Obtain the Sideral Time(ST) and Heliocentric Julian Date(HJD) \n'
print '\nLoading packages ....\n'


#from pyraf import iraf #IRAF
#from login import * #IRAF configurations
from astropy.io import fits #import and export fits images
from astropy.time import Time #control time in fits images
import glob #package for list files
import os #package for control bash commands
import yaml #input data without any trouble
#import string #transform a list in a string of caracters
import useful_functions as use
import numpy as np
from astropy.coordinates import SkyCoord,get_sun,ICRS #get the Sun position from a instant of time
from pandas import DataFrame
#from pandas import HDFStore #save data in a database
print '\n.... Done.'

#******************************************************************************
#**************** BEGIN INPUT PATH FILE ***************************************
#******************************************************************************
#path for your data directory, path for your data save, and names for the lists
#Import with yaml file: input path and prefix information for files
input_file = glob.glob('input*.yaml')
print '\nInput file = ',input_file
original_path = os.getcwd()

if input_file:
    if len(input_file) == 1:
        print '\n reading input file ... \n'
        input_data  =    yaml.load(open(input_file[0])) #creating our dictionary of input variables
        data_path   =    input_data['data_path']
        save_path   =    input_data['save_path']
        planet      =    input_data['exoplanet']
        print '\n....  done! \n'
    if len(input_file) > 1:
        print '\nreading input file ... \n'
        print '\n.... there is more than 1 input*.yaml.\n \nPlease, remove the others files that you do not need. \n'
        raise SystemExit
else:
    print '\nThere is no input*.yaml. \nPlease, create a input file describe in INPUT_PARAMETERS.'
    raise SystemExit
#******************************************************************************
#******************* END INPUT PATH FILE **************************************
#******************************************************************************
print '\nObtain the images .... \n'

print 'Change to ', save_path
os.chdir(save_path) #change to save directory where is our scvience images

images = sorted(glob.glob('AB'+input_data['exoplanet']+'*.fits'))
print '\nImages = \n',images

tempo_loc = [] #time object
SUN = [] #Sun coordinate object
ra_sun, dec_sun, dsun = np.zeros(len(images)),np.zeros(len(images)),np.zeros(len(images)) #sun coordinates
JD = np.zeros(len(images)) #julian date from time object
ST = np.zeros(len(images))
HJD = np.zeros(len(images))
#create the exoplanet object coordianate
exoplanet = SkyCoord(dec=input_data['DEC'],ra=input_data['RA'],unit=('deg','deg'),frame=input_data['frame'])

print '\nObtain data info from header ....\n'
for i in range(len(images)):
    hdr = fits.getheader(images[i])
    UTC = hdr['date-obs']+'T'+hdr['UT'] #string that contain the time in UTC in isot format
    tempo_loc.append(Time(UTC,scale=input_data['scale-time'],format='isot',location=(input_data['lon-obs'],input_data['lat-obs'])))#,input_data['altitude'])))
    JD[i] = tempo_loc[i].jd
    ST[i] = tempo_loc[i].sidereal_time('apparent').hour
    SUN.append(get_sun(tempo_loc[i]))
    ra_sun[i],dec_sun[i] = SUN[i].ra.deg, SUN[i].dec.deg
    dsun[i] = SUN[i].distance.value
    HJD[i] = use.hjd_date(JD[i],dsun[i],dec_sun[i],ra_sun[i],exoplanet.dec.deg,exoplanet.ra.deg,circular_orbit=input_data['circular_orbit'])
    use.update_progress((i+1.)/len(images))
print '\n.... done.\n'

print '\n Time from header = \n'
#print '\nImages ** UTC (YYYY-MM-DDTHH:MM:SS) ** JD (7d.5d) ** ST (hours) ** ST (HH:MM:SS) ** Sun Coordinate (epoch,RA,DEC,Distance) (deg,deg,AU) \n'
ST_string = []
for i in range(len(images)):
    ST1 = int(ST[i])
    ST2 = int((ST[i]-ST1)*60.)
    ST3 = (((ST[i]-ST1)*60.)-ST2)*60
    ST_string.append(str(ST1)+':'+str(ST2)+':'+str(ST3))
    tempo_loc[i] = tempo_loc[i].value
    use.update_progress((i+1.)/len(images))
    #print images[i], ' ** ',tempo_loc[i], ' ** ', JD[i], ' ** ', ST[i],' ** ',ST_string[i],' ** ',sun_loc[i],' ** ',HJD[i]

print '\nSave data file ... \n'
data = DataFrame([images,tempo_loc,list(JD),list(ST),list(ST_string),list(ra_sun),list(dec_sun),list(dsun),list(HJD)]).T
data.columns=['images','UTC','JD','ST','ST_isot','RA_SUN','DEC_SUN','D_SUN','HJD']
print data
data.to_csv('results.csv')

os.chdir(original_path)
