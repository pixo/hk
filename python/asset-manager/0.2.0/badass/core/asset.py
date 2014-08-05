'''
Created on Jan 10, 2013    
@author: pixo
'''
import time
import badass.utils as utils

def createAsset (db = None, doc_id = "", description = "", overdoc = dict(), debug = False):
    """
    This function create an **asset** into the provided database.

    :param db: The database.
    :type db: couchdb.client.Database
    :param doc_id: The asset code.
    :type doc_id: str
    :param description: The asset description.
    :type description: str
    :param overdoc: A dictionnary that contains extra document attributes.
    :type overdoc: dict
    :returns:  document -- The database document.
    :raises: AttributeError, KeyError

    **Example:**
    
    >>> db = pipeline.utils.getDb ( dbname = "prod" , serveradress = "127.0.0.1:5984" )
    >>> createAsset ( db = db, doc_id = "prod_ch_mickey", "This is the mickey characters" )
    
    """

    # Check if db exist if not, get the current project db
    if db==None:
        db=utils.getDb ()

    # Get data from doc_id
    project, typ, slug=doc_id.split ("_")
    asset="%s_%s"%(typ, slug)

    # Check if project name is right
    if not (project in db) :
        print "createAsset: %s project doesn't exist"%project
        return False

    # If asset doesn't exist create the asset
    if doc_id in db :
        print "createAsset: %s already exist"%asset
        return False

    # Create the asset structure
    doc={
        "_id" : doc_id,
        "project" : project,
        "name" : slug,
        "type" : typ,
        "masters":{},
        "tags":{},
        "comments":{},
        "inactive" : False,
        "parents": {},
        "children": {},
        "description" : description,
        "creator" : utils.getCurrentUser(),
        "created" : time.time(),  # time.strftime ( "%Y %b %d %H:%M:%S", time.localtime() ),
        "status": { "art":"ns", "tec":"ns" },
        "infos": { "bid":1, "delivery": 20140611.5, "spent":0, "assigned":"" },
        "subscribers": {}
        }

    # Add extra data if needed
    doc.update (overdoc)

    # Save data structure into the database
    _id, _rev=db.save(doc)

    if not debug :
        print "createAsset: Added %r to project %r"%(asset , project)
    return db[_id]

def createTask (db = None, doc_id = "", description = "", overdoc = dict(), debug = False):
    """
    This function create a **task** into the provided database.

    :param db: The database.
    :type db: couchdb.client.Database
    :param doc_id: The asset code.
    :type doc_id: str
    :param description: The asset description.
    :type description: str
    :param overdoc: A dictionnary that contains extra document attributes.
    :type overdoc: dict
    :returns:  document -- The database document.
    :raises: AttributeError, KeyError

    **Example:**
    
    >>> db = pipeline.utils.getDb ( dbname = "prod" , serveradress = "127.0.0.1:5984" )
    >>> createTask ( db = db, doc_id = "prod_ch_mickey_mod_a", "This is the mickey modeling task 'a'" )
    
    """

    # If db isn't provided, get the current project database
    if db==None:
        db=utils.getDb()

    # Get datas from doc_id
    project, typ, slug, task, fork=doc_id.split ("_")
    asset_id="%s_%s_%s"%(project, typ, slug)
    asset="%s_%s_%s_%s"%(typ, slug, task, fork)

    # Check if project name is right
    if not (project in db) :
        print "createTask: %s project doesn't exist"%project
        return False

    # Check if the asset exist
    if not (asset_id in db):
        print "createTask: Asset '%s' doesn't exist"%asset_id
        return False

    # If task doesn't exist create it
    if doc_id in db :
        print "createTask: %s already exist"%asset
        return False

    # Create the task structure
    doc={
        "_id" : doc_id,
        "project" : project,
        "type" : typ,
        "name" : slug,
        "task" : task,
        "fork" : fork,
        "review" : dict(),
        "release" : dict(),
        "masters":{},
        "tags":{},
        "inactive" : False,
        "parents": {},
        "children": {},
        "comments":{},
        "description" : description,
        "creator" : utils.getCurrentUser(),
        "created" : time.time(),  # time.strftime ( "%Y %b %d %H:%M:%S", time.localtime() ),
        "status": { "art":"ns", "tec":"ns" },
        "infos": { "bid":1, "delivery": 20140611.5, "spent":0, "assigned":"" },
        "subscribers": {}
        }

    # Add extra data if needed
    doc.update(overdoc)

    # Save data structure into the database
    _id, _rev=db.save (doc)
    if not debug :
        print "createTask: Added %r to project %r"%(asset , project)
    return db[_id]

def createPack (db = None, doc_id = "", description = "No description"):
    """
    This function create an asset of type **Pack** into the provided database.

    :param db: The database.
    :type db: couchdb.client.Database
    :param doc_id: The asset code.
    :type doc_id: str
    :param description: The asset description.
    :type description: str
    :returns:  document -- The database document.
    :raises: AttributeError, KeyError

    **Example:**
    
    >>> db = pipeline.utils.getDb ( dbname = "prod" , serveradress = "127.0.0.1:5984" )
    >>> createShot ( db = db, doc_id = "prod_shot_op001", description = "This is the shot openning 001", cut_in = 1, cut_out = 100 )
    
    """

    # Extra shot attributes
    overdoc={"pack" : {}}

    # Create asset shot with shot extra attributes
    result=createAsset (db, doc_id, description, overdoc)

    return result

def createShot (db = None, doc_id = "", description = "No description",
                    cut_in = 1, cut_out = 100):
    """
    This function create an asset of type **Shot** into the provided database.

    :param db: The database.
    :type db: couchdb.client.Database
    :param doc_id: The asset code.
    :type doc_id: str
    :param description: The asset description.
    :type description: str
    :param cut_in: The first frame of the shot.
    :type cut_in: float
    :param cut_out: The last frame of the shot.
    :type cut_out: float
    :returns:  document -- The database document.
    :raises: AttributeError, KeyError

    **Example:**
    
    >>> db = pipeline.utils.getDb ( dbname = "prod" , serveradress = "127.0.0.1:5984" )
    >>> createShot ( db = db, doc_id = "prod_shot_op001", description = "This is the shot openning 001", cut_in = 1, cut_out = 100 )
    
    """

    # Extra shot attributes
    overdoc={"seq" : doc_id.split("_")[2].split("-")[0],
               "cut_in": cut_in,
               "cut_out": cut_out }

    # Create asset shot with shot extra attributes
    result=createAsset (db, doc_id, description, overdoc)

    return result

def setAssetAttr(db = None, docId = "", attr = None, value = None):
    if docId=="" or not attr:
        print ("setAssetAttr(): please provide proper attributes.")
        return

    if not db :
        db=utils.getDb ()

    doc=db[docId]
    doc[attr]=value
    _id, _rev=db.save (doc)
