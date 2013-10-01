'''
Created on Jan 6, 2013

@author: pixo
'''
import os
import couchdb
import rule

class ProjectNoSet ( Exception ) :
    pass

def getDesign () :
    return "AssetManager"

def getServer () :
    db_server = "http://%s/" % os.getenv ( "HK_DB_SERVER" )
    return db_server

def getDb ( dbname = "" , serveradress = "" ) :
    
    if serveradress == "" or serveradress == None :
        serveradress = getServer ()
        
        if serveradress == "" or serveradress == None :
            print "getDb(): can't get the server address '%s'" % str(serveradress)
            return False
    
    if dbname == "" or dbname == None  :
        dbname = os.getenv ( "HK_DB" )
        
        if dbname == "" or dbname == None:
            print "getDb(): wrong dbname '%s'" % str(serveradress)
            
            return False
        
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
    
    design = getDesign ()
    viewname = "_design/%s/_view/%s" % ( design, view )
    view = db.view ( viewname, startkey = startkey, endkey = endkey )
    
    doc_ls = list()
    
    for row in view.rows:
        doc_ls.append(row["value"]["name"])
        
    return doc_ls

def createDbViews (db):
    asset = rule.getAssetTypes ()
    task = rule.getAssetTasks()
    
    views = dict()
    views['project']= {'map': 'function(doc) {\n  if(doc.type == "project") {\n    emit(doc.name, doc);\n}\n}'}
    views['asset']= {'map': "function(doc) {\n  if(doc.type != \"project\" && !doc.task  ) {\n    emit(doc._id, doc);\n}\n}"}
    views['task']= {"map": "function(doc) {\n  if(doc.task) {\n    emit(doc._id, doc);\n}\n}"}
        
    for key in asset:
        views[asset[key]] = {'map': 'function(doc) {\n  if(doc.type == "%s") {\n    emit(doc._id, doc);\n}\n}' % asset[key]}
    
    for key in task:
        views[task[key]] = {'map': 'function(doc) {\n  if(doc.task == "%s") {\n    emit(doc._id, doc);\n}\n}' % task[key] }
                
    doc = {
           "_id" : "_design/AssetManager",
           "language" : "javascript",
           "views" : views
           }
    
    _id, _rev = db.save (doc )
    return (_id, _rev)

def createDb ( name = "default", serveradress = None ):
    server = couchdb.client.Server ( serveradress )
    db = server.create ( name )
    createDbViews ( db )
    return db
