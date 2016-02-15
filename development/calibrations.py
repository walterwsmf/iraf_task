# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 22:23:56 2016

@author: Walter Martins-Filho
e-mail: walter at on.br
        waltersmartinsf at gmail.com
"""
#******************************************************************************
#**************** Loading Pacakges ********************************************
#******************************************************************************
print 'Calibration your science images ....\n'
print 'Loading Iraf packages .... \n'
from pyraf import iraf
from login import * #loading login.cl parameters for iraf
from ExoSetupTaskParameters import * #loading setup from PyExoDRPL
print '.... done. \n'
print 'Loading some python packages ....\n'
import glob #package for list files
import os #package for control bash commands
import sys #package for control the system parameters opf python
import yaml #input data without any trouble
import string #transform a list in a string of caracters
from astropy.io import fits
from astropy.time import Time 
from astropy.coordinates import SkyCoord
from astropy import units as unit
from astropy.coordinates import Angle
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
        RA = file['RA']
        DEC = file['DEC']
        RA_unit = file['u.RA']
        DEC_unit = file['u.DEC']
        frame = file['frame']
        observatory = file['observatory']
        epoch = file['epoch']
        lon_obs = file['lon-obs']
        lat_obs = file['lat-obs']
        print 'Loaded this variables: \n \n',
        print 'data_path = ',data_path
        print 'save_path = ',save_path
        print 'Exoplanet :',planet
        print 'Exoplanet coordinates (RA,DEC,epoch,frame) = ',RA,RA_unit,DEC,DEC_unit,epoch,frame
        print 'Name of the observatory = ',observatory
        print 'Coordinates (lat,lon) = ',lat_obs,lon_obs
        print '\n....  done! \n'
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

#******************************************************************************
#******************* Setting Sideral Time *************************************
#******************************************************************************

#change to save_path directory
print '\nChange to save_path directory: \n'
print save_path
os.chdir(save_path)

#create a time object
images = glob.glob('AB'+planet+'*.fits')
print '\nList of images = \n'
print images

#obtain the sideral time from header data
local_time = []
sideraltime = []
for i in range(len(images)):
    im,hdr = fits.getdata(images[i],header=True)
    tempo = Time(hdr[file['date-obs']]+'T'+hdr[file['time-obs']],format='isot',scale=file['scale-time'])
    local_time.append(tempo)
    sideraltime.append(tempo.sidereal_time('apparent',longitude=file['lon-obs']))

print '\nThis is the list of local time: \n'
print '\nImage ** Local Time (isot format) ** Sideral Time (hours min seg)\n'
for i in range(len(images)):
    print images[i],' ** ',local_time[i],' ** ',sideraltime[i]

print '\nSetting coordinates to our '+planet+': \n'
RA = Angle(file['RA']+file['u.RA'])
DEC = Angle(file['DEC']+file['u.DEC'])
coordinates = SkyCoord(RA,DEC,frame=file['frame'])
print '\nCoordinates: ',coordinates


print '\nIncluding RA,DEC,epoch in the header of the images ....\n'
#RA in hours
for i in range(len(images)):
    iraf.ccdhedit(images[i],'RA',coordinates.ra.hour,type='string')
    iraf.ccdhedit(images[i],'DEC',coordinates.dec.deg,type='string')
    iraf.ccdhedit(images[i],'epoch',file['epoch'],type='string')
    iraf.ccdhedit(images[i],'st',sideraltime[i].hour,type='string')
    update_progress((i+1.)/len(images))
 
print '\nCalibrating your airmass correction: \n'
print 'Setting observatory: ',file['observatory']
iraf.setairmass('AB'+planet+'*.fits')
iraf.setairmass.observatory = file['observatory']
print '\n.... done.\n'

#Setting Julian Date
print '\n Setting Julian Date\n'
iraf.setjd.time = "ut"
iraf.setjd('AB'+planet+'*.fist')
print '\n.... done.\n'