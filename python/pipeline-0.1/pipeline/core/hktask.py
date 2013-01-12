'''
Created on Jan 10, 2013

ASSET type list:
    character        : chr
    vehicle          : vcl
    prop             : prp
    environment      : env
    freetype         : ***

ASSET tasks:
    sculpting       :scp
    modeling        : mod    
    texturing       : tex
    rigging         : rig
    surfacing       : srf

SHOT tasks:
    layouting        : lay
    lighting         : lit
    compositing      : cmp
    matte-painting   : dmp
    cam              : cam

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
import os, time
import hkasset
import pipeline.utils.dataBase as dataBase
from pipeline.core import hkshot

def lsTask ( db, doc_id ):
    """Get datas from doc_id"""
    task = doc_id.split("_")[3]
    startkey = u"%s" % doc_id
    endkey = u"%s\u0fff" % doc_id
    return dataBase.lsDb(db, task, startkey, endkey)

def createAssetTask ( db="", doc_id="", description="", overdoc=dict() ):
    """
    Create a task.
    db, type couch.db.Server
    doc_id, type string
    description, type string
    """
    
    """ Get datas from doc_id """
    project, typ, asset, task, fork = doc_id.split ( "_" )
    asset_id = "%s_%s_%s" % ( project, typ, asset )
    name = "%s_%s_%s_%s" % ( typ, asset, task, fork )
    
    """ Check if the asset exist """
    asset_ls = hkasset.lsAsset ( db, doc_id )
    if not ("%s_%s" % ( typ, asset )) in asset_ls:
        print "createAssetTask: %s doesn't exist" % asset_id 
        return False
    
    """ Check the task doesn't exist """
    task_ls = lsTask ( db, doc_id )
    if not ( name in task_ls ) :
        
        """ Create the task structure """
        doc = {
            "file_system":"%s/%s_%s/%s_%s_%s/%s_%s_%s_%s" % (typ,typ,asset,typ,asset,task,typ,asset,task,fork),
            "type": "%s_%s" % (typ,task),
            "task": task,
            "_id": doc_id,
            "project_id": project,
            "asset_id": asset_id,
            "fork": fork,
            "name": name,
            "description": description,
            "versions": dict(),
            "creator": os.getenv ( "USER" ),
            "created": time.strftime ( "%Y %b %d %H:%M:%S", time.gmtime() ),
            "state":"na"
            }
        doc.update(overdoc)
        
        """Save data structure into the database """
        _id, _rev = db.save (doc )
        print "createAssetTask: Added %r to project %r" % ( name , project )
        return db[_id]
    
    else:
        
        print "createAssetTask: %s already exist" % name
        return False
    
def createShotTask ( db="", doc_id="", description="", overdoc=dict() ):
    """
    Create a task.
    db, type couch.db.Server
    doc_id, type string
    description, type string
    """
    
    """ Get datas from doc_id """
    project, seq, shot, task, fork = doc_id.split ( "_" )
    shot_id = "%s_%s_%s" % ( project, seq, shot )
    name = "%s_%s_%s_%s" % ( seq, shot, task, fork )
    
    """ Check if the shot exist """
    shot_ls = hkshot.lsShot(db, doc_id)
    if not ("%s_%s" % ( seq, shot )) in shot_ls:
        print "createShotTask: Shot %s_%s doesn't exist" % (seq, shot)
        return False
    
    """ Check the task doesn't exist """
    task_ls = lsTask ( db, doc_id )
    if not ( name in task_ls ) :
        
        """ Create the task structure """
        doc = {
            "file_system":"%s/%s/%s_%s/%s_%s_%s/%s_%s_%s_%s" % ("shots",seq,seq,shot,seq,shot,task,seq,shot,task,fork),
            "type": "%s_%s" % ("shot",task),
            "task": task,
            "_id": doc_id,
            "project_id": project,
            "shot_id": shot_id,
            "fork": fork,
            "name": name,
            "description": description,
            "versions": dict(),
            "creator": os.getenv ( "USER" ),
            "created": time.strftime ( "%Y %b %d %H:%M:%S", time.gmtime() ),
            "state":"na"
        }
        doc.update(overdoc)
        
        """Save data structure into the database """
        _id, _rev = db.save (doc )
        print "createShotTask: Added %r to project %r" % ( name , project )
        return db[_id]
    
    else:
        
        print "createShotTask: %s already exist" % name
        return False
    