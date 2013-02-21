'''
Created on Jan 6, 2013

@author: pixo
'''
import os
import couchdb

class ProjectNoSet(Exception):
    pass

def getDataBase( dbname = False, serveradress = False):
    
    if not serveradress :
        serveradress = os.getenv ( "HK_DB_SERVER" )
    
    if not dbname :
        dbname = os.getenv ( "HK_DB" )
        
    server = couchdb.Server ( serveradress )
    
    return server [ dbname ]

def lsDb( db = None, view = "", startkey = "", endkey = "" ):
    
    if db == None:
        db = getDataBase ()
        
    if endkey == "":
        endkey = startkey + "\u0fff"
        
    view = db.view ( "_design/%s/_view/%s" % ( "homeworks", view ),
                    startkey = startkey, endkey = endkey )
    
    doc_ls = list()
    for row in view.rows:
        doc_ls.append(row["value"]["name"])
        
    return doc_ls