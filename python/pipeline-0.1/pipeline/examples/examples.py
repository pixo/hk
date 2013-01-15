'''
Created on Jan 11, 2013

ASSET tasks:
    modeling        : mod
    texturing       : tex
    rigging         : rig
    surfacing       : srf
    
SHOT tasks:    
    layouting       : lay
    lighting        : lit
    render          : rdr
    compositing     : cmp
    matte-painting  : dmp
    cam             : cam

ASSET type list:
    character       : chr
    vehicle         : vcl
    prop            : prp
    environment     : env
    freetype        : ***

Filename and id rules:
    project_asset-type_asset_task_fork
    
    project
    asset_id = project_asset-type_asset
    name = asset-type_asset_task_fork

ID example:
    character:
    testing_chr_mickey_tex_main

    shot:
    testing_seq01_sht001_lgt_main

Filesystem example:
    chr/chr_mickey/chr_mickey_tex/chr_mickey_tex_ma
    seq100/seq100_sht100/seq100_sht100_lighting/seq100_sht100_lighting_main

asset: length is 3
    testing_chr_mickey
    testing_seq100_sht100

task: length is 5
    testing_chr_mickey_tex_main
    testing_seq100_sht100_lighting_main

@author: pixo
'''

import pipeline.core as core
import pipeline.utils as utils

def testCreateWs():
    db = utils.dataBase.getDataBase()
    core.hkrepository.createWorkspace(db, "testing_sq02_sh100_lit_main")
    core.hkrepository.createWorkspace(db, "testing_chr_mickey_mod_main")

def testProject():
    db = utils.dataBase.getDataBase()
    name = "testing"
    core.hkproject.createProject(db, name)

def testSequence():
    db = utils.dataBase.getDataBase()
    core.hksequence.createSequence(db,"testing_sq02", "sequence 1")

def testShot():
    db = utils.dataBase.getDataBase()
    core.hkshot.createShot(db,"testing_sq02_sh100", 1, 100,"sequence 1 shot 100")

def testAsset():
    "testing_chr_mickey"
    """
    character        : chr
    vehicle            : vcl
    prop             : prp
    environment     : env
    """
    db = utils.dataBase.getDataBase()
    doc_ids=list({"testing_chr_mickey","testing_vcl_mickey","testing_prp_mickey","testing_env_mickey"})
    
    for doc_id in doc_ids:
        core.hkasset.createAsset(db, doc_id, "ceci est l'asset %s" % doc_id)

def testTask():
    db = utils.dataBase.getDataBase()
#     doc_ids = list({'mod',    
#                 'tex',
#                 'rig',
#                 'srf',
#                 'lay',
#                 'lit',
#                 'cmp',
#                 'dmp',
#                 'cam'})
#     for doc_id in doc_ids :
#         print """ core.hktask.createShotTask(db, "testing_sq01_sh100_%s_main" , "ceci est la tache %s") """% (doc_id,doc_id)
#         core.hktask.createAssetTask(db, "testing_chr_mickey_%s_main" % doc_id, "ceci est la tache %s" % doc_id)
#         core.hktask.createShotTask(db, "testing_sq01_sh100_%s_main" % doc_id, "ceci est la tache %s" % doc_id)
    
    core.hktask.createAssetTask(db, "testing_chr_mickey_srf_main" , "ceci est la tache srf") 
    core.hktask.createAssetTask(db, "testing_chr_mickey_tex_main" , "ceci est la tache tex") 
    core.hktask.createAssetTask(db, "testing_chr_mickey_rig_main" , "ceci est la tache rig") 
    core.hktask.createAssetTask(db, "testing_chr_mickey_mod_main" , "ceci est la tache mod")
    
    core.hktask.createAssetTask(db, "testing_vcl_mickey_srf_main" , "ceci est la tache srf") 
    core.hktask.createAssetTask(db, "testing_vcl_mickey_tex_main" , "ceci est la tache tex") 
    core.hktask.createAssetTask(db, "testing_vcl_mickey_rig_main" , "ceci est la tache rig") 
    core.hktask.createAssetTask(db, "testing_vcl_mickey_mod_main" , "ceci est la tache mod")
    
    core.hktask.createAssetTask(db, "testing_prp_mickey_srf_main" , "ceci est la tache srf") 
    core.hktask.createAssetTask(db, "testing_prp_mickey_tex_main" , "ceci est la tache tex") 
    core.hktask.createAssetTask(db, "testing_prp_mickey_rig_main" , "ceci est la tache rig") 
    core.hktask.createAssetTask(db, "testing_prp_mickey_mod_main" , "ceci est la tache mod")
    
    core.hktask.createAssetTask(db, "testing_env_mickey_srf_main" , "ceci est la tache srf") 
    core.hktask.createAssetTask(db, "testing_env_mickey_tex_main" , "ceci est la tache tex") 
    core.hktask.createAssetTask(db, "testing_env_mickey_rig_main" , "ceci est la tache rig") 
    core.hktask.createAssetTask(db, "testing_env_mickey_mod_main" , "ceci est la tache mod") 

    core.hktask.createShotTask(db, "testing_sq02_sh100_lit_main" , "ceci est la tache lit") 
    core.hktask.createShotTask(db, "testing_sq02_sh100_dmp_main" , "ceci est la tache dmp") 
    core.hktask.createShotTask(db, "testing_sq02_sh100_lay_main" , "ceci est la tache lay") 
    core.hktask.createShotTask(db, "testing_sq02_sh100_cam_main" , "ceci est la tache cam") 
    core.hktask.createShotTask(db, "testing_sq02_sh100_cmp_main" , "ceci est la tache cmp")
    
def testRepository():
    db = utils.dataBase.getDataBase()
    pushlit = '/homeworks/users/pixo/projects/testing/shots/sq02/sq02_sh100/sq02_sh100_lit/sq02_sh100_lit_main/litcaca.gproject'
    pushmod = '/homeworks/users/pixo/projects/testing/chr/chr_mickey/chr_mickey_mod/chr_mickey_mod_main/cacamodeling.1001.1000.exr'
    
    """WORKSPACE"""
    """AssetTask"""
    core.hkrepository.createWorkspace(db, "testing_chr_mickey_mod_main")
    """ShotTask"""
    core.hkrepository.createWorkspace(db, "testing_sq02_sh100_lit_main")
    
    """PUSH"""
    """Push modeling"""
    core.hkrepository.push(db, "testing_chr_mickey_mod_main", pushmod, "modeling")
    """Push lighting"""
    core.hkrepository.push(db, "testing_sq02_sh100_lit_main", pushlit, "lighting")
    
    """PULL"""
    """Pull modeling """
    core.hkrepository.pull(db, "testing_chr_mickey_mod_main")
    """Pull lighting """
    core.hkrepository.pull(db, "testing_sq02_sh100_lit_main")    

def testPush():
    db = utils.dataBase.getDataBase()
    filetopush = "/homeworks/users/pixo/projects/testing/shots/sq02/sq02_sh100/sq02_sh100_lit/sq02_sh100_lit_main/mylighting.gproject"
    core.hkrepository.push(db, "testing_sq02_sh100_lit_main", filetopush, "modeling")
    
def testPull():
    db = utils.dataBase.getDataBase()
    core.hkrepository.pull(db, "testing_sq02_sh100_lit_main")
    
# testAsset()
    
# testTask()
db = utils.dataBase.getDataBase()

testCreateWs()
# core.hkasset.lsAsset(db, "testing_chr_mickey")

