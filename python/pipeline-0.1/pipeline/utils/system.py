'''
Created on Jan 19, 2013

@author: pixo
'''
import itertools
import re
import os

def getRootPath():
    return os.getenv("HK_ROOT")

def getProjectsPath():
    return os.getenv("HK_PROJECTS_PATH")

def getProjectName():
    return os.getenv("HK_PROJECT") 

def extract_number(name):
    # Match the last number in the name and return it as a string,
    # including leading zeroes (that's important for formatting below).
    print name
    result = re.findall(r"\d+", name.split(".")[-2])[0]
    
    return result
    
def collapse_group(group):

    if len(group) == 1:
        return group[0][1]
    
    first = extract_number(group[0][1])
    last = extract_number(group[-1][1])
    length = len(str(int(last)))    
    prefix = re.findall(r"\d+.\w+$", group[0][1])[0]
    ext = prefix.split(".")[-1]
    base = group[0][1].replace(prefix, '').split(os.sep)[-1]

    return "%s####%s[%s-%s]" % (base, ".%s" % ext,
                                first[-length:],last[-length:])

def lsSeq(path):
    lsdir = os.listdir(path)
    lsdir.sort()
    itemDict = dict()
    resultDict = dict()
    
    for fil in lsdir:
        fullpath = os.path.join(path,fil)
        
        if os.path.isfile( fullpath ):
            base = fil.split(".")[0]
            
            if not ( base in itemDict ):
                itemDict[base] = list()
            itemDict[base].append(fullpath)
    
    for key in itemDict :
        groups = [collapse_group(tuple(group)) \
                  for i, group in itertools.groupby(enumerate(itemDict[key]),
                  lambda(index, name):index - int(extract_number(name)))]
        resultDict['\n'.join(map(str, groups))] = itemDict[key]
        
    return resultDict

