'''
Created on Jan 6, 2013

@author: pixo
'''
import pipeline.core as core
import pipeline.utils as utils
import os

db=utils.dataBase.getDataBase()
project=os.getenv("HK_PROJECT")
sequence="001"
shot="001"

core.asset.createAsset( db, "testing_chr_caca", "Asset shit ma queue" )
core.task.createTask( db, "testing_chr_caca_mod_main", "modeling ma queue" )

# core.asset.createAsset(db, "testing_chr_maqueue", "Asset shit ma queue")
# core.task.createTask(db, "testing_chr_mickey_mod_main", "modeling shit ma bite")

# core.project.createProject(project, db)
# 
# for seq in range(1,3):
#     sequence_name="sq%03d" % seq
#     core.sequence.createSequence(project, sequence_name, "ceci est une sequence", db)
#     for sh in range(1,3):
#         shot_name="%s-sh%03d"% (sequence_name,sh)
#         core.shot.createShot(project, sequence_name, shot_name, "ceci est le shot %03d" % sh, 1, 100, db)
#         core.shotTask.createShotTask(project, sequence_name, shot_name, "lighting", "ceci est une tache lighting", db)
        #core.shotTask.createShotTask(project, sequence_name, shot_name, "render", "ceci est une tache render", db)
        #core.shotTask.createShotTask(project, sequence_name, shot_name, "comp", "ceci est une tache comp", db)
        #core.shotTask.createShotTask(project, sequence_name, shot_name, "layout", "ceci est une tache layout", db)

#core.shot.lsShots(db, project,sequence)

#core.sequence.lsSequences(db, project)
#core.project.createProject(project, db)
#core.sequence.createSequence(project, sequence, "ceci est une sequence", db)
#core.shot.createShot(project, sequence, shot, "ceci est un shot", 1, 100, db)