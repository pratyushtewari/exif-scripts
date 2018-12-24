#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Create a KML file based on exif data

Requires exiftool to have been installed    
Usage: exif2kml.py *.jpg > output.kml

"""

import os
import sys
import re
import time
import datetime
import dateutil.parser

def getDateTimeFromISO8601String(s):
    print >> sys.stderr, "getDateTimeFromISO8601String >> ", s.rstrip(), "\n"
    d = dateutil.parser.parse(s)
    print >> sys.stderr, "aftergetDateTimeFromISO8601String >> ", d.rstrip(), "\n"
    return d

def decimalat(DegString):
    # This function requires that the re module is loaded
    # Take a string in the format "34 56.78 N" and return decimal degrees
    SearchStr=r''' *(\d+) deg (\d+)' ([\d\.]+)" (\w)'''
    Result = re.search(SearchStr, DegString)

    # Get the (captured) character groups from the search
    Degrees = float(Result.group(1))
    Minutes = float(Result.group(2))
    Seconds = float(Result.group(3))
    Compass = Result.group(4).upper() # make sure it is capital too

    # Calculate the decimal degrees
    DecimalDegree = Degrees + Minutes/60 + Seconds/(60*60)
    if Compass == 'S' or Compass == 'W':
        DecimalDegree = -DecimalDegree  
    return DecimalDegree

def writePlace(filename,lat,lon,date,altitude,gpsdate):
    PlacemarkString = '''
    <Placemark>
     <name>{0}</name>
     <Point>
      <altitudeMode>absolute</altitudeMode>
      <altitude>{4}</altitude>
      <coordinates>{1}, {2}</coordinates>
      <TimeStamp>
        <when>{3}</when>
      </TimeStamp>
      <gpsDate>{5}</gpsDate>
     </Point>
    </Placemark>'''.format(filename,lat,lon,date, altitude,gpsdate)
    return PlacemarkString 

HeadString='''<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<kml xmlns=\"http://earth.google.com/kml/2.2\">
<Document>'''

if len(sys.argv)<2:
    print >> sys.stderr, __doc__

else:
    placestring = ''
    FList = sys.argv[1:]
    for F in FList:
        ExifData=os.popen('exiftool "'+ F +'" -DateTimeOriginal -GPSLatitude -GPSLongitude -GPSAltitude -MediaCreateDate -CreationDate -FileModificationDateTime').read()
        if "Longitude" in ExifData:
            print >> sys.stderr, F,"\n",ExifData.rstrip()
            Fields = ExifData.split("\n")
            for Items in Fields:
                gpsdate = ""
                GPSAltitude = ""                
                if len(Items)> 10:
                    K,V = Items.split(" : ")
                    if "Latitude" in K:
                        lat = decimalat(V)
                    elif "Longitude" in K:
                        lon = decimalat(V)
                    elif "File Modification Date" in K:
                        date = time.strptime(getDateTimeFromISO8601String(V.strip()),"%Y:%m:%d %H:%M:%S")
                        using = "File Modification Date"
                    elif "Time Original" in K:
                        date = time.strptime(V.strip(),"%Y:%m:%d %H:%M:%S")  # time format
                        using = "Time Original"
                    elif "Creation Date" in K:
                        # is 2018:09:22 08:06:15-06:00
                        # needs 2008-09-03T20:56:35.450686+05:00
                        a = V.strip().split("-")
                        date = time.strptime(a[0],"%Y:%m:%d %H:%M:%S")                        
                        using = "Creation Date"
                    elif "GPS Date" in K:
                        gpsdate = V.strip()
                    elif "GPS Altitude" in K:
                        GPSAltitude = V.strip().replace(" m Above Sea Level", "").replace(" m ", "")
            if lat:
                print >> sys.stderr, F,"\n","using ", using.rstrip()
                TimeFmt = "%Y-%m-%dT%H:%M:%S"
                placestring += writePlace(F,lon,lat,time.strftime(TimeFmt,date),GPSAltitude,gpsdate)
                lat = ''
    # Generate the output file...
    # This just prints to screen -- use > to capture to file...
    print HeadString
    print placestring
    print """</Document>\n</kml>"""