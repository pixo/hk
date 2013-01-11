'''
Created on Jan 10, 2013

ASSET tasks:
    modeling        : mod    
    texturing         : tex
    rigging         : rig
    surfacing        : srf
    layouting        : lay
    lighting         : lgt
    compositing        : cmp
    matte-painting     : dmp

ASSET type list:
    character        : chr
    vehicle            : vcl
    prop             : prp
    environment     : env
    ??? camera            : cam ??? not sure about this let see later
    freetype         : ***

Filename and id rules:
    project_asset-type_asset_task_fork
    
    project_id = project
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
import asset

def lsTasks(db, entity_id):
    """
    List tasks.
    db, type couch.db.Server
    entity id, type string
    """
    
    """Get datas from entity id"""
    #project,assettype,assetname,task,fork= entity_id.split("_")
    task = entity_id.split("_")[3]
    
    """Create the patterns to filter the database documents"""
    startkey = u"%s" % entity_id
    endkey = u"%s\u0fff" % entity_id
    view = db.view ( "_design/%s/_view/%sByProjectAndName" % ( "cg_project", task ), startkey=startkey, endkey=endkey )
    
    """Iterate over all the collected tasks type documents """
    tasks = list()
    for row in view.rows:
        tasks.append(row["value"]["name"])
        print row["value"]["name"]
        
    return tasks

def createTask( db="", entity_id="", description="", doc=dict(),fssuffix="" ):
    """
    Create a task.
    db, type couch.db.Server
    entity id, type string
    description, type string
    """
    
    """ Get datas from entity id """
    project, assettype, assetname, task, fork = entity_id.split ( "_" )
    project_id = "%s" % project
    asset_id = "%s_%s_%s" % ( project, assettype, assetname )
    asset_name = "%s_%s" % ( assettype, assetname )
    name = "%s_%s_%s_%s" % ( assettype, assetname, task, fork )
    taskslist = lsTasks ( db, entity_id )
    asset_list = asset.lsAssets(db, entity_id)
    
    """ Check if the asset exist """
    if not asset_name in asset_list:
        print "createTask: %s doesn't exist" % asset_id 
        return False
    
    """ Check the task doesn't exist """
    if not ( name in taskslist ) :
        
        """ Create the task structure """
        task_doc = {
            "file_system":"%s%s/%s_%s/%s_%s_%s/%s_%s_%s_%s" % (fssuffix,assettype,assettype,assetname,assettype,assetname,task,assettype,assetname,task,fork),
            "type": task,
            "_id": entity_id,
            "project_id": project_id,
            "asset_id": asset_id,
            "fork": fork,
            "name": name,
            "description": description,
            "versions": dict(),
            "creator": os.getenv ( "USER" ),
            "created": time.strftime ( "%Y %b %d %H:%M:%S", time.gmtime() ),
            "inherit": "%s" % assettype,
            "state":"na"
        }
        task_doc.update(doc)
        
        """Save data structure into the database """
        _id, _rev = db.save (task_doc )
        print "createTask: Added %r to project %r" % ( name , project )
        return True
    
    else:
        
        print "createTask: %s already exist" % name
        return False
    
