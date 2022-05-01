# script to rename all the folders like "FolderName (YYYY) [BluRay] [1080p] [Webrip]"
# to 'YYYY - FolderName'
# and all its content to 'YYYY - FolderName.Originalextension'
# usage : python3 YTSrename.py folderpath
# Author: Pratyush Tewari (tewari.pratyush@gmail.com)

import sys, os
from os import walk
import time
import re

def show_options(exitval):
    "Show the options and exit."
    print('USAGE: %s directory' % sys.argv[0])
    sys.exit(exitval)

#
# Parse arguments
#
if len(sys.argv) < 2:
    show_options(-1)
dir = sys.argv[-1] # last argument
if not os.path.exists(dir):
  print('%s does not exist.' % dir)
  show_options(-1)
countofFiles = 0

for (dirpath, dirnames, filenames) in walk(dir):
  dirparent = os.path.dirname(dirpath)
  dirname = os.path.basename(dirpath)
  # remove the format text
  cleandirname = re.sub("\[BluRay\]|\[[0-9]*p\]|\[YTS.*\]|\[Webrip\]|\[WEBRip.x265-RARBG\]|\[2160p\]|\[x265\]|\[10bit\]|\[AAC5\]|\[4K\]", "", dirname, flags=re.I).strip()
  nameAndYear = cleandirname.rsplit('(',1)
  newdirpath = dirpath # will be updated in next line
  newdirName = dirname # will be update in next line
  # check if the dirname has (YYYY)
  if len(nameAndYear) == 2:
    base = nameAndYear[0]
    year = nameAndYear[1].rsplit(')',1)[0]
    finalName = year + ' - ' + base.strip()
    # replace multiple spaces to single space
    newdirName = ' '.join(finalName.split())
    newdirpath = os.path.join(dirparent, newdirName)

    print(" >> dir: ")
    print("oldPath -> %s" % dirpath)
    print("newdirpath -> %s" % newdirpath)
    print("")
    os.rename(dirpath, newdirpath)

  for file in filenames:
    basename = os.path.basename(file)
    if basename == ".DS_Store":
      continue
    extension = basename.rsplit('.',1)
    newfilename = newdirName + '.' + extension[1]
    oldFilePath = os.path.join(newdirpath, file)
    newFilePath = os.path.join(newdirpath, newfilename)
    
    if basename.lower().endswith(".jpg"):
      print(" Deleted >> " + oldFilePath)
      os.remove(oldFilePath)
      continue

    if basename.lower().endswith(".txt"):
      print(" Deleted >> " + oldFilePath)
      os.remove(oldFilePath)
      continue

    # check if the newfilename already exists, in that case increment the file name
    count = 0
    while os.path.exists(newFilePath):
      print(" >> AIYYYYOOO ")
      count += 1
      newfilename = newdirName + "-" + str(count) + '.' + extension[1]
      newFilePath = os.path.join(newdirpath, newfilename)

    print(" >> Files: ")
    print("file -> %s" % file)
    print("oldPath -> %s" % oldFilePath)
    print("newPath -> %s" % newFilePath)
    print("")
    os.rename(oldFilePath, newFilePath)
