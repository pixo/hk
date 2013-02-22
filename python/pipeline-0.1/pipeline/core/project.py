'''
Created on Jan 11, 2013

@author: pixo
'''
import os,time
import pipeline.utils as utils

def lsProjects(db, project=""):
    endkey = u"%s\u0fff" % ( project )
    view = db.view("_design/%s/_view/%s" % ("homeworks","project"),
                   startkey=project, endkey=endkey)
    proj_ls = list()
    
    for row in view.rows:
        proj_ls.append(row["value"]["name"])
        print row["value"]["name"]
        
    return proj_ls
    
def createProject( name = "NewProject", description = "Default", overdoc=dict(), 
                   serveradress = "http://admin:admin@127.0.0.1:5984/" ):
    
    assets = utils.getAssetTypes()
    tasks = utils.getTaskTypes()
    
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
    
    db = utils.createDb ( name, serveradress )
    _id, _rev = db.save( doc )
    
    #TODO:add project environment creation
    print "Project %s created" % (name)
    return db   