'''
Created on Jan 7, 2013

@author: pixo
'''
import os, time

def lsShotTask(db, shot_id="",task=""):
    startkey = u"%s_%s" % (shot_id,task)
    endkey = u"%s_%s\u0fff" % ( shot_id,task)
    view = db.view("_design/%s/_view/%ssByProjectAndName" % ("cg_project",task), startkey=startkey, endkey=endkey)
    tasks = list()
    
    for row in view.rows:
        tasks.append(row["value"]["name"])
        print row["value"]["name"]
    return tasks

def createShotTask( db, project, sequence, shot, assettype, description ):
    """string projectName, string shotName, string description, int cut_in, int cut_out, couch.db.Server db"""
    project_id = "%s" % project
    sequence_id = "%s_%s" % (project_id, sequence)
    shot_id = "%s_%s" % (sequence_id, shot)
    task_id = "%s_%s" % (shot_id, assettype)
    
    name = "%s_%s" % (shot, assettype)
#     shot_doc = db[shot_id]
#     tasks = shot_doc.setdefault(assettype, {})
    taskslist = lsShotTask(db, shot_id, assettype)
    
    if not ( name in taskslist ) :
        task_doc = {
            "type": assettype,
            "_id": task_id,
            "project_id": project_id,
            "sequence_id": sequence_id,
            "shot_id": shot_id,
            "name": name,
            "description": description,
            "versions": dict(),
            "creator": os.getenv("USER"),
            "created": time.strftime("%Y %b %d %H:%M:%S", time.gmtime()),
            "inherit": "shots",
            "state":"na"
        }
        
        _id, _rev = db.save(task_doc)
        print "createShotTask: Added %r to project %r" % (name , project)
        return True
    
    else:
        print "createShotTask: Shot %s already exist" % name
        return False
    