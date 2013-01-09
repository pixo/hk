'''
Created on Jan 8, 2013

@author: pixo
'''
import os, time, shutil

#TODO:make a general cleaning (c'est caca ! )

def getIdFromPath(db,userFile=""):
    """Get doc_id from path , firstly to push in cli """
    
    userFile = os.path.expandvars(userFile)
    userRepository = os.getenv ( "HK_USER_REPOSITORY_PATH" ) + os.sep
    userFile = userFile.replace ( userRepository , "" )
    userFile = userFile.replace ( userFile.split(os.sep)[0] + os.sep, "" )
    doc_id = "%s_%s" % ( os.getenv ( "HK_PROJECT" ), os.path.dirname ( userFile ).replace ( os.sep, "_" ) )    #basename(userFile)
    
    if doc_id in db:
        print doc_id 
        return db [ doc_id ]
    
    else:
        print "getDocIdFromUserFile: doc_id not in db "
        return False
    
def pull(db, entity_id, version="latest"):
    """Get the data from the repository """
    
    entity_doc = db [ entity_id ]
    entity_version_attr = entity_doc [ "version" ]
    
    if version == "latest" :
        version = len ( entity_version_attr )
        
    source_path = entity_version_attr[ str(version) ] [ "path" ]
    destination_path = source_path.replace ( "$HK_REPOSITORY_PATH", "$HK_USER_REPOSITORY_PATH" )
    
    """Expand paths"""
    source_path = os.path.expandvars ( source_path )
    destination_path = os.path.expandvars ( destination_path )
    
    if not os.path.exists ( destination_path ):
        shutil.copytree ( source_path, destination_path )
        print "Pulled: %s" % destination_path
        return True
    else :
        print "File already exist, please rename or remove it : %s" % destination_path
        return False 

def push( db, entity_id, source_file, comments ):
    """Put the datas into the repository """
    
    entity_doc = db [ entity_id ]
    entity_version_attr = entity_doc [ "version" ]
    version = len ( entity_version_attr ) + 1
    
    if type(source_file) == str:
        source_files_list = list({source_file})
    else:
        source_files_list = source_file
            
    destination_path = entity_id [ len ( "%s_" % os.getenv( "HK_PROJECT" ) ) : ]    #remove the project name from the entity_id
    destination_path = destination_path.replace ( "_", os.sep )
    destination_path = os.path.join ( "$HK_REPOSITORY_PATH", entity_doc["inherit"], destination_path, "v%03d" % version )    
    expanded_destination_path = os.path.expandvars ( destination_path )
      
    if os.path.exists ( expanded_destination_path ):
        return False
    
    os.makedirs ( expanded_destination_path, 0775 )
    destination_file_list=list()
    
    for source_file in source_files_list :
        file_name = os.path.basename(source_file)#Because some peoples use to name directories with points
        file_ext = file_name.replace(file_name.split(".")[0],"")#Get extension , textures UDIMs and frames a separated with a point
        
        destination_file = entity_id + file_ext
        destination_file_list.append(destination_file)
        destination_full = os.path.join ( expanded_destination_path, destination_file )
        
        if os.path.exists ( source_file ) :
            shutil.copyfile ( source_file, destination_full )
            print "Pushed: %s" % destination_full
        
        else:
            #TODO:Add an exception here
            print "Something wrong:s% doesn't exist" % source_file
            return False
    
    fileinfo = {
                "creator" : os.getenv ( "USER" ),
                "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.gmtime() ),
                "comments" : comments ,
                "path" : destination_path ,
                "files" : destination_file_list
                }

    entity_version_attr [ version ] = fileinfo
    entity_doc [ "version" ] = entity_version_attr
    db [ entity_id ] = entity_doc
    return True
