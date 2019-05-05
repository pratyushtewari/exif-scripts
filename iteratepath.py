import os
import sys
absolutepath = ''
fn = sys.argv[1]
if os.path.exists(fn):
    absolutepath = os.path.abspath(fn)
    

def list_files(absolutepath):
    r = []    
    for root, dirs, files in os.walk(absolutepath):
        for name in files:
            b = os.path.join(root, name).replace(" ","\ ")
            print b
            r.append(b)
        for name in dirs:
            r.append(" ")
            a = os.path.join(root, name)
            list_files(a)
    return r

print absolutepath.replace(" ","\ ")
list_files(absolutepath)
# print("\n".join(list_files(absolutepath)))
