import os
import pipeline.core as core
import pipeline.utils as utils
# 
# def cli ( path, description ):
#     if not os.path.exists ( path ):
#         print "hk-texture-publish: %s doesn't exists" % path
#         return False
#     
#     db = utils.getDb ()
#     doc_id = core.getIdFromPath ( path )
#         
#     if not ( doc_id in db ) :
#         print "hk-texture-publish: %s isn't in the  database" % doc_id
#         return False
#             
#     core.texturePush ( db, doc_id, path, description )
#      
# path = "/homeworks/users/pixo/projects/testing/chr/mickey/tex/main/003"    
# cli ( path, "test publish")
