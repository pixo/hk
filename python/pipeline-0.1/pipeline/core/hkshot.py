'''
Created on Jan 11, 2013

@author: pixo
'''
import os, time
import pipeline.utils as utils
import hksequence
    
def lsDbShot ( db, doc_id ):
    doc_id = doc_id.split("_")
    project,seq,shot = doc_id[0], doc_id[1], doc_id[2]
    startkey = u"%s_%s_%s" % ( project, seq, shot )
    endkey = u"%s_%s_%s\u0fff" % ( project, seq, shot )
    return utils.dataBase.lsDb(db, "shot", startkey, endkey)

def createShot( db, doc_id, cut_in, cut_out, description ):
    """
    Create a shot.
    db, type couch.db.Server
    doc_id, type string
    description, type string
    """
    
    """ Get datas from doc_id """
    project, seq, shot = doc_id.split ( "_" )
    name = "%s_%s" % ( seq, shot )
    
    """ Check the sequence exists """
    seq_ls = hksequence.lsDbSeq( db, doc_id )
    if not ( seq in seq_ls ):
        print "createShot: Sequence %s doesn't exists ." % seq
        return False

    """ Check the shot doesn't exists """
    shot_ls = lsDbShot ( db, doc_id )
    if not ( name in shot_ls ) :
        """ Create the shot structure """
        doc = {
            "type" : "shot",
            "_id" : doc_id,
            "project_id" : project,
            "name" : name,
            "description" : description,          
            "cut_in": cut_in,
            "cut_out": cut_out,
            "creator" : os.getenv ( "USER" ),
            "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.gmtime() ),
            "state" : "na"
            }
        
        """Save data structure into the database """
        _id, _rev = db.save (doc )
        
        print "createShot: Added %r to project %r" % ( name , project )
        return db[_id]
    
    else:        
        print "createShot: %s already exist" % name
        return False