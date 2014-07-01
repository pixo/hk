'''
Created on Jan 19, 2013

@author: pixo
'''
import itertools, re, os, hashlib, time


def hashTime () :
    """
    This function return a hash based on sha1 current time.
    Useful to get a random value. 
    
    :returns:  str -- Return the current time 'sha1' hash.
    
    >>> random_value = hashTime ()
    >>> 'a8f2aa40f66a763dde036f83e854d1762436e97d'
    
    """
    
    # Get the hash from current time
    sha1 = hashlib.sha1 ( str ( time.time () ) )
    return str ( sha1.hexdigest () )

def hashFile ( path = "" ) :
    """
    This function compare the two files contains, based on sha1.
    It is very useful if you need to know if the two file are the same.

    :param path: The file path
    :type path: str
    :returns:  str -- sha1 hash file
    :raises: RepositoryError if the path doesn't exists.

    **Example:**
    
    >>> hashFile ( path = "/home/user/filea" )
    >>> 'a8f2aa40f66a763dde036f83e854d1762436e97d'
    
    """
    
    #Check if the file exists
    if os.path.exists ( path ):
        raise Exception ( "Can't compare '%s', file doesn't exists." % path )
    
    # Get the sha1lib
    sha1 = hashlib.sha1 ()
    
    # Get the file for read
    f = open ( path, 'rb' )
     
    # Try to get the hash
    try:
        sha1.update ( f.read () )    
    finally:
        f.close ()
    
    # return the hash
    return sha1.hexdigest ()
     
def compareFile ( file_a = "", file_b = "" ):
    """
    This function compare two files contains based on sha1.
    It is very useful if you need to know if two files are the same.

    :param file_a: The first file path
    :type file_a: str
    :param file_b: The second file path
    :type file_b: str
    :returns:  bool -- True if file are the same.
    :raises: RepositoryError if one of the file doesn't exists.

    **Example:**
    
    >>> compareFile ( file_a = "/home/user/filea", file_b = "/home/user/fileb" )
    >>> True
    
    """
    
    #Check if the file_a exists
    if os.path.exists ( file_a ):
        raise Exception ( "Can't compare '%s', file doesn't exists." % file_a )
    
    #Check if the file_b exists
    if not os.path.exists ( file_b ):
        raise Exception ( "Can't compare '%s', file doesn't exists." % file_b )
         
    #Compare the sha1 hash of the files
    if hashFile ( file_a ) == hashFile ( file_b ):
        # if the file are the same return True
        return True
    else :
        # if they are not the same return False
        return False

def createFile ( path ="", content = "", overwrite = False) :
    
    if os.path.exists ( path ) and (not overwrite):
        print "createFile (): %s already exists." % path 
        return False
    
    dirnam = os.path.dirname ( path )

    if not os.path.exists ( dirnam ) :
        os.makedirs ( dirnam, 0775 )
    
    else:
        os.chmod ( dirnam, 0775 )
    
    path = open ( path, 'w' )
    path.write ( content )
    path.close ()
    
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
    return os.path.join ( os.getenv ( "HK_BADASS" ), "badass", "creative" )

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

def lsSeq(path, recursive = True):
    #Collapse Group functions
    def collapseGroup ( group, root = os.sep ):
    
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

    itemDict = dict()
    resultDict = dict()
    
    if recursive :
        for root, subFolders, files in os.walk(path):
            files.sort()
        
            for fil in files:
                fullpath = os.path.join(root,fil)
                base = fullpath.split(".")[0].replace(path+os.sep,"")
                
                if not ( base in itemDict ):
                    itemDict[base] = list()
                    
                itemDict[base].append(fullpath)    
    
    else:
        files = os.listdir(path)
        files.sort()
        
        for fil in files:
            fullpath = os.path.join(path,fil)
            
            if os.path.isfile( fullpath ):
                base = fil.split(".")[0]
                
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
    """ rsync in python """
    
    """ Basic update args """
    update="--progress -rvuh --ignore-existing"
    
    """ Excludes args """
    exclude = ""
    for i in excludes:
        if type ( i ) == str :
            exclude += "--exclude=%s " % i
    
    exclude = exclude.rstrip()
    
    """ Creating rsync command """    
    cmd = "rsync %s %s %s %s" % ( update, exclude, source, destination )
    os.system ( cmd )
    
    return cmd
    