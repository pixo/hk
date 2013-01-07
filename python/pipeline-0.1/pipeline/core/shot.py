'''
Created on Jan 6, 2013

@author: pixo
'''
#import couchdb
#import argparse
import os,time

def lsShots(db, project="", sequence="", shot=""):
    if sequence != "":
        sequence="sq%s_" % sequence
        if shot != "":
            shot="sh%s_" % shot
         
    startkey = u"%s_%s%s" % (project , sequence, shot)
    endkey = u"%s_%s%s\u0fff" % (project , sequence, shot)
    view = db.view("_design/%s/_view/shotsByProjectAndName" % "cg_project", startkey=startkey, endkey=endkey)
    shots = list()
    
    for row in view.rows:
        shots.append(row["value"]["name"])
        print row["value"]["name"]
    return shots

def createShot(project, sequence, name, description, cut_in, cut_out, db):
    """string projectName, string shotName, string description, int cut_in, int cut_out, couch.db.Server db"""
    project_id = "%s" % project
    sequence_id = "%s_%s" % (project_id, sequence)
    sequence_doc = db[sequence_id]
    shots = sequence_doc.setdefault("shots", {}) 
    shotslist = lsShots(db, project, sequence, name)
    
    if not (name in shotslist ) :
        shot_doc = {
            "type": "shot",
            "_id": "%s_%s" % (project_id, name),
            "name": name,
            "project_id": project_id,
            "sequence_id": sequence_id,
            "description": description,
            "cut_in": cut_in,
            "cut_out": cut_out,
            "creator": os.getenv("USER"),
            "created": time.strftime("%Y %b %d %H:%M:%S", time.gmtime())
        }
        
        _id, _rev = db.save(shot_doc)
        print "createShot: Added shot %r to sequence %r project %r" % (name, sequence, project)
        return True
    else:
        print "createShot: Shot %s already exist" % name
        return False