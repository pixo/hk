'''
Created on Jan 6, 2013

@author: pixo
'''
#import couchdb
#import argparse
import os,time

def lsSequences(db, project="", sequence=""):
    if sequence != "":
        sequence="sq%s_" % sequence
    
    startkey = u"%s_" % project
    endkey = u"%s_\u0fff" % project
    view = db.view("_design/%s/_view/sequencesByProjectAndName" % "cg_project", startkey=startkey, endkey=endkey)
    seqs = list()
    
    for row in view.rows:
        seqs.append(row["value"]["name"])
        print row["value"]["name"]
    return seqs

def createSequence(project, name, description, db):
    """string projectName, string sequenceName, string description, couch.db.Server db"""
    project_id = "%s" % project
    project_doc = db[project_id]
    
    seqs = project_doc.setdefault("sequences", {})
    seqlist = lsSequences(db, project)
    
    if not (name in seqlist) :
        seq_doc = {
            "type": "sequence",
            "_id": "%s_%s" % (project_doc["_id"], name),
            "name": name,
            "project_id": project_id,
            "description": description,
            "creator": os.getenv("USER"),
            "created": time.strftime("%Y %b %d %H:%M:%S", time.gmtime())
        }
        
        _id, _rev = db.save(seq_doc)
        print "createSequence: Added sequence %r to project %r" % (name, project)
        return True
    else:
        print "createSequence: Sequence %s already exist" % name
        return False
