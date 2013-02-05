'''
Created on Jan 11, 2013

@author: pixo
'''
import os,time

def lsProjects(db, project=""):
    endkey = u"%s\u0fff" % ( project )
    view = db.view("_design/%s/_view/%s" % ("homeworks","project"),
                   startkey=project, endkey=endkey)
    proj_ls = list()
    
    for row in view.rows:
        proj_ls.append(row["value"]["name"])
        print row["value"]["name"]
        
    return proj_ls
    
def createProject( db, name = "NewProject", description = "Default", overdoc=dict() ):
    
    proj_ls = lsProjects ( db, name )
    
    if not ( name in proj_ls ):
        doc = {
        "_id": "%s" % name,
        "type": "project",
        "name": name,
        "description" : description,
        #TODO:Task list
        "task":"layout,lighting,render,comp,compout",
        "creator": os.getenv ( "USER" ),
        "created": time.strftime ( "%Y %b %d %H:%M:%S", time.gmtime() )
        }
        doc.update( overdoc )
        _id, _rev = db.save( doc )
        print "Project %r created as Document(%r)" % (name, _id)
        return True
    
    else :
        print "Project %r already exist" % name
        return None
    