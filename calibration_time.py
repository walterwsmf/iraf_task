# -*- coding: utf-8 -*-
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
from string import split #use to unconcanated a string in parts
from pandas import DataFrame, read_csv #work with dataframes
print '\n.... Done.'

#input data
print '\nReading input*.yaml file ....\n'
input_data, original_path, data_path, save_path, planet = use.inputdata()
print '\n.... done.\n'

#change to save data reduction directory
os.chdir(save_path)

print '\n Previous results from info_time task: \n'
results_time = glob.glob('results*.csv')
data_time = read_csv(results_time[0])
#name of the columns in this data_time dataframe
#['images','UTC','JD','ST','ST_isot','RA_SUN','DEC_SUN','D_SUN','HJD']
#print data_time

print '\n Reading the list of images ....\n'
images = sorted(glob.glob('AB'+planet+'*.fits'))
print images

#include de RA,DEC and epoch of the exoplanet
RA,DEC,epoch = input_data['RA'],input_data['DEC'],input_data['epoch']

#obtain ST JD using iraf task and introduce in the header
for i in range(len(images)):
    hdr = fits.getheader(images[i])
    if int(split(hdr['UT'],':')[0]) < int(hdr['timezone']):
        new_date = use.yesterday(hdr['date-obs'])
        #print images[i], new_date
    else:
        new_date = hdr['date-obs']
    year,month,day = split(new_date,'-')
    iraf.asttimes(year=year,month=month,day=day,time=hdr['loctime'],obs=input_data['observatory'])
    JD = iraf.asttimes.jd #obtain julian date
    LMST = iraf.asttimes.lmst #obtain the sideral time
    LMST = use.sexagesimal_format(LMST) #convert sideral time in sexagesimal format
    iraf.hedit(images[i],'ST',LMST,add='yes',verify='no',show='no',update='yes') #create the ST keyword in the header
    iraf.ccdhedit(images[i],'LMST',LMST,type='string') #include the mean sideral time in the header
    iraf.ccdhedit(images[i],'JD',JD,type='string') #include de julian date in the header
    #include RA, and DEC of the object in your header
    iraf.ccdhedit(images[i],"RA",RA,type="string") #include right ascention in the header
    iraf.ccdhedit(images[i],"DEC",DEC,type="string")  #include declination in the header
    iraf.ccdhedit(images[i],"epoch",epoch,type="string") #include epoch in the header
    # use.update_progress((i+1.)/len(images))

print '\n Setting airmass ....\n'
for i in range(len(images)):
    #iraf.hedit(images[i],'airmass',airmass,add='yes')
    #iraf.hedit(images[i],'HJD',HJD,add='yes')
    iraf.setairmass.observatory = input_data['observatory']
    iraf.setairmass(images[i])
    iraf.setjd.time = 'ut'
    iraf.setjd(images[i])
print '\n.... done.\n'

#export information
hjd, jd, airmass, st = [],[],[],[]
for i in range(len(images)):
    hdr = fits.getheader(images[i])
    hjd.append(hdr['HJD'])
    jd.append(hdr['JD'])
    airmass.append(hdr['airmass'])
    st.append(hdr['st'])

#saving the data
data = DataFrame([list(hjd),list(jd),list(st),list(airmass)]).T
data.columns = ['HJD','JD','ST','Airmass']
data.to_csv('results_iraf_calibrations.csv')

#change to workings directory
os.chdir(original_path)
