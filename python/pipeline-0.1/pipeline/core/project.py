'''
Created on Jan 11, 2013

@author: pixo
'''
import os,time
import pipeline.utils as utils

class ProjectError ( Exception ):
    """
    Error raised by the project module.
    
    """
    def __init__ ( self, value ):
        self.value = value
    def __str__ ( self ):
        return repr ( self.value )
    
def isProject ( db = None):
    """
    This function check if the current Db is contains a homeworks project.

    :param db: The database.
    :type db: couchdb.client.Database
    :returns:  bool -- True if db contains a homeworks project.

    **Example:**
    
    >>> db = pipeline.utils.getDb ( dbname = "prod" , serveradress = "127.0.0.1:5984" )
    >>> isProject ( db )
    >>> True
    
    """
    
    # Check if Db contains a Document with the same name
    if not ( db.name in db ) :
        return False
    
    dbproj = db [ db.name ]
    
    # Check if the Document have a type attr
    if not ( "type" in dbproj ) :
        return False
    
    doctype = dbproj [ "type" ]
    
    # Check if the Document is a project type Document
    if doctype == "project":
        return True
    else :
        return False
    
def getProject ( db = None ):
    """
    This function return the project Document from DB.

    :param db: The database.
    :type db: couchdb.client.Database
    :returns:  couchdb.client.Document -- Return the project Document.

    **Example:**
    
    >>> db = pipeline.utils.getDb ( dbname = "prod" , serveradress = "127.0.0.1:5984" )
    >>> getProject ( db )
    >>> <Document 'bls'@'5-97ef4c34350f1c4f5141f05048150bdb' ... >
    
    """
    
    # Check if the db contains project 
    if not ( isProject ( db ) ): 
        raise ProjectError ( "getProject(): Db %s doesn't  contains a project" % db.name )
    
    return db [ db.name ]
    
def getProjectUsers ( db = None ):    
    """
    This function return the list of authorised project users.

    :param db: The database.
    :type db: couchdb.client.Database
    :returns:  list -- Return the list of authorised project users.

    **Example:**
    
    >>> db = pipeline.utils.getDb ( dbname = "prod" , serveradress = "127.0.0.1:5984" )
    >>> getProjectUsers ( db )
    >>> [ 'jdoe', 'mickey', 'pixo' ]
    
    """
    
    # Check if the db contains project 
    if not ( isProject ( db ) ): 
        raise ProjectError ( "getProjectUsers(): Db %s isn't a project" % db.name )
    
    dbproject = db [ db.name ]
    
    # Check if the project contains Users 
    if not ( "users" in dbproject ): 
        raise ProjectError ( "getProjectUsers(): Project %s doesn't contains Users" % db.name )
    
    # Return the Users list
    return dbproject ["users"]

def lsProjectServer ( serveradress ):
    """
    This function return a list of all homeworks projects on the DbServer.

    :param serveradress: The database.
    :type serveradress: couchdb.client.Database
    :returns:  list -- Return the list of authorised project users.

    **Example:**

    >>> getProjectUsers ( serveradress = "admin:pass@127.0.0.1:5984" )
    >>> [ 'hkprod1', 'hkprod2', 'hkprod3' ]
    
    """
    
    server = utils.getServer ( serveradress )
    projects = list ()
    user = os.getenv ( "USER" )
        
    for db_name in server :
        db = server [ db_name ]
                
        if isProject ( db ) :
            users = getProjectUsers ( db )
            
            if user in users:
                projects.append ( db_name )
        
    return projects


def createProjectEnv ( name = "" ):
    if name == "" :
        return False

# TODO:Create this document with a ui
    env_data = r"""source $HOME/.bashrc
source $HK_ROOT/users/$USER/.hk/$HK_PROJECT

#Set environment variables
export HK_DB=$HK_PROJECT

export HK_COAT_VER=4-0-03
export HK_COAT_VER_T=4-0-03
export HK_GUERILLA_VER=0.17.0b12
export HK_GUERILLA_VER_T=0.17.0b12
export HK_HIERO_VER=1.6v1
export HK_HIERO_PLAYER_VER=1.6v1
export HK_HOUDINI_VER=12.5
export HK_MARI_VER=2.0v1
export HK_MARI_VER_T=2.1v1a1
export HK_MAYA_VER=2013
export HK_MAYA_ROOT="/usr/autodesk"
export HK_MODO_VER=701
export HK_MUDBOX_VER=2013
export HK_NUKE_VER=7.0v2
export HK_PIPELINE_VER=0.1

if $HK_DEV_MODE
    then
        devmode="DEV-"
fi

alias ~~='cd $HK_HOME'

logpath="$HK_USER_REPO"
export HK_PIPELINE="$HK_CODE_PATH/python/pipeline-$HK_PIPELINE_VER"
export HK_COUCHDB="$HK_CODE_PATH/python/couchdb-python"
export HK_PYSIDE="$HK_CODE_PATH/python/pyside"
argparse="$HK_CODE_PATH/python/argparse"
json="$HK_CODE_PATH/python/json"
export PYTHONPATH="$HK_PIPELINE:$json:$argparse:$PYTHONPATH"

#Set PS1
export PS1='\[\033[1;34m\]|\u@\h\[\033[1;37m\]|\t\[\033[1;31m\]|$devmode$HK_PROJECT>\[\033[0;33m\]\w$ \[\033[00m\]'

#Set the current directory
if ! ([ -d $logpath ])
      then
        mkdir -p $logpath
fi
"""

    # Get the project env file
    env_file = utils.getProjectEnv ( name )
        
    if env_file :
        if utils.createFile ( env_file, env_data ):
            print "createProjectEnv(): %s created " % env_file
            return env_file
        else:
            print "createProjectEnv(): can't create %s " % env_file
            return False
    else:
        print "createProjectEnv(): can't get project env %s " % env_file
        return False
    
def createProjectCred ( name, db_server, host_root ):
#     Create credential file contains
    cred = "export HK_DB_SERVER=%s\n" % db_server
    cred += "export HK_HOST_ROOT=%s\n" % host_root
            
#     Create credential file
    file_cred = os.path.join ( os.getenv ( "HK_ROOT" ), "users", os.getenv ( "USER" ) )
    file_cred = os.path.join ( file_cred , ".hk", name  )
    
    iscreated = utils.createFile ( file_cred, cred, True )
    
    if iscreated:
        os.chmod ( file_cred, 0600 )
        return True
    
    else:
        return False
    
def createProject ( name = "", description = "Default", db_server = "",
                      host_root = "", overdoc = dict () ):
    """
    This function create a project.

    :param name: The project name
    :type name: str
    :param description: The project description
    :type description: str
    :param db_server: The data base adress
    :type db_server: str
    :param host_root: The host data server root adress  
    :type host_root: str
    :param overdoc: A dictionnary that contains extra document attributes.
    :type overdoc: dict
    :returns:  db document -- db document.
    :raises: AttributeError, KeyError

    **Example:**

    >>> createProject ( name = "prod", description = "this is the project prod",
                        db_server = "admin:pass@127.0.0.1:5984", host_root = "admin@127.0.0.1:/homeworks" )
    
    """
    
    #Check if DB server exists
    adress = "http://%s/" % db_server
    exists = utils.serverExists ( adress )
    
    if not exists :
        print "createProject(): Wrong DB server adress,user or/and password"
        return False
    
    #Check args
    if name == "" :
        print "CreateProject(): Please provide a project name"
        return False
    
    if db_server == "" or db_server == None :
        print "CreateProject(): No server adress provided"
        return False
    
    #Check if DB and project already exist
    db = utils.getDb ( name, adress )
        
    #If DB and project exists return                 
    if db != False :
        return False
        
    #Create DB
    db = utils.createDb ( name, adress )
        
    #Create project env and cred file
    createProjectEnv ( name )
    createProjectCred ( name, db_server, host_root )    
    
    #Adding db project documents    
    assets = utils.getAssetTypes ()
    tasks = utils.getAssetTasks ()
    
    doc = {
            "_id" : "%s" % name,
            "type" : "project",
            "name" : name,
            "description" : description,
            "assets_type" : assets,
            "tasks_type" : tasks,
            "creator" : os.getenv ( "USER" ),
            "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.localtime() ),
            "root" : "/homeworks",
            "users" : list ( [ os.getenv ( "USER" ) ] ),
            "host" : host_root
            }
    
    doc.update( overdoc )
    
    _id, _rev = db.save( doc )
    print "createProject(): Project '%s' created" % ( name )
    return db
