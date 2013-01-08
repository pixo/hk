'''
Created on Jan 6, 2013

@author: pixo
'''
import os,time

def lsProjects(db, project=""):
    startkey = u"%s" % ( project )
    endkey = u"%s\u0fff" % ( project )
    view = db.view("_design/%s/_view/projectsByName" % "cg_project", startkey=startkey, endkey=endkey)
    projs = list()
    
    for row in view.rows:
        projs.append(row["value"]["name"])
        print row["value"]["name"]
        
    return projs
    
def createProject(name,db):
    projlist=lsProjects(db, name)
    
    if not (name in projlist):
        doc = {
        "_id": "%s" % name,
        "type": "project",
        "name": name,
        "shot_task":"layout,lighting,render,comp,compout",
        "creator": os.getenv("USER"),
        "created": time.strftime("%Y %b %d %H:%M:%S", time.gmtime())
        }
        _id, _rev = db.save(doc)
        print "Project %r created as Document(%r)" % (name, _id)
        return True
    else :
        print "Project %r already exist" % name
        return False
