import pipeline.utils as utils
import os

def get_sync_tasks ( sync_args ) :
    args = sync_args.split (",")

    if "all" in args :
        return list ()
    
    """Get tasks code"""
    at = utils.getAssetTasks ()
    tasks = list ()
    for k in at : tasks.append ( at [ k ] )

    """Check args and return the task code to sync"""
    result = tasks

    for a in args :
        """ append legal tasks """
        if a in tasks :
            result.remove ( a )

    return result

def hk_rsync ( source = "", destination = "", excludes = list (), dev = None ):
    """Check if update codes or projects"""
    
    if dev and bool ( int ( dev ) ) :
        category = "codes"
        source = os.path.join ( source, category )
        destination = os.path.join ( destination ) 

    else:
        category = "projects"
        directory = utils.getProjectName ()
        source = os.path.join ( source, category, directory ) 
        destination = os.path.join ( destination, category )
    
    cmd = utils.rsync ( source = source, destination = destination, excludes = excludes )
    return cmd

def cli ( sync, push, pull, dev ):

    local_root = utils.getLocalRoot ()
    host_root = utils.getHostRoot ()
    
    if sync :
        excludes = get_sync_tasks ( sync )
        """Pushing"""
        cmd = hk_rsync ( source = local_root, destination = host_root, excludes = excludes, dev = dev )
        # os.system ( cmd )
        print cmd

        """Pulling"""
        cmd = hk_rsync ( source = host_root, destination = local_root, excludes = excludes, dev = dev )
        # os.system ( cmd )
        print cmd

    if push :
        excludes = get_sync_tasks ( push )
        """Pushing"""
        cmd = hk_rsync ( source = local_root, destination = host_root, excludes = excludes, dev = dev )
        # os.system ( cmd )
        print cmd

    if pull :
        excludes = get_sync_tasks ( pull )
        """Pulling"""
        cmd = hk_rsync ( source = host_root, destination = local_root, excludes = excludes, dev = dev )
        # os.system ( cmd )
        print cmd
        
sync = "all"
push = None
pull = None
dev = 1

cli ( sync, push, pull, dev )