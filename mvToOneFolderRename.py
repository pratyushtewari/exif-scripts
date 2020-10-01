# script to move all the files from mentioned folder to the finalfolder. It does not move the subfolders for now
# which is safer
# usage : python3 mvRname.py folder1 folder2 folder3 folder4 ... finalFolder
# Author: Pratyush Tewari (tewari.pratyush@gmail.com)

import sys, os
from os import walk
import time

def show_options(exitval):
    "Show the options and exit."
    print('USAGE: %s directories ... [destination directory]' % sys.argv[0])
    sys.exit(exitval)

#
# Parse arguments
#
if len(sys.argv) < 3:
    show_options(-1)
dst_dir = sys.argv[-1] # last argument
dirs = sys.argv[1:-1] # all the other argument but last. argc[0] is the command it self
if not os.path.isdir(dst_dir):
    print('%s is not a directory.' % dst_dir)
    show_options(-2)
for dir in dirs:
    if not os.path.exists(dir):
        print('%s does not exist.' % dir)
        show_options(-3)
# print(dst_dir)
# print(dirs)
countofFiles = 0
#
# Move files from the dirs into the dst_dir
#
for dir in dirs:
  f = []
  for (dirpath, dirnames, filenames) in walk(dir):
    # f.extend(filenames)
    for file in filenames:
      basename = os.path.basename(file)
      if basename == ".DS_Store":
        continue
      # print basename
      head, tail = os.path.splitext(basename)
      dst_file = os.path.join(dst_dir, basename)
      # rename if necessary
      count = 0
      while os.path.exists(dst_file):
          count += 1
          dst_file = os.path.join(dst_dir, '%s-%d%s' % (head, count, tail))
     
      fromfile = os.path.join(dirpath, file)
      tofile = os.path.abspath(dst_file)
      # print('Renaming %s to %s' % (fromfile, tofile))
      countofFiles += 1
      os.rename(fromfile, tofile)
      print("Moved %s files." % countofFiles, end='\r')
print('Done: Moved %s files' % countofFiles)
