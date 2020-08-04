#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime # Library to convert julian day to dd-mm-yyyy

def getBand(filename):
    bandSetted = False
    bands = ['M6C','M3C'] 
    bandLenghts = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16']
    mode = 0

    while not bandSetted: 
        Band = (filename[filename.find(bands[mode])+3:filename.find("_G16")])
        if (Band not in bandLenghts):    
            mode +=1  
        else:
            bandSetted = True    
    return Band        

def convertDate(filename):
    # Search for the Scan start in the file name
    Start = (filename[filename.find("_s")+2:filename.find("_e")])
    # Converting from julian day to dd-mm-yyyy
    year = int(Start[0:4])
    dayjulian = int(Start[4:7]) - 1 # Subtract 1 because the year starts at "0"
    dayconventional = datetime.datetime(year,1,1) + datetime.timedelta(dayjulian) # Convert from julian to conventional
    date = dayconventional.strftime('%d-%b-%Y') # Format the date according to the strftime directives
    timeScan = Start [7:9] + ":" + Start [9:11] + ":" + Start [11:13] # Time of the Start of the Scan   

    Date_dict = {}
    Date_dict['year'] = year
    Date_dict['day_julian'] = dayjulian
    Date_dict['date_strf'] = date
    Date_dict['time_Scan'] = timeScan
    return Date_dict

