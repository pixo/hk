'''
Created on Jan 11, 2013

@author: pixo
'''
import os,time
import pipeline.utils as utils

def lsDbProjects ( db, project = "" ):
    endkey = u"%s\u0fff" % ( project )
    design = "_design/" + utils.getDesign ()
    proj_ls = list ()
    
    if design in db :
        view = db.view("%s/_view/%s" % ( design, "project" ),
                       startkey = project, endkey = endkey )
        
        for row in view.rows :
            proj_ls.append ( row ["value"] ["name"] )
        
    return proj_ls

def lsServerProjects ( serveradress ):
    server = utils.getServer ( serveradress )
    projects = list ()
    user = os.getenv ( "USER" )
        
    for db_name in server :
        db = server [ db_name ]
        project_ls = lsDbProjects ( db )
        
        if len ( project_ls ) > 0 :
            for proj in project_ls :
                users = db [ proj ]["users"]
                
                if db_name == proj and ( user in users ) :
                    projects.append ( proj )
        
    return projects

def createProjectEnv ( name = "" ):
    
    if name == "" :
        return False
        
    env = r"""source $HOME/.bashrc
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

