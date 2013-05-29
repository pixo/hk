'''
Created on Jan 11, 2013

@author: pixo
'''
import os,time
import pipeline.utils as utils

def createProjectEnv ( name = "", dbname = "" ):
    
    if dbname == "":
        dbname = "projects"
        
    env = r"""
source $HOME/.bashrc

#Set environment variables
export HK_DB=%s
HK_DB_USER="admin:admin"
export HK_DB_SERVER="http://$HK_DB_USER@127.0.0.1:5984/"
#export HK_DB_SERVER="https://$HK_DB_USER@homeworks.iriscouch.com"

export HK_COAT_VER=4-BETA12B
export HK_COAT_VER_T=4-BETA12B
export HK_GUERILLA_VER=0.17.0b0
export HK_GUERILLA_VER_T=0.17.0b0
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
pythonpath="$HK_CODE_PATH/python/pipeline-$HK_PIPELINE_VER:$HK_CODE_PATH/python/json"
export PYTHONPATH="$pythonpath:$PYTHONPATH"

#Set PS1
export PS1='\[\033[1;34m\]|\u@\h\[\033[1;37m\]|\t\[\033[1;31m\]|$devmode$HK_PROJECT>\[\033[0;33m\]\w$ \[\033[00m\]'

#Set the current directory
if ! ([ -d $logpath ])
      then
        mkdir -p $logpath
fi
""" % ( dbname )

    file = utils.getProjectEnv ( name )
    
    if file :
        if utils.createFile ( file, env ):
            print "createProjectEnv(): %s created " % file
            return file
        else:
            print "createProjectEnv(): can't create %s " % file
            return False
    else:
        print "createProjectEnv(): can't get project env %s " % file
        return False

def lsProjects(db, project=""):
    endkey = u"%s\u0fff" % ( project )
    design = utils.getDesign ()
    view = db.view("_design/%s/_view/%s" % ( design, "project" ),
                   startkey = project, endkey = endkey )
    proj_ls = list ()
    
    for row in view.rows :
        proj_ls.append ( row ["value"] ["name"] )
        
    return proj_ls
    
def createProject( name = "", description = "Default", serveradress = "",
                   dbname = "projects", overdoc = dict () ):
        
    if name == "" :
        print "CreateProject(): Please provide a project name"
        return False
    
    if serveradress == "" or serveradress == None :
        print "CreateProject(): No server adress provided"
        return False
                
    assets = utils.getAssetTypes ()
    tasks = utils.getTaskTypes ()
    
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
    
    env = createProjectEnv ( name, dbname )
    
    if env :
        db = utils.getDb ( dbname, serveradress )
        
        if not db :
            db = utils.createDb ( dbname, serveradress )
            
        else :
            project = lsProjects ( db, name )
            
            if len ( project ) > 0 :
                print "createProject(): project %s already exist" % name
                return False
            
        _id, _rev = db.save( doc )
        
        print "createProject(): Project '%s' created" % ( name )
        return db
    else :
        return False
