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
    entity_version_attr = entity_doc [ "versions" ]
    
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
    
    #Get a copy of the document to work on
    entity_doc = db [ entity_id ]
    
    #Get a copy of the copied doccument "versions" attribute
    entity_version_attr = entity_doc [ "versions" ]
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
        print "%s already exist please remove it and try again." % expanded_destination_path
        return False
    
    os.makedirs ( expanded_destination_path, 0775 )
    destination_file_list=list()
    
    #iterate over all the provided source files
    for source_file in source_files_list :
        
        #check if the source file exists in the repository
        if os.path.exists ( source_file ) :
            
            #Because some peoples use to name directories with points
            file_name = os.path.basename(source_file)
            
            #Get extension(s) ,UDIMs and frames are commonly separated with this char
            file_ext = file_name.replace(file_name.split(".")[0],"")
            
            #Creating the full file name
            destination_file = entity_id + file_ext
            destination_full = os.path.join ( expanded_destination_path, destination_file )
            
            #Store the name for the database so we avoid to call the database for each source file
            destination_file_list.append ( destination_file )
    
            #Copy the data into the repository
            shutil.copyfile ( source_file, destination_full )
            print "Pushed: %s" % destination_full
            
        else:
            #TODO:Add an exception here
            print "Error:s% doesn't exist" % source_file
            return False
        
    #Create the new version data for the "versions" document's attribute 
    fileinfo = {
                "creator" : os.getenv ( "USER" ),
                "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.gmtime() ),
                "comments" : comments ,
                "path" : destination_path ,
                "files" : destination_file_list
                }
    
    #Append the data into the document version attribute copy
    entity_version_attr [ version ] = fileinfo
    
    #Replace the original "versions" attribute by our modified version
    entity_doc [ "versions" ] = entity_version_attr
    
    #Push the info into the db
    db [ entity_id ] = entity_doc
    
    return True
