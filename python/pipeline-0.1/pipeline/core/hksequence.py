'''
Created on Jan 11, 2013

@author: pixo
'''
import pipeline.utils as utils
import os,time

def lsSeq ( db, doc_id ):
    doc_id = doc_id.split("_")
    project,seq = doc_id[0], doc_id[1]
    startkey = u"%s_%s" % ( project, seq )
    endkey = u"%s_%s\u0fff" % ( project, seq )
    return utils.dataBase.lsDb(db, "seq", startkey, endkey)
    
def createSequence( db, doc_id, description):    
    project, name = doc_id.split ( "_" )
    seq_ls = lsSeq( db, doc_id )
    
    """ Check the asset doesn't exist """
    if not ( name in seq_ls ) :
        
        """ Create the asset structure """
        doc = {
            "type" : "seq",
            "_id" : doc_id,
            "project_id" : project,
            "name" : name,
            "description" : description,
            "creator" : os.getenv ( "USER" ),
            "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.gmtime() ),
            "state" : "na"
            }
                
        """Save data structure into the database """
        _id, _rev = db.save (doc )
        
        print "createAsset: Added %r to project %r" % ( name , project )
        return db[_id]
    
    else:        
        print "createAsset: %s already exist" % name
        return False