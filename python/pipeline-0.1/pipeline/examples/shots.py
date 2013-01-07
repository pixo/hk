'''
Created on Jan 6, 2013

@author: pixo
'''
import pipeline.core as core
import pipeline.utils as utils

db=utils.dataBase.getDataBase()
project="testing"
sequence="001"
shot="001"

#core.project.createProject(project, db)
for seq in range(1,3):
    sequence_name="sq%03d" % seq
    core.sequence.createSequence(project, sequence_name, "ceci est une sequence", db)
    for sh in range(1,10):
        shot_name="%s_sh%03d"% (sequence_name,sh)
        core.shot.createShot(project, sequence_name, shot_name, "ceci est le shot %03d" % sh, 1, 100, db)

#core.shot.lsShots(db, project,sequence)

#core.sequence.lsSequences(db, project)
#core.project.createProject(project, db)
#core.sequence.createSequence(project, sequence, "ceci est une sequence", db)
#core.shot.createShot(project, sequence, shot, "ceci est un shot", 1, 100, db)