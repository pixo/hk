'''
Created on Jan 8, 2013

@author: pixo
'''
import pipeline.core as core
import pipeline.utils as utils

db = utils.dataBase.getDataBase()
entity_id = "testing_sq001_sq001-sh001_lighting"

core.repository.push(db, entity_id,"/home/pixo/caca.txt","my comments")

#core.repository.pull(db, entity_id, 1)