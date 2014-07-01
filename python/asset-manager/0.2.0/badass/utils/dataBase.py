'''
Created on Jan 6, 2013

@author: pixo
'''
import os
import couchdb
import rule

class DatabaseError ( Exception ):
    """
    Error raised by the project module.
    
    """
    def __init__ ( self, value ):
        self.value = value
    def __str__ ( self ):
        return repr ( self.value )


def getDesign () :
    return "AssetManager"


def getServer ( serveradress = "" ) :

    if serveradress == "" :
        serveradress = os.getenv ( "HK_DB_SERVER" )

    if serveradress.find ( "http://" ) == -1 :
        serveradress = "http://%s" % serveradress

    db_server = couchdb.Server ( serveradress )

    return db_server


def serverExists ( serveradress = "" ) :
    if serveradress.find ( "http://" ) < 0:
        serveradress = "http://%s" % serveradress

    server = couchdb.Server ( serveradress )

    try:
        stats = server.stats()
        return stats

    except:
        return False

def getDb ( dbname = "" , serveradress = "" ) :

    if dbname == "" or dbname == None  :
        dbname = os.getenv ( "HK_DB" )

        if dbname == "" or dbname == None:
            print "getDb(): wrong dbname '%s'" % str( serveradress )
            return False

    if serveradress == "" :
        serveradress = os.getenv ( "HK_DB_SERVER" )

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

    design = getDesign()
    viewname = "_design/%s/_view/%s" % ( design, view )
    view = db.view ( viewname, startkey = startkey, endkey = endkey )

    doc = dict()
    for row in view.rows:
        doc[row["key"]] = row["value"]
    return doc

#     doc_ls = list()
#     for row in view.rows:
#         doc_ls.append( row["value"]["name"] )
#     return doc_ls

def createDbViews ( db ):
    asset = rule.getAssetTypes ()
    task = rule.getAssetTasks()

    views = dict()
    views['project'] = {'map': 'function(doc) {\n  if(doc.type == "project") {\n    emit(doc.name, doc);\n}\n}'}
    views['asset'] = {'map': "function(doc) {\n  if(doc.type != \"project\" && !doc.task  ) {\n    emit(doc._id, doc);\n}\n}"}
    views['task'] = {"map": "function(doc) {\n  if(doc.task) {\n    emit(doc._id, doc);\n}\n}"}

    for key in asset:
        views[asset[key]] = {'map': 'function(doc) {\n  if(doc.type == "%s") {\n    emit(doc._id, doc);\n}\n}' % asset[key]}

    for key in task:
        views[task[key]] = {'map': 'function(doc) {\n  if(doc.task == "%s") {\n    emit(doc._id, doc);\n}\n}' % task[key] }

    doc = {
           "_id" : "_design/AssetManager",
           "language" : "javascript",
           "views" : views
           }

    _id, _rev = db.save ( doc )
    return ( _id, _rev )

def createDb ( name = None, serveradress = None ):
    """
    This function create a **DataBase** into the provided server.

    :param name: The database name.
    :type name: str
    :param serveradress: The asset code.
    :type serveradress: str
    
    :returns: Database -- return the database
    :raises: DatabaseError if database already exist

    **Example:**
    
    >>> createDb ( name = "prod", serveradress = "admin:pass@192.168.0.100" )
    """

    if not ( serveradress ) or ( serveradress == "" ) :
        raise DatabaseError ( "CreateDb (): Serveradress doesn't exists" % name )

    # Get Db Server
    server = couchdb.client.Server ( serveradress )

    # Check if db name already exist
    if name in server :
        raise DatabaseError ( "CreateDb (): Database '%s' already exist" % name )

    # Create DataBate
    db = server.create ( name )

    # Create predefined Database Views
    createDbViews ( db )

    return db
