'''
Created on Jan 10, 2013    
@author: pixo
'''
import os, time
import badass.utils as utils


def createAsset ( db = None, doc_id = "", description = "", overdoc = dict() ): 
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
    if db == None:
        db = utils.getDb ()
        
    # Get data from doc_id
    project, typ, asset = doc_id.split ( "_" )
    name = "%s_%s" % ( typ, asset )
    
    #Check if project name is right
    if not ( project in db ) :
        print "createAsset: %s project doesn't exist" % project
        return False
    
    # If asset doesn't exist create the asset
    if not ( doc_id in db ) :
        
        #Create the asset structure
        doc = {
            "type" : typ,
            "_id" : doc_id,
            "project_id" : project,
            "name" : name,
            "description" : description,
            "creator" : os.getenv ( "USER" ),
            "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.localtime() ),
            "state" : "na"
            }
        
        #Add extra data if needed
        doc.update ( overdoc )
        
        # Save data structure into the database
        _id, _rev = db.save (doc )
        
        print "createAsset: Added %r to project %r" % ( name , project )
        return db[_id]
    
    else:        
        print "createAsset: %s already exist" % name
        return False


def createTask ( db = None, doc_id = "", description = "", overdoc = dict() ):
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
    if db == None:
        db = utils.getDb()
        
    #Get datas from doc_id
    project, typ, asset, task, fork = doc_id.split ( "_" )
    asset_id = "%s_%s_%s" % ( project, typ, asset )
    name = "%s_%s_%s_%s" % ( typ, asset, task, fork )
        
    #Check if project name is right
    if not ( project in db ) :
        print "createTask: %s project doesn't exist" % project
        return False
    
    # Check if the asset exist
    if not ( asset_id in db ):
        print "createTask: Asset '%s' doesn't exist" % asset_id 
        return False
    
    # If task doesn't exist create it
    if not ( doc_id in db ) : #not ( name in task_ls ) :
        
        # Create the task structure
        doc = {
            "type" : "%s_%s" % (typ,task),
            "task" : task,
            "_id" : doc_id,
            "project_id" : project,
            "asset_id" : asset_id,
            "fork" : fork,
            "name" : name,
            "description" : description,
            "versions" : dict(),
            "creator" : os.getenv ( "USER" ),
            "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.localtime() ),
            "state" : "na"
            }
        
        #Add extra data if needed
        doc.update(overdoc)
        
        #Save data structure into the database
        _id, _rev = db.save (doc )
        
        print "createTask: Added %r to project %r" % ( name , project )
        return db[_id]
    
    else:
        print "createTask: %s already exist" % name
        return False

 
def createShot ( db = None, doc_id = "", description = "No description",
                    cut_in = 1, cut_out = 100 ):
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
    overdoc = {"seq" : doc_id.split("_")[2].split("-")[0],
               "cut_in": cut_in,
               "cut_out": cut_out }
     
    # Create asset shot with shot extra attributes
    shot = createAsset ( db, doc_id, description, overdoc )
    
    return shot
    
