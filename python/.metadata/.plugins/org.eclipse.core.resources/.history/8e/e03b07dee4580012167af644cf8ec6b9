'''
Created on Jan 6, 2013

@author: pixo
'''
import os,time

def createProject(name,db):
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
