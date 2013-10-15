'''
Created on Jan 6, 2013

@author: pixo
'''
import os, socket
import couchdb
import rule

class ProjectNoSet ( Exception ) :
    pass

def getDesign () :
    return "AssetManager"

def getServer ( serveradress = "" ) :
    
    if serveradress == "" :
        serveradress = os.getenv ( "HK_DB_SERVER" )
        
    if serveradress.find ( "http://" ) == -1 :
        serveradress = "http://%s/" %  serveradress
        
    db_server = couchdb.Server ( serveradress )
     
    return db_server 

def serverExists ( serveradress = "" ) :
    server = couchdb.Server ( serveradress )
    try:
        stats = server.stats()
        return True
    except:
        return False

def getDb ( dbname = "" , serveradress = "" ) :
    
    if dbname == "" or dbname == None  :
        dbname = os.getenv ( "HK_DB" )
        
        if dbname == "" or dbname == None:
            print "getDb(): wrong dbname '%s'" % str(serveradress)
            return False
        
    server = getServer ( serveradress )
    
    if dbname in server :
        return server [ dbname ]
    
    else :
        return False



def lsDb ( db = None , view = "", startkey = "", endkey = "" ):
    
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
