'''
Created on Jan 19, 2013

@author: pixo
'''
import itertools, re, os

def getRootPath():
    return os.getenv("HK_ROOT")

def getProjectsPath():
    return os.getenv("HK_PROJECTS_PATH")

def getCCPath():
    return os.path.join(os.getenv( "HK_PIPELINE"), "pipeline","creative")

def getProjectName():
    return os.getenv("HK_PROJECT") 

def extractNumber(name):
    # Match the last number in the name and return it as a string,
    # including leading zeroes (that's important for formatting below).
    return re.findall(r"\d+", name.split(".")[-2])[0]
    
def collapseGroup(group, root = os.sep):

    if len(group) == 1:
        return group[0][1]
    
    if root[-1] != os.sep :
        root = root + os.sep
    
    first = extractNumber(group[0][1])
    last = extractNumber(group[-1][1])
    length = len(str(int(last)))    
    prefix = re.findall(r"\d+.\w+$", group[0][1])[0]
    ext = prefix.split(".")[-1]
    base = group[0][1].replace(prefix, '').split(root)[-1]

    result= "%s####%s[%s-%s]" % (base, ".%s" % ext,
                                first[-length:],last[-length:])
    return result

def lsSeq(path, recursive = True):

    itemDict = dict()
    resultDict = dict()
    
    if recursive :
        for root, subFolders, files in os.walk(path):
            files.sort()
        
            for file in files:
                fullpath = os.path.join(root,file)
                base = fullpath.split(".")[0].replace(path+os.sep,"")
                
                if not ( base in itemDict ):
                    itemDict[base] = list()
                    
                itemDict[base].append(fullpath)    
    else:
        files = os.listdir(path)
        files.sort()
        
        for file in files:
            fullpath = os.path.join(path,file)
            
            if os.path.isfile( fullpath ):
                base = file.split(".")[0]
                
                if not ( base in itemDict ):
                    itemDict[base] = list()
                itemDict[base].append(fullpath)
        
    for key in itemDict :
        groups = [collapseGroup(tuple( group), path ) \
                  for i, group in itertools.groupby(enumerate(itemDict[key]),
                  lambda(index, name):index - int(extractNumber(name)))]
        resultDict['\n'.join(map(str, groups))] = itemDict[key]
        
    return resultDict
