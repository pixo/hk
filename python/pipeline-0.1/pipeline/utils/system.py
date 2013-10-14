'''
Created on Jan 19, 2013

@author: pixo
'''
import itertools, re, os

def createFile ( file, content ) :
    
    if os.path.exists ( file ):
        print "createFile (): %s already exists." % file 
        return False
    
    dir = os.path.dirname ( file )

    if not os.path.exists ( dir ) :
        os.makedirs ( dir, 0775 )
    
    else:
        os.chmod ( dir, 0775 )
    
    
    file = open ( file, 'w' )
    file.write ( content )
    file.close ()
    
    return True

def getLocalRoot () :
    return os.getenv ( "HK_ROOT" )

def getHostRoot () :
    return os.getenv ( "HK_HOST_ROOT" )

def getRepo () :
    repo = os.getenv ( "HK_REPO" )
    if repo == None :
        root = getLocalRoot ()
        repo = os.path.join ( root, "projects" )
    return repo

def getProjectEnv ( project = "" ) :
    #Return a path for the project env file
    if project == "" :
        project = getProjectName ()
        
    repo = getRepo ()
    if repo : 
        envfile = os.path.join ( repo, project, "config", project + ".env" )
        return envfile
    else :
        print "getProjectEnv():can't get network repository"
        return False

def getCCPath () :
    return os.path.join ( os.getenv ( "HK_PIPELINE" ), "pipeline", "creative" )

def getProjectName () :
    return os.getenv ( "HK_PROJECT" ) 

def extractNumber ( name ):
    
    try :
        sp = name.split ( "." ) [1]
    
    except IndexError:
        sp = name
        
    result = re.findall ( r"\d+", sp )
    
    if len ( result ) > 0 :
        return result[0]
    
    else:
        return "0"

def collapseGroup(group, root = os.sep):

    if len(group) == 1:
        result = os.path.basename(group[0][1])
        return result
    
    if root[-1] != os.sep :
        root = root + os.sep
    
    part = group[0][1].split(".")
    
    first = extractNumber ( group [0][1] )
    last = extractNumber ( group [-1][1] )
    length = len ( str ( int (last) ) )
    prefix = re.findall ( r"\d+.\w+$", group[0][1] )[0]
    ext = part [-1]
    base = group[0][1].replace ( part[1], "####" )
    base = base.split ( root )[-1]

    result = "%s[%s-%s]" % ( base, first[-length:],last[-length:])
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
        groups = [ collapseGroup ( tuple ( group ), path ) \
                  for i, group in itertools.groupby(enumerate(itemDict[key]),
                  lambda(index, name):index - int(extractNumber(name)))]
        resultDict['\n'.join(map(str, groups))] = itemDict[key]
        
    return resultDict

def rsync ( source = "", destination = "", excludes = list ()  ):
    """rsync in python"""
    
    """Basic update args"""
    update="--progress -rvuh --ignore-existing"
    
    """Excludes args"""    
    exclude = ""
    for i in excludes:
        if type ( i ) == str :
            exclude += "--exclude=%s " % i
    
    exclude = exclude.rstrip()
    
    """Creating rsync command"""    
    cmd = "rsync %s %s %s %s" % ( update, exclude, source, destination )
    return cmd
    