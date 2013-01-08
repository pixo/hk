'''
Created on Jan 8, 2013

@author: pixo
'''

import os, time, shutil

def pull(db, entity_id, version="latest"):
    """Get the data from the repository """
    entity_doc = db[entity_id]
    entity_version_attr = entity_doc["version"]

    if version == "latest":
        version = len(entity_version_attr)
        
    source_path = entity_version_attr[str(version)]["path"]
    destination_path=source_path.replace ( "$HK_REPOSITORY_PATH", "$HK_USER_REPOSITORY_PATH" )
    
    """Expand paths"""
    source_path = os.path.expandvars(source_path)
    destination_path=os.path.expandvars(destination_path)
    
    if not os.path.exists(destination_path):
        shutil.copytree(source_path, destination_path)
        print "Pulled: %s" % destination_path
        return True
    else :
        print "File already exist, please rename or remove it : %s" % destination_path
        return False 

def push(db, entity_id, source_file,comments):
        
    """Put the data into the repository """
    entity_doc = db[entity_id]
    entity_version_attr = entity_doc["version"]
    version = len(entity_version_attr)+1
        
    destination_path = entity_id [ len ( "%s_" % os.getenv( "HK_PROJECT" ) ) : ]    #remove the project name from the entity_id
    destination_path = destination_path.replace ( "_", os.sep )
    destination_path = os.path.join ( "$HK_REPOSITORY_PATH", entity_doc["inherit"], destination_path, "v%03d" % version )
    destination_file = entity_id + os.path.splitext ( source_file )[-1]
    destination_full = os.path.join ( destination_path, destination_file )

    fileinfo = {"path":destination_path,
                "files":1,
              "comments":comments,
              "creator":os.getenv("USER"),
              "created":time.strftime("%Y %b %d %H:%M:%S", time.gmtime())}
    entity_version_attr[version] = fileinfo
    entity_doc["version"] = entity_version_attr
    
    destination_path = os.path.expandvars ( destination_path )
    destination_full = os.path.expandvars ( destination_full )
    
    if os.path.exists(source_file) and (not os.path.exists(destination_path)):
        os.makedirs(destination_path, 0775)
        shutil.copyfile(source_file, destination_full)
        db[entity_id] = entity_doc
        print "Pushed: %s" % destination_full
        return True
    else:
        return False
    