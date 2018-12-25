# Author Pratyush Tewari
# Usage `python3 setToOldestDate.py <dir>`

import os
import sys
from subprocess import Popen, PIPE

absolutepath = ''
fn = sys.argv[1]
if os.path.exists(fn):
    absolutepath = os.path.abspath(fn)
    

def fix_files(absolutepath):
    # r = []    
    for root, dirs, files in os.walk(absolutepath):
        for name in files:
            b = os.path.join(root, name)
            # Change all the times to the oldest time
            output1 = Popen(["exiftool", "-OldestDateTime", "-S", "-s",  str(b)], stdout=PIPE, universal_newlines=True).communicate()[0].strip()
            
            # touch the file to the oldest time
            output = Popen(["exiftool", "-d", "'%Z'" , "-OldestDateTime", "-S", "-s",  str(b)], stdout=PIPE, universal_newlines=True).communicate()[0].strip()

            print (str(b) + " --> " + str(output1) + " --> " + str(output))
        for name in dirs:
            # r.append(" ")
            a = os.path.join(root, name)
            list_files(a)
    # return r
    return

fix_files(absolutepath)
