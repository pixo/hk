'''
Created on Jan 6, 2013

@author: pixo
'''
import os
import couchdb

class ProjectNoSet ( Exception ) :
    pass

def getDesign () :
    return "AssetManager"

def getServer () :
    return os.getenv ( "HK_DB_SERVER" )

def getDb ( dbname = "" , serveradress = "" ) :
    
    if serveradress == "" :
        serveradress = getServer ()
    
    if dbname == "" :
        dbname = os.getenv ( "HK_DB" )
        
    server = couchdb.Server ( serveradress )
    
    if dbname in server :
        return server [ dbname ]
    else :
        return False

def lsDb( db = None , view = "", startkey = "", endkey = "" ):
    
    if db == None :
        db = getDb ()
        
    if endkey == "":
        endkey = startkey + "\u0fff"
    
    design = getDesign()    
    view = db.view ( "_design/%s/_view/%s" % ( design, view ),
                    startkey = startkey, endkey = endkey )
    
    doc_ls = list()
    
    for row in view.rows:
        doc_ls.append(row["value"]["name"])
        
    return doc_ls

def createDbViews (db):
    doc = {
           "_id" : "_design/AssetManager",
           "language" : "javascript",
           "views" : {
                     'project': {'map': 'function(doc) {\n  if(doc.type == "project") {\n    emit(doc.name, doc);\n}\n}'},
                     'asset_task': {'map': 'function(doc) {\n  if(doc.task && !doc.shot_id) {\n    emit(doc._id, doc);\n}\n}'},
                     'shot_task': {'map': 'function(doc) {\n  if(doc.task && doc.shot_id) {\n    emit(doc._id, doc);\n}\n}'},
                     'shot': {'map': 'function(doc) {\n  if(doc.type == "shot") {\n    emit(doc._id, doc);\n}\n}'},
                     'seq': {'map': 'function(doc) {\n  if(doc.type == "seq") {\n    emit(doc._id, doc);\n}\n}'},
                     'tex': {'map': 'function(doc) {\n  if(doc.task == "tex") {\n    emit(doc._id, doc);\n}\n}'},
                     'prp': {'map': 'function(doc) {\n  if(doc.type == "prp") {\n    emit(doc._id, doc);\n}\n}'},
                     'rig': {'map': 'function(doc) {\n  if(doc.task == "rig") {\n    emit(doc._id, doc);\n}\n}'},
                     'sct': {'map': 'function(doc) {\n  if(doc.task == "sct") {\n    emit(doc._id, doc);\n}\n}'},
                     'rtp': {'map': 'function(doc) {\n  if(doc.task == "rtp") {\n    emit(doc._id, doc);\n}\n}'},
                     'vcl': {'map': 'function(doc) {\n  if(doc.type == "vcl") {\n    emit(doc._id, doc);\n}\n}'},
                     'lit': {'map': 'function(doc) {\n  if(doc.task == "lit") {\n    emit(doc._id, doc);\n}\n}'},
                     'chr': {'map': 'function(doc) {\n  if(doc.type == "chr") {\n    emit(doc._id, doc);\n}\n}'},
                     'env': {'map': 'function(doc) {\n  if(doc.type == "env") {\n    emit(doc._id, doc);\n}\n}'},
                     'mtl': {'map': 'function(doc) {\n  if(doc.type == "mtl") {\n    emit(doc._id, doc);\n}\n}'},
                     'lay': {'map': 'function(doc) {\n  if(doc.task == "lay") {\n    emit(doc._id, doc);\n}\n}'},
                     'mod': {'map': 'function(doc) {\n  if(doc.task == "mod") {\n    emit(doc._id, doc);\n}\n}'},
                     'srf': {'map': 'function(doc) {\n  if(doc.task == "srf") {\n    emit(doc._id, doc);\n}\n}'},
                     'dmp': {'map': 'function(doc) {\n  if(doc.task == "dmp") {\n    emit(doc._id, doc);\n}\n}'},
                     'cam': {'map': 'function(doc) {\n  if(doc.task == "cam") {\n    emit(doc._id, doc);\n}\n}'},
                     'vfx': {'map': 'function(doc) {\n  if(doc.type == "vfx") {\n    emit(doc._id, doc);\n}\n}'},
                     'cmp': {'map': 'function(doc) {\n  if(doc.task == "cmp") {\n    emit(doc._id, doc);\n}\n}'}
                     }
           }  
    _id, _rev = db.save (doc )
    return (_id, _rev)

def createDb ( name = "default", serveradress = None ):
    server = couchdb.client.Server ( serveradress )
    db = server.create ( name )
    createDbViews ( db )
    return db
