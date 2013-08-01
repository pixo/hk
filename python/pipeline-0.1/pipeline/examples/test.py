import os
import pipeline.core as core
import pipeline.utils as utils
import glob, re


fname = "/homeworks/users/pixo/projects/testing/shot/op001/lay/a/testing_shot_op001_lay_a.v003.base1/testing_shot_op001_lay_a.ma"

def getDocIdFromRefFile ( fname ):
    basename = os.path.basename ( fname )
    doc_id = os.path.splitext ( basename )[0]
    return doc_id

doc_id = getDocIdFromRefFile ( fname )
print core.getAssetVersions ( doc_id )