'''
Created on Jan 8, 2013

@author: pixo
'''
import os, time, shutil, hashlib
import pipeline.utils as utils
import pipeline.utils.dataBase as dataBase

def hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    
    try:
        sha1.update(f.read())
    finally:
        f.close()
        
    return sha1.hexdigest()

def comparefile( firstfile, secondfile ):
    
    if not (os.path.exists(firstfile) and os.path.exists(secondfile)) :
        return False
        
    if hashfile(firstfile) == hashfile(secondfile):
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
    
def pull( db = None, doc_id = "", ver = "latest", progressbar = False, msgbar = False ):
    """Get the files from the repository """
    if db == None:
        db = dataBase.getDataBase()
    
    doc = db [ doc_id ]
    ver_attr = doc [ "versions" ]
    
    """Check which version to import"""
    if ver == "latest" :
        ver = len ( ver_attr )
        
    src = ver_attr[ str(ver) ] [ "path" ]
    dst = src.replace ( "$HK_REPOSITORY_PATH", "$HK_USER_REPOSITORY_PATH" )
    
    """Expand paths"""
    src = os.path.expandvars ( src )
    dst = os.path.expandvars ( dst )
    
    if not os.path.exists ( dst ):
        os.makedirs(dst, 0775)
        lsdir = os.listdir(src)
        progress_value = 0
        progress_step = 100.0/(len(lsdir))
        
        for file in lsdir:
            fulldst = os.path.join(dst,file)
            shutil.copyfile(os.path.join(src,file),
                            fulldst)
            msg = "Pulled: %s" % fulldst
            print msg 
            if msgbar :
                msgbar(msg)
            if progressbar :
                progress_value += progress_step
                progressbar.setProperty("value", progress_value)
            
#         shutil.copytree ( src, dst, ignore = shutil.ignore_patterns('*.sha1') )
        return True
    else :
        msg = "File already exist, please rename or remove it : %s" % dst
        if msgbar :
            msgbar(msg)
        print msg
        return False 

def push( db = "", doc_id = "", src_ls = list(), description = "",
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
    """ Get a copy of the document to work on """
    doc = db [ doc_id ]
    wspace = getWorkspaceFromId(db, doc_id) + os.sep
    
    """ Get a copy of the copied document "versions" attribute """
    ver_attr = doc [ "versions" ]
    ver = len ( ver_attr ) + 1
    
    """ Create the path name where to push to file into the repo"""
    dst_dir = doc [ "file_system" ].replace ( "/", os.sep )
    path_attr = os.path.join ( "$HK_REPOSITORY_PATH", dst_dir, "%03d" % ver )
    dst_dir = os.path.expandvars(path_attr)
    
    if ver > 1:
        prev_dst_path = doc [ "versions" ][ str( ver-1 ) ]["path"]
        prev_dst_path = os.path.expandvars ( prev_dst_path )
        
    if os.path.exists ( dst_dir ):
        print "%s already exist please remove it and try again." % dst_dir
        return False
    
    files_attr=list()    
    push_dict = diff_dict = dict()
           
    """ Iterate over all the provided source files """
    for src in src_ls :
        
        """ check if the source file exists in the repository """
        if os.path.exists ( src ) :
            
            """ Because some peoples use to name directories with points """
            file_space = os.path.dirname( src ).replace( wspace, "" )
            file_name =  os.path.join( file_space, os.path.basename ( src ) )
            
            """ Get extension(s) ,UDIMs and frames are commonly separated 
                with this char """
            file_ext = file_name.replace(file_name.split(".")[0],"")
            
            """ Creating the full file name """
            if rename:
                dst_file = doc_id + file_ext
            else:
                dst_file = file_name
                
            dst = os.path.join ( dst_dir, dst_file )
            
            """ If ver > 1 then compare the last version to the current """
            same = False
            if ver > 1:
                    prev_dst = os.path.join ( prev_dst_path, dst_file )
                    same = comparefile( src, prev_dst )
            
            """ If there is no difference between the latest version
                put it in the same dict """
            if not same :
                diff_dict[src] = dst
            else:
                print "Same file : \n %s\n%s\n" % (src,prev_dst)
                            
            push_dict[src] = dst

            """ Store the name for the database so we avoid to call 
                the database for each source file """
            files_attr.append ( dst_file )
            
        else:
            print "Warning: %s doesn't exist" % src
            return False
    
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
    
    """ Copy the data into the repository """
    
    """ If there's no file to copy then no need to push """
    if len(diff_dict) == 0 :
        print "push(): no changes between version or no files to push"
        return False
    
    progress_value = 0
    progress_step = 100.0/(len(push_dict))

    """Copy the data to the repository"""
    os.makedirs ( dst_dir, 0775 )
    print "push():"
    for key in push_dict:
        if progressbar :
            progress_value += progress_step
            progressbar.setProperty("value", progress_value)
            
        dirname = os.path.dirname(push_dict[key])
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        
        shutil.copy( key, push_dict[key] )
        msg = "%s" % push_dict[key]
        print msg
        if msgbar :
            msgbar(msg)
    
    print progress_value
    """ Push the info into the db """
    db [ doc_id ] = doc
    
    return True
