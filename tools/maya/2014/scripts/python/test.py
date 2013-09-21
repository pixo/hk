import maya_check_dependencies as mcd
import pipeline.core as core

fname = "/homeworks/users/pixo/projects/testing/shot/op001/lay/a/testing_shot_op001_lay_a.v003.base1/testing_shot_op001_lay_a.ma"
# mcd.mCheckDependencies ( fname )

print mcd.getDocIdFromRefFile ( fname )
