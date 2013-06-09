import pipeline.core as core
import pipeline

# source = "/homeworks/projects/bls/chr/belanus/mod/main/001/bls_chr_belanus_mod_main.mb"
# destination = "/homeworks/projects/bls/chr/belanus/mod/main/001" 
# core.assetExport ( source, destination )

# db = pipeline.utils.getDb("projects", "http://admin:admin@127.0.0.1:5984/")
# pipeline.utils.createDbViews(db)

#!/usr/bin/env python
import os
import pipeline.core as core
import pipeline.utils as utils

def cli ( path, description ):
    
    if not os.path.exists ( path ):
        print "hk-texture-publish: %s doesn't exists" % path
        return 1

    if not os.path.isdir ( path ):
        print "hk-texture-publish: %s should be a path" % path
        return 1

    if not os.path.isabs ( path ) :
        path = os.path.abspath ( path )   

    db = utils.getDb ()
    doc_id = core.getIdFromPath ( path )
        
    if not ( doc_id in db ) :
        print "hk-texture-publish: %s isn't in the  database" % doc_id
        return 1
            
    core.texturePush ( db, doc_id, path, description )
    return 0

cli ( "/homeworks/users/pixo/projects/testing/chr/belanus/tex/main/002", "change naming convention ")
