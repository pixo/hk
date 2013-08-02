'''
Created on Jan 10, 2013    
@author: pixo
'''
import os, time
import pipeline.utils as utils

def lsAsset ( db, doc_id ):
    doc_id = doc_id.split("_")
    project, typ, asset = doc_id[0], doc_id[1], doc_id[2]
    return utils.lsDb(db, typ, doc_id)

def createAsset( db = None, doc_id = "", description = "", overdoc = dict() ):
    """
    Create a asset.
    db, type couch.db.Server
    doc_id, type string
    description, type string
    """

    if db == None:
        db = utils.getDb ()
        
    """ Get datas from doc_id """
    project, typ, asset = doc_id.split ( "_" )
    name = "%s_%s" % ( typ, asset )
    
    """ Check the asset doesn't exist """
    asset_ls = utils.lsDb(db, typ, doc_id)
    if not ( name in asset_ls ) :
        """ Create the asset structure """
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
        
        doc.update(overdoc)
        
        """Save data structure into the database """
        _id, _rev = db.save (doc )
        
        print "createAsset: Added %r to project %r" % ( name , project )
        return db[_id]
    
    else:        
        print "createAsset: %s already exist" % name
        return False
        
def createShot( db = None, doc_id = "", cut_in = 1, cut_out = 100,
                description = "No description" ):

    overdoc = {"seq" : doc_id.split("_")[2].split("-")[0],
               "cut_in": cut_in,
               "cut_out": cut_out}
     
    createAsset ( db, doc_id, description, overdoc )
    