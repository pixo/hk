import os
import pipeline.core as core
import pipeline.utils as utils
import glob, re

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

def getFileSeq( dirPath ):
    '''Return file sequence with same name as the parent directory. Very loose example!!'''
    dirName = os.path.basename( dirPath )
    # COLLECT ALL FILES IN THE DIRECTORY THAT HVE THE SAME NAME AS THE DIRECTORY
#     files = glob.glob( os.path.join( dirPath, '%s.*.*' % doc_id ) )
    files = glob.glob( os.path.join( dirPath, '*' ) )
    files.sort()
    # GRAB THE RIGHT MOST DIGIT IN THE FIRST FRAME'S FILE NAME
    firstString = re.findall( r'\d+', files[0] )[-1]
    # GET THE PADDING FROM THE AMOUNT OF DIGITS
    padding = len( firstString )
    # CREATE PADDING STRING FRO SEQUENCE NOTATION
    paddingString = '%02s' % padding
    # CONVERT TO INTEGER
    first = int( firstString )
    # GET LAST FRAME
    last = int( re.findall( r'\d+', files[-1] )[-1] )
    # GET EXTENSION
    ext = os.path.splitext( files[0] )[-1]
    # BUILD SEQUENCE NOTATION
    fileName = '%s.%%%sd%s %s-%s' % ( files[0].split(".")[0], str(padding).zfill(2), ext, first, last )
    # RETURN FULL PATH AS SEQUENCE NOTATION
    return os.path.join( dirPath, fileName )


print getFileSeq ("/homeworks/users/pixo/projects/bls/shot/studio-bls/lit/main/test/belanus/beauty")