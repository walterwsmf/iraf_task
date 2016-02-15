# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 21:37:28 2016

@author: Walter Martins-Filho
e-mail: walter at on.br
        waltersmartinsf at gmail.com
"""

#******************************************************************************
#***************** Usefull functions ******************************************
#******************************************************************************

import sys #package for control the system parameters opf python
import numpy as np

#******************************************************************************
#**************** BEGIN INPUT PATH FILE ***************************************
#******************************************************************************
def inputdata():
    """
    Reading the input file YAML in your directory and return variables of the reduction.
    ___
    INPUT

    this code don't need a input. It search in your directory for a yaml file.

    OUTPUT:
    input_data: dictionary variable with the information in tha input*.yaml file. type: dictionary
    original_path: original directory where you are running this task
    data_path: path for your original data directory, type: string
    save_path: path for your reduction data directory, type: string
    planet: name of the exoplanet in your images, like exoplanet*.fits. type: string
    """
    #import packages
    import glob
    import yaml
    import os
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
    return input_data, original_path, data_path, save_path, planet
#******************************************************************************
#******************* END INPUT PATH FILE **************************************
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

#obtain heliocentric julian date
def hjd_date(JD,distance_sun,declination_sun,right_ascention_sun,declination_obj,right_ascention_obj,circular_orbit=False):
    """
    Return the Heliocentric Julian Date from a given Julian Date]
    ___
    INPUT:
    JD :  Julian Date, type: float
    distance_sun :  distance of observer from the Sun, unit: astronomical unit (AU), type: float
    declination_sun: declination of the Sun from the specific Julian Date input, unit:degrees, type:float
    right_ascention: right ascention of the Sun from the specific Julian Date input, unit:degrees, type:float
    declination_obj: declination of the extrasolar object, unit:degrees, type:float
    right-ascention: right ascention of the extrasolar objet, unit:degrees, type:float
    circular_orbit: boolean value that inform if you assume the Earth orbit is circular. Defult is a elipse orbit. Default value: False

    OUTPUT:
    date_hjd: heliocentric julian date, type:float
    """
    from astropy.constants import c, au
    from astropy import units as u
    from astropy.coordinates import Angle
    #contants
    day = 86400 #seconds
    #Convert degrees in radians and astronomical unit to meters
    declination_sun,right_ascention_sun = Angle(declination_sun *u.deg).rad, Angle(right_ascention_sun *u.deg).rad
    declination_obj,right_ascention_obj = Angle(declination_obj *u.deg).rad, Angle(right_ascention_obj *u.deg).rad
    distance_sun = distance_sun * au.value
    # obtain the heliocentric julian date
    delta_alpha = np.cos(right_ascention_obj - right_ascention_sun)
    delta = (np.sin(declination_sun)*np.sin(declination_obj)) + (np.cos(declination_sun) *np.cos(declination_obj)*delta_alpha)
    if circular_orbit == False:
        corr_seconds = ((distance_sun)/c.value)*delta
    else:
        corr_seconds = ((au.value)/c.value)*delta
    corr_days = corr_seconds/day
    date_hjd = JD - corr_days
    return date_hjd

#obtain the mean time from a given exposure when the exposure is less than 1 min
def delta_exp(exptime, time,date):
    """
    obtain the mean time of the exposure when the exposure is less than 1 minute
    ____
    INPUT:
    EXPTIME: the exposure time from the header of the image, string or float
    time: UT time from the exposure from header
    date: UT date of the exposure from header

    OUTPUT:
    mean_time: mean time of the exposure in isot format (YYYY-MM-DDTHH:MM:SS)
    """
    from string import split
    from numpy import zeros

    time = split(time,':') #split the time in hours, minutes and seconds in each value of a array
    new_time = zeros(len(time)) #create our new time
    new_time[0],new_time[1] = float(time[0]), float(time[1])
    new_time[2] = float(time[2])+float(exptime)/2.

    mean_time = date+'T'+str(int(new_time[0]))+':'+str(int(new_time[1]))+':'+str(new_time[2])

    return mean_time

#obtain the sexagesimal system from a number in float
def sexagesimal_format(number_decimal):
    """
    Return the time or angle number in sexagesimal format.
    ___
    INPUT:
    number_decimal: number in decimal format

    OUTPUT:
    number in sexagesimal format.
    """
    N1 = int(number_decimal)
    N2 = int((number_decimal - N1)*60.)
    N3 = (((number_decimal - N1)*60.) - N2)*60.
    return str(N1)+':'+str(N2)+':'+str(N3)

def yesterday(date_obs):
    """
    Return the previous day of the input.
    ___
    INPUT:
    data in a STRING format like YYYY-MM-DD

    Return:
    previous day in the same format.
    """
    from string import split
    from datetime import datetime, timedelta

    date_obs = split(date_obs,'-')
    new_date_obs = datetime(int(date_obs[0]),int(date_obs[1]),int(date_obs[2])) - timedelta(days=1) #remove 1 day
    if new_date_obs.month < 10:
        month = '0'+str(new_date_obs.month)
    else:
        month = str(new_date_obs.month)
    if new_date_obs.day < 10:
        day = '0'+str(new_date_obs.day)
    else:
        day = str(new_date_obs.day)
    year = str(new_date_obs.year)
    return year+'-'+month+'-'+day

def time_split(time_split):
    """
    Return time in the
    """
    return time
#******************************************************************************
#************ END of Usefull functions ****************************************
#******************************************************************************
