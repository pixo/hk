'''
Created on Jan 8, 2013

@author: pixo
'''
import pipeline.core as core
import pipeline.utils as utils

db = utils.dataBase.getDataBase()
entity_id = "testing_sq001_sq001-sh001_lighting"
source_file ="/homeworks/users/pixo/projects/testing/shots/sq001/sq001-sh001/lighting/testing_sq001_sq001-sh001_lighting.txt"
source_file =list({"lighting/caca.1001.1.txt","lighting/caca.1001.2.txt","lighting/caca.1001.3.txt"})
comments = "ma bite"

#core.repository.getIdFromPath(db,"/homeworks/users/pixo/projects/testing/shots/sq001/sq001-sh001/lighting/testing_sq001_sq001-sh001_lighting.txt")
#core.repository.pull(db, entity_id, 1)
core.repository.push(db, entity_id, source_file, comments)