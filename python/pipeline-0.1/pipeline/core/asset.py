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

#TODO:create the all view
def lsAssets(db, entity_id):
    """
    List assets.
    db, type couch.db.Server
    entity id, type string
    """
    
    """Get datas from entity id"""
    entity_id = entity_id.split("_")
    project,assettype,asset = entity_id[0], entity_id[1], entity_id[2]
    
    """Create the patterns to filter the database documents"""
    startkey = u"%s_%s_%s" % ( project, assettype, asset )
    endkey = u"%s_%s_%s\u0fff" % ( project, assettype, asset )
    view = db.view ( "_design/%s/_view/%sByProjectAndName" % ( "cg_project", assettype ), startkey=startkey, endkey=endkey )
    
    """Iterate over all the collected assets type documents """
    assets = list()
    for row in view.rows:
        assets.append(row["value"]["name"])
        print row["value"]["name"]
        
    return assets

def createAsset( db, entity_id, description, doc=dict() ):
    """
    Create a asset.
    db, type couch.db.Server
    entity id, type string
    description, type string
    """
    
    """ Get datas from entity id """
    project, assettype, assetname = entity_id.split ( "_" )
    project_id = "%s" % project
    name = "%s_%s" % ( assettype, assetname )
    assetslist = lsAssets ( db, entity_id )
    
    """ Check the asset doesn't exist """
    if not ( name in assetslist ) :
        
        """ Create the asset structure """
        asset_doc = {
            "type" : assettype,
            "_id" : entity_id,
            "project_id" : project_id,
            "name" : name,
            "description" : description,
            "creator" : os.getenv ( "USER" ),
            "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.gmtime() ),
            "state" : "na"
        }
        asset_doc.update(doc)
        
        """Save data structure into the database """
        _id, _rev = db.save (asset_doc )
        print "createAsset: Added %r to project %r" % ( name , project )
        return True
    
    else:
        
        print "createAsset: %s already exist" % name
        return False