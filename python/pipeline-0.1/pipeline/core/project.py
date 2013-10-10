'''
Created on Jan 11, 2013

@author: pixo
'''
import os,time
import pipeline.utils as utils

def lsProjects ( db, project = "" ):
    endkey = u"%s\u0fff" % ( project )
    design = utils.getDesign ()
    view = db.view("_design/%s/_view/%s" % ( design, "project" ),
                   startkey = project, endkey = endkey )
    proj_ls = list ()
    
    for row in view.rows :
        proj_ls.append ( row ["value"] ["name"] )
        
    return proj_ls

def createProjectEnv ( name = "", dbname = "", db_user = "", db_password  = "",
                         db_host  = "", repo_user  = "", repo_password = "", repo_host = "" ):
    
    if dbname == "":
        dbname = "projects"
        
    env = r"""
source $HOME/.bashrc
source $HK_ROOT/users/$USER/.hk/$HK_PROJECT

#Set environment variables
export HK_DB=%s

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
""" % ( dbname )

    # Get the project env file
    file_env = utils.getProjectEnv ( name )
        
    if file_env :
        if utils.createFile ( file_env, env ):
            print "createProjectEnv(): %s created " % file_env
            return file_env
        else:
            print "createProjectEnv(): can't create %s " % file_env
            return False
    else:
        print "createProjectEnv(): can't get project env %s " % file_env
        return False
    
def createProjectCred ( name, db_server ):
#     Create credential file contains
    cred = """export HK_DB_SERVER=%s""" % ( db_server )
            
#     Create credential file
    file_cred = os.path.join ( os.getenv ( "HK_ROOT" ), "users", os.getenv ( "USER" ) )
    file_cred = os.path.join ( file_cred , ".hk", name  )
    iscreated = utils.createFile ( file_cred, cred )
    
    if iscreated:
        os.chmod ( file_cred, 600 )
        return True
    
    else:
        return False
    
def createProject ( name = "", description = "Default", db_server = "",
                      db_name = "projects", overdoc = dict () ):

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
    
    #Create DB, project env and cred file                    
    db = utils.getDb ( db_name, adress )        
    if db == False :
        db = utils.createDb ( db_name, adress )
        createProjectEnv ( name, db_name )
        createProjectCred ( name, db_server )
        
    else :
        project = lsProjects ( db, name )    
        if len ( project ) > 0 :
            print "createProject(): project %s already exist" % name
            return False
    
    #Adding db project documents    
    assets = utils.getAssetTypes ()
    tasks = utils.getAssetTasks ()
    
    doc = {
            "_id": "%s" % name,
            "type": "project",
            "name": name,
            "description" : description,
            "assets_type": assets,
            "tasks_type": tasks,
            "creator": os.getenv ( "USER" ),
            "created": time.strftime ( "%Y %b %d %H:%M:%S", time.localtime() )
            }
    
    doc.update( overdoc )
    
    _id, _rev = db.save( doc )
    print "createProject(): Project '%s' created" % ( name )
    return db

