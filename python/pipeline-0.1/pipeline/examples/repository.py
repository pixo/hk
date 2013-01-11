'''
Created on Jan 8, 2013

@author: pixo
'''
import pipeline.core as core
import pipeline.utils as utils


db = utils.dataBase.getDataBase()
entity_id = "testing_sq001_sq001-sh001_lighting"
entity_id = "testing_chr_caca"
entity_id = "testing_chr_caca_mod_main"
source_file = list()
source_file.append("/homeworks/users/pixo/projects/testing/chr/chr_caca/chr_caca_mod/chr_caca_mod_main/testing.001.txt")
source_file.append("/homeworks/users/pixo/projects/testing/chr/chr_caca/chr_caca_mod/chr_caca_mod_main/testing.002.txt")
source_file.append("/homeworks/users/pixo/projects/testing/chr/chr_caca/chr_caca_mod/chr_caca_mod_main/testing.003.txt")

# source_file =list({"lighting/caca.1001.1.txt","lighting/caca.1001.2.txt","lighting/caca.1001.3.txt"})
comments = "ma bite"

core.repository.createWorkspace(db, entity_id)
# core.repository.getIdFromPath(db,source_file)
#core.repository.pull(db, entity_id)
core.repository.push(db, entity_id, source_file, comments)