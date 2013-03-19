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
import pipeline.utils as utils

def createTask ( db = None, doc_id = "", description = "", overdoc = dict() ):
    """
    Create a task.
    db, type couch.db.Server
    doc_id, type string
    description, type string
    """
    
    if db == None:
        db = utils.getDb()
        
    """ Get datas from doc_id """
    project, typ, asset, task, fork = doc_id.split ( "_" )
    asset_id = "%s_%s_%s" % ( project, typ, asset )
    name = "%s_%s_%s_%s" % ( typ, asset, task, fork )
        
    """ Check if the asset exist """
    asset_ls = utils.lsDb ( db, typ, asset_id )
    
    if not ("%s_%s" % ( typ, asset )) in asset_ls:
        print "createTask: %s doesn't exist" % asset_id 
        return False
    
    """ Check the task doesn't exist """
    task_ls = utils.lsDb ( db, task, doc_id )
    
    if not ( name in task_ls ) :
        """ Create the task structure """
        
        doc = {
            "type" : "%s_%s" % (typ,task),
            "task" : task,
            "_id" : doc_id,
            "project_id" : project,
            "asset_id" : asset_id,
            "fork" : fork,
            "name" : name,
            "description" : description,
            "versions" : dict(),
            "creator" : os.getenv ( "USER" ),
            "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.localtime() ),
            "state" : "na"
            }
        doc.update(overdoc)
        
        """Save data structure into the database """
        _id, _rev = db.save (doc )
        
        print "createTask: Added %r to project %r" % ( name , project )
        return db[_id]
    
    else:
        print "createAssetTask: %s already exist" % name
        return False
