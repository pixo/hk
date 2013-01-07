'''
Created on Jan 6, 2013

@author: pixo
'''
import os,time
import pipeline.utils as utils

def createProjectOnFS(name):
    projectsRootPath = utils.path.getProjectsPath()
    projectPath = "%s/%s" % (projectsRootPath,name)
    if not os.path.exists(projectPath): 
        os.makedirs(projectPath, mode = 0775) 
        print "Project %s created : %s" % (name, projectPath)

def createProjectOnDB(name,db):
    #TODO:check if project exist
    doc = {
    "_id": "%s" % name,
    "type": "project",
    "name": name,
    "creator": os.getenv("USER"),
    "created": time.strftime("%Y %b %d %H:%M:%S", time.gmtime())
    }
    _id, _rev = db.save(doc)
    print "Project %r created as Document(%r)" % (name, _id)
    
def createProject(name,db):
    createProjectOnDB(name,db)
    #createProjectOnFS(name)
