'''
Created on Jan 11, 2013

@author: pixo
'''
import os, time
import badass.utils as utils


class ProjectError (Exception):
    """
    Error raised by the project module.
    
    """
    def __init__ (self, value):
        self.value=value

    def __str__ (self):
        return repr (self.value)


def isProject (db = None):
    """
    This function check if the current Db is contains a homeworks project.

    :param db: The database.
    :type db: couchdb.client.Database
    :returns:  bool -- True if db contains a homeworks project.

    **Example:**
    
    >>> db = badass.utils.getDb ( dbname = "prod" , serveradress = "127.0.0.1:5984" )
    >>> isProject ( db )
    >>> True
    
    """

    # Check if Db contains a Document with the same name
    if not (db.name in db) :
        return False

    dbproj=db [ db.name ]

    # Check if the Document have a type attr
    if not ("type" in dbproj) :
        return False

    doctype=dbproj [ "type" ]

    # Check if the Document is a project type Document
    if doctype=="project":
        return True
    else :
        return False


def getProject (db = None):
    """
    This function return the project Document from DB.

    :param db: The database.
    :type db: couchdb.client.Database
    :returns:  couchdb.client.Document -- Return the project Document.

    **Example:**
    
    >>> db = badass.utils.getDb ( dbname = "prod" , serveradress = "127.0.0.1:5984" )
    >>> getProject ( db )
    >>> <Document 'bls'@'5-97ef4c34350f1c4f5141f05048150bdb' ... >
    
    """

    # Check if the db contains project
    if not (isProject (db)):
        raise ProjectError ("getProject(): Db %s doesn't  contains a project"%db.name)

    # Return the Project Document from db
    return db [ db.name ]


def getProjectUsers (db = None):
    """
    This function return the list of authorised project users.

    :param db: The database.
    :type db: couchdb.client.Database
    :returns:  list -- Return the list of authorised project users.

    **Example:**
    
    >>> db = badass.utils.getDb ( dbname = "prod" , serveradress = "127.0.0.1:5984" )
    >>> getProjectUsers ( db )
    >>> [ 'jdoe', 'mickey', 'pixo' ]
    
    """

    # Check if the db contains project
    if not (isProject (db)):
        raise ProjectError ("getProjectUsers(): Db %s isn't a project"%db.name)

    dbproject=db [ db.name ]

    # Check if the project contains Users
    if not ("users" in dbproject):
        raise ProjectError ("getProjectUsers(): Project %s doesn't contains Users"%db.name)

    # Return the Users list
    return dbproject ["users"]


def lsProjectServer (serveradress):
    """
    This function return a list of all DbServer homeworks projects.

    :param serveradress: The database adress.
    :type serveradress: str
    :returns:  list -- Return the list of authorised project users.

    **Example:**

    >>> lsProjectServer ( serveradress = "admin:pass@127.0.0.1:5984" )
    >>> [ 'prod1', 'prod2', 'prod3' ]
    
    """

    # Get db server from adress
    server=utils.getServer (serveradress)
    projects=list ()
    user=utils.getCurrentUser()

    # Iterate over all databases contained in the DB server
    for db_name in server :
        if not db_name in ("_replicator", "_users"):
            db=server [ db_name ]

            # Check if the current db is a HK project
            if isProject (db) :

                # Get project authorized users
                users=getProjectUsers (db)

                # If current user is in the user list append project in the project list
                if user in users:
                    projects.append (db_name)

    # Return a list of projects name (str)
    return projects


def createProjectEnv (name = "", badassversion = None):
    """
    This function create a project environment file.
    It contains project environment variables related to the project.
    This file is sourced each times a user log to a project via the hk-project command.

    :param name: The project name.
    :type name: str
    :param badassVersion: The asset manager version.
    :type badassVersion: str
    :returns:  str/bool -- If environment file created return the file path else False

    **Example:**

    >>> createProjectEnv ( name = "prod" )
    >>> '/homeworks/projects/prod/config/prod.env'
    
    """

    # Check the project name is
    if (name!=None) and (name==""):
        return False

    if not badassversion:
        badassversion=utils.getBadassVersion()

    # TODO:Create this document with a ui
    env_data="source $HOME/.bashrc\n"
    env_data+="source $HK_ROOT/users/$USER/.hk/$HK_PROJECT\n\n"
    env_data+="#Set environment variables\n"
    env_data+="export HK_DB=$HK_PROJECT\n"
    env_data+="export HK_COAT_VER=4-0-03\n"
    env_data+="export HK_COAT_VER_T=4-0-03\n"
    env_data+="export HK_GUERILLA_VER=0.17.0b12\n"
    env_data+="export HK_GUERILLA_VER_T=0.17.0b12\n"
    env_data+="export HK_HIERO_VER=1.6v1\n"
    env_data+="export HK_HIERO_PLAYER_VER=1.6v1\n"
    env_data+="export HK_HOUDINI_VER=12.5\n"
    env_data+="export HK_MARI_VER=2.0v1\n"
    env_data+="export HK_MARI_VER_T=2.1v1a1\n"
    env_data+="export HK_MAYA_ROOT=/usr/autodesk\n"
    env_data+="export HK_MAYA_VER=2013\n"
    env_data+="export HK_MODO_VER=701\n"
    env_data+="export HK_MUDBOX_VER=2013\n"
    env_data+="export HK_NUKE_VER=7.0v2\n"
    env_data+="export HK_BADASS_VER=%s\n\n"%badassversion
    env_data+="if $HK_DEV_MODE\n"
    env_data+="    then\n"
    env_data+="        hkmode=\"|dev\"\n"
    env_data+="fi\n\n"
    env_data+="alias work='cd $HK_HOME'\n\n"
    env_data+="logpath=\"$HK_USER_REPO\"\n"
    env_data+="export HK_BADASS=\"$HK_CODE_PATH/python/asset-manager/$HK_BADASS_VER\"\n"
    env_data+="export HK_COUCHDB=\"$HK_CODE_PATH/python/couchdb-python\"\n"
    env_data+="export HK_PYSIDE=\"$HK_CODE_PATH/python/pyside\"\n"
    env_data+="argparse=\"$HK_CODE_PATH/python/argparse\"\n"
    env_data+="json=\"$HK_CODE_PATH/python/json\"\n"
    env_data+="export PYTHONPATH=\"$HK_BADASS:$json:$argparse:$PYTHONPATH\"\n\n"
    env_data+="#Set PS1\n"
    env_data+=r"export PS1='\[\033[1;34m\]|\u@\h\[\033[1;37m\]|\t\[\033[1;31m\]|$HK_PROJECT$hkmode>\[\033[0;33m\]\w$ \[\033[00m\]'"+"\n\n"
    env_data+="#Set the current directory\n"
    env_data+="if ! ([ -d $logpath ])\n"
    env_data+="      then\n"
    env_data+="        mkdir -p $logpath\n"
    env_data+="fi\n"

    # Get the project env file
    env_file=utils.getProjectEnv (name)

    if env_file :
        # Create Environment file
        if utils.createFile (env_file, env_data):
            print "createProjectEnv(): %s created "%env_file
            return env_file
        else:
            print "createProjectEnv(): can't create %s "%env_file
            return False
    else:
        print "createProjectEnv(): can't get project env %s "%env_file
        return False


def createProjectCred (name, db_server, host_root):
    """
    This function create a project credential file.
    It contains the project **database server adress** and
    the **host root adress**.

    :param name: The project name.
    :type name: str
    :param db_server: The data base server adress.
    :type db_server: str
    :param host_root: The host server adress root path.
    :type host_root: str
    
    :returns:  str/bool -- If credential file created return the file path else False

    **Example:**

    >>> createProjectCred ( name = 'prod', db_server = 'admin:pass@192.168.0.100:5984', host_root = 'admin@192.168.0.9:/homeworks' )
    >>> '/homeworks/users/jdoe/.hk/prod'
    
    """

    # Create credential file contains
    cred="export HK_DB_SERVER=%s\n"%db_server
    cred+="export HK_HOST_ROOT=%s\n"%host_root

    # Create credential file
    file_cred=os.path.join (os.getenv ("HK_ROOT"), "users", os.getenv ("USER"))
    file_cred=os.path.join (file_cred , ".hk", name)

    # Create the file with the collected credential data
    iscreated=utils.createFile (file_cred, cred, True)

    # Check if the file is created
    if iscreated :

        # Change the permission
        os.chmod (file_cred, 0600)

        # Return the create file credential path (str)
        return file_cred

    else :
        return False

def createProject (name = "", description = "Default", db_server = "",
                      host_root = "", overdoc = dict (), badassversion = None):
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
    :returns:  couchdb.client.Database -- return the db.
    :raises: AttributeError, KeyError

    **Example:**

    >>> createProject ( name = "prod", description = "this is the project prod",
                        db_server = "admin:pass@127.0.0.1:5984", host_root = "admin@127.0.0.1:/homeworks" )
    
    """
    # Check if DB server exists
    adress="http://%s/"%db_server
    exists=utils.serverExists (adress)

    if not exists :
        print "createProject(): Wrong DB server adress,user or/and password"
        return False

    # Check args
    if name=="" :
        print "CreateProject(): Please provide a project name"
        return False

    if db_server=="" or db_server==None :
        print "CreateProject(): No server adress provided"
        return False

    # Check if DB and project already exist
    db=utils.getDb(name, adress)

    # If DB and project exists return
    if db!=False :
        return False

    # Create DB
    db=utils.createDb(name, adress)

    # Create project env and cred file
    createProjectEnv(name, badassversion)
    createProjectCred(name, db_server, host_root)

    # Adding db project documents
    assets=utils.getAssetTypes()
    tasks=utils.getAssetTasks()

    # Users
    users=dict()
    users[utils.getCurrentUser()]="admin"

    doc={
            "_id" : "%s"%name,
            "type" : "project",
            "name" : name,
            "description" : description,
            "asset_types" : assets,
            "asset_tasks" : tasks,
            "creator" : os.getenv ("USER"),
            "created" : time.time(),
            "root" : "/homeworks",
            "users" : users,
            "status": {"art":"ns", "tech":"ns"},
            "host" : host_root
            }

    doc.update(overdoc)

    _id, _rev=db.save(doc)
    print "createProject(): Project '%s' created"%(name)

    return db
