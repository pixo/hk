'''
Created on Jan 8, 2013

@author: pixo
'''
import os, time, shutil, hashlib
import pipeline.utils as utils
import pipeline.utils.dataBase as dataBase

def hashTime():
    sha1 = hashlib.sha1(str(time.time()))
    return sha1.hexdigest()
    
def hashFile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    
    try:
        sha1.update(f.read())
    finally:
        f.close()
        
    return sha1.hexdigest()

def compareHashFile( firstfile, secondfile ):
    if not (os.path.exists(firstfile) and os.path.exists(secondfile)) :
        return False
        
    if hashFile(firstfile) == hashFile(secondfile):
        return True
    
    else :
        return False

def getWorkspaceFromId(db = None, doc_id = ""):
    if db == None:
        db = utils.dataBase.getDataBase()
    
    doc = db[doc_id]
    path = doc [ "file_system" ].replace ( "/", os.sep )
    path = os.path.join ( os.getenv("HK_USER_REPOSITORY_PATH"), path )
    return path

def createWorkspace(db = None, doc_id = ""):
    """Create the entity directory in the user repository  """
    if db == None :
        db = dataBase.getDataBase()
        
    path = getWorkspaceFromId(db, doc_id)
    if os.path.exists(path):
        print("createWorkspace(): %s already exist" % path )
        return False
    
    os.makedirs(path, 0775)
    print("createWorkspace(): %s created" % path )
    return path

def getIdFromPath(db,user_file=""):
    """Get doc_id from path , firstly to push in cli """
    user_file = os.path.expandvars(user_file)
    user_repo = os.getenv ( "HK_USER_REPOSITORY_PATH" ) + os.sep
    user_file = user_file.replace ( user_repo , "" )
    user_file = user_file.replace ( user_file.split(os.sep)[0] + os.sep, "" )
    doc_id = "%s_%s" % ( os.getenv ( "HK_PROJECT" ), 
                         os.path.dirname ( user_file ).replace ( os.sep, "_" ) )
    
    if doc_id in db:
        return db [ doc_id ]
    else:
        print "getDocIdFromUserFile: doc_id not in db "
        return False
    
def getAssetPath ( db = None, doc_id = "", ver = "latest" ):
    doc = db [ doc_id ]
    ver_attr = doc [ "versions" ]
    """Check which version to import"""
    if ver == "latest" :
        ver = len ( ver_attr )
    return ver_attr[ str ( ver ) ] [ "path" ]

def pull( db = None, doc_id = "", ver = "latest", progressbar = False,
          msgbar = False ):
    
    """Get the files from the repository """
    if db == None:
        db = dataBase.getDataBase()
    
    """ Get asset files path """
    src = getAssetPath ( db, doc_id, ver )
    dst = src.replace ( "$HK_REPOSITORY_PATH", "$HK_USER_REPOSITORY_PATH" )
    """ Expand paths """
    src = os.path.expandvars ( src )
    dst = os.path.expandvars ( dst )
    
    if not os.path.exists ( dst ):
        os.makedirs(dst, 0775)
        
        lsdir = list()
        for root, subFolders, files in os.walk(src):
            for file in files:
                lsdir.append( os.path.join( root, file ) )
        
        progress_value = 0
        progress_step = 100.0 / len(lsdir) if len(lsdir) != 0 else 1
        
        for file in lsdir:
            fulldst = file.replace ( src, dst )
            dirname = os.path.dirname ( fulldst )
            
            if not os.path.exists ( dirname ):
                os.makedirs( dirname , 0775 )
                 
            shutil.copyfile( file, fulldst)
            msg = "Pulled: %s" % fulldst
            print msg 
            
            if msgbar :
                msgbar(msg)
                
            if progressbar :
                progress_value += progress_step
                progressbar.setProperty("value", progress_value)
            
        return True
    else :
        msg = "File already exist, please rename or remove it : %s" % dst
        if msgbar :
            msgbar(msg)
        print msg
        return False 

def push ( db = "", doc_id = "", src_ls = list(), description = "",
          progressbar = False, msgbar = False, rename = True):
    
    """
    push() Put the datas into the repository 
    db, type couch.db.Server
    doc_id, type string
    src_ls, type list of string
    description, type string
    """
        
    """ Check the src_ls type is a list """
    if type ( src_ls ) == str :
        src_ls = list ( [ src_ls ] )
                
    """ check if the source file exists in the repository """
    file_list = list()
    for src in src_ls :
        if os.path.exists ( src ) :
            file_list.append(src)
        else:
            print "Warning: %s doesn't exist" % src
            
    """ Get a copy of the document to work on """
    fs = db [ doc_id ][ "file_system" ]
    
    """ Get root destination directory to push files """
    dst_dir =os.path.join ( "$HK_REPOSITORY_PATH", fs )
    dst_dir = dst_dir.replace ( "/", os.sep )
    
    """ Get temporary destination directory to push files """
    tmp_dir = os.path.expandvars(dst_dir)
    tmp_dir = os.path.join ( tmp_dir, str( hashTime () ) )
            
    """ Copy all the files in the destination directory """
    progress_value = 0
    progress_step = 100.0/len(file_list)
    files_attr = list()
    wspace = getWorkspaceFromId(db, doc_id)
            
    """ Iterate over all the provided source files """
    for src in file_list :
        """ Because some peoples use to name directories with points """
        file_space = os.path.dirname( src )
        file_space = file_space.replace( wspace, "" )
        file_name =  os.path.join( file_space, os.path.basename ( src ) )
         
        """ Get extension(s) ,UDIMs and frames are commonly separated 
            with this char """
        file_ext = file_name.replace(file_name.split(".")[0],"")
         
        """ Creating the full file name """
        if rename:
            dst_file = doc_id + file_ext
        else:
            dst_file = file_name
             
        if dst_file[0] == os.sep :
            dst_file = dst_file[1:]
            
        tmp_file = os.path.join ( tmp_dir, dst_file )
                      
        dirname = os.path.dirname(tmp_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
         
        shutil.copy( src, tmp_file )
        msg = "%s" % tmp_file
         
        """ Store the name for the database so we avoid to call 
            the database for each source file """
        files_attr.append ( dst_file )
        
        
        if progressbar :
            progress_value += progress_step
            progressbar.setProperty("value", progress_value)
            
        if msgbar :
            msgbar(msg)
            
    """ Get latest version number because somebody may push a new version 
        during the process """
    doc = db [ doc_id ]
    ver_attr = doc [ "versions" ]
    ver = len ( ver_attr ) + 1
    path_attr = os.path.join ( dst_dir, "%03d" % ver )
    repo = os.path.expandvars ( path_attr )
    """Rename the temp dir"""
    os.rename( tmp_dir, repo ) 
    
    """ Create the new version data for the "versions" document's attribute """
    fileinfo = {
                "creator" : os.getenv ( "USER" ),
                "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.gmtime()),
                "description" : description ,
                "path" : path_attr ,
                "files" : files_attr
                }
    
    """ Append the data into the document version attribute copy """
    ver_attr [ ver ] = fileinfo
     
    """ Replace the original "versions" attribute by our modified version """
    doc [ "versions" ] = ver_attr
    
    """ Push the info into the db """
    db [ doc_id ] = doc
    
    """ print published file for the user"""
    for file in files_attr:
        print os.path.join( repo , file)
        
    return True