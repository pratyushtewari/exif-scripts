# Author Pratyush Tewari
# Usage `python3 setToOldestDate.py <dir>`
# This depends upon the oldest_datetime_config without which this script will not work

import os
import sys
import subprocess
from subprocess import Popen, PIPE
import time

absolutepath = ''

fn = sys.argv[1]
if os.path.exists(fn):
    absolutepath = os.path.abspath(fn)
else:
    print ("The path [" + str(fn) + "] does not exists.") 
    print ("Exiting program!")
    sys.exit()

total = 0

for dirName, subdirList, fileList in os.walk(absolutepath):

    for fname in fileList:
        # ignore all hidden files
        
        if fname.startswith(".") :
            print ("Not Processing " + fname)
            continue

        b = os.path.join(dirName, fname)

        filename = str(b).replace(" ", "\ ").replace("'", "\'")
        # Change all the times to the oldest time
        #exiftool -overwrite_original_in_place "-FileModifyDate<OldestDateTime" "-ModifyDate<OldestDateTime" "-DateTimeOriginal<OldestDateTime" "-CreateDate<OldestDateTime" "-GPSDateTime<OldestDateTime" -S -s FILEorDIR
        command = 'exiftool -overwrite_original "-FileModifyDate<OldestDateTime" "-ModifyDate<OldestDateTime" "-DateTimeOriginal<OldestDateTime" "-CreateDate<OldestDateTime" "-GPSDateTime<OldestDateTime" -S -m -progress -ee ' + ' ' + filename
        subprocess.Popen([command], stdout=PIPE, universal_newlines=True, shell=True)
        
        # get createtime
        command = 'exiftool -d "%Y%m%d%H%M.%S" -OldestDateTime -S -s -ee ' +  filename
        createtime = subprocess.Popen([command], stdout=PIPE, universal_newlines=True, shell=True).communicate()[0].strip()
        
        #get Timezone
        #timezone = Popen(["exiftool", "-d", "%Z" , "-OldestDateTime", "-S", "-s",  str(b)], stdout=PIPE, universal_newlines=True).communicate()[0].strip()
        
        # touch the file to the oldest time
        #subprocess.run(["TZ=" + timezone + " touch -t "+  time + " " + str(b).replace(" ", "\ ")], shell=True, check=True)
        # global total
        total += 1
        command = 'exiftool "-filename<OldestDateTime" -d %Y%m%d_%H%M%S%%-c.%%e -S -m -ee -progress ' + ' ' + filename
        subprocess.Popen([command], stdout=PIPE, universal_newlines=True, shell=True)
        # To print on top of last output, add ",end = '\r'" at the end of the print statement
        print (str(b) + " --> " + " --> " + createtime)
        time.sleep(.1)

print ("")
print ("Total files updated : " + str(total))
