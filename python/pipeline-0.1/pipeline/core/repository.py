'''
Created on Jan 8, 2013

@author: pixo
'''
import os, time, shutil, hashlib, re, glob, commands
import pipeline.utils as utils
import pipeline

def hashTime () :
    sha1 = hashlib.sha1 ( str ( time.time () ) )
    return str ( sha1.hexdigest () )
     
def hashFile ( filepath ) :
    sha1 = hashlib.sha1 ()
    f = open ( filepath, 'rb' )
     
    try:
        sha1.update ( f.read () )
    finally:
        f.close ()
         
    return sha1.hexdigest ()
 
def compareHashFile( firstfile, secondfile ):
    if not ( os.path.exists ( firstfile ) and os.path.exists ( secondfile ) ) :
        return False
         
    if hashFile ( firstfile ) == hashFile ( secondfile ):
        return True
     
    else :
        return False
 
def getIdFromPath ( path = "" ):
    """Get doc_id from path , firstly to push in cli """
    path = os.path.expandvars(path)
    user_repo = os.getenv ( "HK_USER_REPO" ) + os.sep
    path = path.replace ( user_repo , "" )
    part = path.split ( os.sep )
    doc_id = "%s_%s_%s_%s_%s" % ( part[0],part[1], part[2], part[3], part[4] )
    return doc_id
     
def getRootAssetPath ( doc_id = "", local = False):
    """Return root path of an asset from the doc_id"""
    path = doc_id.replace ( "_", os.sep )
    if local :
        root = os.getenv ( "HK_USER_REPO" )
    else:
        root = os.getenv ( "HK_REPO" )
        
    path = os.path.join ( root, path )
    return path
    
def getAssetVersions ( doc_id = "" ):
    path = getRootAssetPath ( doc_id )
    versions = glob.glob ( path + os.sep +"[0-9][0-9][0-9]" )
    versions.sort ()
    return versions

def getAssetTypeFromId ( doc_id ):
    return doc_id.split("_")[1]

def getAssetTaskFromId ( doc_id ):
    return doc_id.split("_")[3]

def getIdFromPushedFile ( fname ):
    basename = os.path.basename ( fname )
    doc_id = os.path.splitext ( basename )[0]
    return doc_id

def getAssetPath ( doc_id = "", version = "last" ):
    if version == "last" :
        version = getAssetVersions ( doc_id = doc_id )
        version = version[-1]
         
    path = getRootAssetPath ( doc_id = doc_id, local = False )
    path = os.path.join ( path, "%03d" % float ( version ) )
    return path

def getAssetLocalPath ( doc_id = "", version = 1 ):
    count = 1
    fdir = getRootAssetPath ( doc_id, True )
    name = "%s.v%03d.base" % ( doc_id, version )
    dst = os.path.join ( fdir, name ) 
    
    while os.path.exists ( dst ) :
        dst = os.path.join ( fdir, name + str ( count ) )
        count += 1
    
    return dst

def getWorkspaceFromId ( doc_id = "" ):
    """Get user asset workspace from doc_id"""
    path = getRootAssetPath ( doc_id, True )
    return path
 
def createWorkspace( doc_id = ""):
    """Create the entity directory in the user repository  """
    path = getWorkspaceFromId ( doc_id )
    if os.path.exists ( path ) :
        print ( "createWorkspace(): %s already exist" % path )
        return False
    
    os.makedirs ( path, 0775 )
    print ( "createWorkspace(): %s created" % path )
    return path

def transfer ( sources = list(), destination = "", doc_id = "", rename = True ) :
    """ Check the src_ls type is a list """
    if type ( sources ) == str :
        sources = list ( [ sources ] )
                 
    """ check if the source file exists in the repository """
    files = dict()
    
    for src in sources :
        
        if os.path.exists ( src ) :
            basename = os.path.basename ( src )
            filename = basename.replace ( basename.split(".")[0], doc_id )
            files [src] = os.path.join ( destination, filename )
        else:
            print "Warning: %s doesn't exist" % src
    
    os.system( "chmod 775  %s" % destination )
    for fil in files:                
        dirname = os.path.dirname ( files [ fil ] )
        if not os.path.exists ( dirname ) :
            os.makedirs ( dirname )
        shutil.copy ( fil, files [ fil ] )
    os.system( "chmod -R 555  %s" % destination )
        
def pull ( doc_id = "", ver = "latest", extension = "", progressbar = False,
           msgbar = False ):
     
    """Get the files from the repository """
    """Check id"""
    docsplit = doc_id.split("_")
    if len ( docsplit ) < 5:
        print "pull(): Wrong asset id"
        return False
    
    """ Get asset local, network path """
    src = getAssetPath ( doc_id = doc_id, version = ver )
    dst = getAssetLocalPath ( doc_id = doc_id, version = ver)
         
    if not os.path.exists ( dst ):
        os.makedirs ( dst, 0775 )
         
        lsdir = list()
        for root, subFolders, files in os.walk(src):
            for file in files:
                lsdir.append ( os.path.join ( root, file ) )
         
        progress_value = 0
        progress_step = 100.0 / len(lsdir) if len(lsdir) != 0 else 1
         
        pulled = list()
        for file in lsdir:
            fulldst = file.replace ( src, dst )
            dirname = os.path.dirname ( fulldst )
             
            if not os.path.exists ( dirname ):
                os.makedirs( dirname , 0775 )
                  
            if extension != "":
                if os.path.splitext ( fulldst )[-1] == extension:
                    shutil.copyfile( file, fulldst)
                    pulled.append(fulldst)
                    msg = "Pulled: %s" % fulldst
                    print msg
                    if msgbar :
                        msgbar(msg)
                    
            else:
                shutil.copyfile ( file, fulldst )
                pulled.append ( fulldst )
                msg = "Pulled: %s" % fulldst
                
                print msg
                if msgbar :
                    msgbar(msg)
                             
            if progressbar :
                progress_value += progress_step
                progressbar.setProperty("value", progress_value)
             
        return pulled
    
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
              
    """ Get root destination directory to push files """
    dst_dir = getRootAssetPath ( doc_id )
     
    """ Get temporary destination directory to push files """
    tmp_dir = os.path.join ( dst_dir, hashTime () )
             
    """ Copy all the files in the destination directory """
    progress_value = 0
    progress_step = 100.0/len ( file_list )
    files_attr = list ()
    wspace = getWorkspaceFromId ( doc_id )
             
    """ Iterate over all the provided source files """
    for src in file_list :
        """Get file dir"""
        file_space = os.path.dirname ( src )
        """file space in case we need to publish directories """
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
        
        """ Store the files names in a list to avoid to call 
            the database for each source file """
        files_attr.append ( dst_file )
                    
        """Create temporary directory"""
        dirname = os.path.dirname ( tmp_file )
        if not os.path.exists ( dirname ):
            os.makedirs(dirname)
        
        """Copy files to temporary directory"""  
        shutil.copy ( src, tmp_file )
                            
        if progressbar :
            progress_value += progress_step
            progressbar.setProperty ( "value", progress_value )
        else :
            print progress_value 
             
        if msgbar :
            msgbar ( dst_file )
             
    """ Get latest version """
    doc = db [ doc_id ]
    ver_attr = doc [ "versions" ]
    ver = len ( ver_attr ) + 1
    path_attr = os.path.join ( dst_dir, "%03d" % ver )
    repo = os.path.expandvars ( path_attr )
    
    """Rename the temp dir"""
    os.rename( tmp_dir, repo )
    os.system( "chmod -R 555  %s" % repo )
         
    """ Create the new version data for the "versions" document's attribute """
    fileinfo = {
                "creator" : os.getenv ( "USER" ),
                "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.localtime()),
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
         
    """Return the published directory"""
    return repo

def pushDir ( db = "", doc_id = "", path = list(), description = "" ):
     
    """
    push() Put the datas into the repository 
    db, type couch.db.Server
    doc_id, type string
    path, directory
    description, type string
    """
                          
    """ check if the source file exists in the repository """
    if not os.path.exists ( path ) :
        print "pushDir(): %s doesn't exist" % path
        return False
    
    """ Get root destination directory to push files """
    dst_dir = getRootAssetPath ( doc_id )
     
    """ Get temporary destination directory to push files """
    tmp_dir = os.path.join ( dst_dir, hashTime () )
    os.makedirs ( tmp_dir )
    
    """ Copy all the files in the destination directory """
    files_attr = list ()
    file_list = os.listdir ( path )
    
    for src in file_list :
        """file space in case we need to publish directories """
        path_src =  os.path.join ( path, src )                           
        dst = os.path.join ( tmp_dir, src )
                                
        if os.path.isfile ( path_src ):
            print  "pushDir(): copying file %s " % src
            shutil.copy ( path_src, dst )
        elif os.path.isdir ( path_src ):
            print  "pushDir(): copying directory %s " % src
            shutil.copytree ( path_src, dst )
          
        """ Store the files names in a list to avoid to call 
            the database for each source file """
        files_attr.append ( src )
             
    """ Get latest version number because somebody may push a new version 
        during the process """
    doc = db [ doc_id ]
    ver_attr = doc [ "versions" ]
    ver = len ( ver_attr ) + 1
    path_attr = os.path.join ( dst_dir, "%03d" % ver )
    repo = os.path.expandvars ( path_attr )
    """Rename the temp dir"""
    os.rename ( tmp_dir, repo )
    os.chmod( repo, 0555)
         
    """ Create the new version data for the "versions" document's attribute """
    fileinfo = {
                "creator" : os.getenv ( "USER" ),
                "created" : time.strftime ( "%Y %b %d %H:%M:%S", time.localtime()),
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
         
    """Return the published directory"""
    return repo

def pushFile ( db = "", doc_id = False, path = list (), description="", rename = True ):
     
    if db == None :
        db = utils.getDb()
         
    if type ( path ) == str:
        path = list ( [ path ] )

    if not doc_id:
        doc_id = getIdFromPath ( path[0] )
    
    return push ( db = db , doc_id = doc_id , src_ls = path ,
                  description =  description, progressbar = False,
                  msgbar = False, rename = rename )

def getTextureAttr ( path ):
    textureType = utils.getTextureTypes()
    fname = os.path.basename ( path )
    
    for typ in textureType :
        simpTex = "%s\d*.\d\d\d\d." % typ
        animTex = "%s\d*.\d\d\d\d.\d\d\d\d." % typ
        pattern = "%s|%s" % ( simpTex, animTex )
        
        if len ( re.findall ( pattern, fname ) ):
            return ( typ, textureType[typ] )
        
    return ( False, False )

def textureBuild ( path = "", mode = "ww", texfilter = None ):
    """Guerilla texture build"""
    
    #TODO: Add Gamma support
    if texfilter == None :
        if mode == "latlong":
            texfilter = "triangle"
        
        else:
            texattr = getTextureAttr ( path )[1]
            
            if not texattr :  
                return False
            
            texfilter = texattr[4]
            texgamma = texattr[5]
        
    file, ext = os.path.splitext ( path )
    tex = file + ".tex"
    
    cmd = """render --buildtex --in %s --mode %s --filter %s --out %s""" % ( path, mode, texfilter, tex )
    os.system ( cmd )
    print "buildtex: building %s" % tex
    return True
   
def textureOptimise ( path ):
    
    fname = os.path.basename(path)
    texattr = getTextureAttr ( path )[1]
    
    if texattr :
        #Default texture attributes
        texchannel = texattr[0]
        texdepth = texattr[1]
        texbgcolor = texattr[2]
        texcompress = texattr[3]
        texfilter = texattr[4]
        
        #Current image attributes
        cmd_identify = "identify %s" % path
        imgattr = commands.getoutput ( cmd_identify ).split("\n")[-1]
        imgattr = imgattr.split(" ")
        imgdepth = imgattr[4]
        imgformat = imgattr[1]
        imgres = imgattr[2]
        
        if texcompress :
            cmd_compress = "mogrify -compress Zip %s" % path
            os.system(cmd_compress)
            print "compress 'Deflate': %s" % fname
            
        elif texbgcolor != "" :
            cmd_alpharm = """mogrify -background "%s" -flatten +matte %s""" % ( path, texbgcolor )
            os.system(cmd_alpharm)
            print "remove alpha: %s" % fname
            
        if texchannel == "R" : 
            cmd_channel = "mogrify -channel R -separate %s" % path
            os.system(cmd_channel)
            print "grayscale: %s" % fname
             
        if texdepth.find(imgdepth) < 0 : 
            print "warning: wrong depth '%s', %s should be '%s'  " % ( imgdepth, fname, texdepth )
            
        #TODO:check if tiff format warning is working
        if imgformat != "TIFF":
            print "warning: wrong format '%s', %s should be '%s'  " % ( imgformat, fname, "TIFF" )
                 
    else:
        print "Can't find the '%s' texture type" % fname
    
def textureExport ( path = "", progressbar = False ):
    files = glob.glob ( os.path.join ( path, "*.tif" ) )
    #TODO: support progressbar for textures optimisation
    for file in files :
        textureOptimise ( file )
        textureBuild ( file )
        
    return True

def textureCheck ( doc_id = "", files = list() ) :
    textureType = utils.getTextureTypes ()
    not_pushed = list ( files )
        
    for file in files :
        fname = os.path.basename ( file )
        
        for typ in textureType :
            simpTex = "%s_\d*_%s\d*.\d\d\d\d." % ( doc_id, typ )
            simpTex = simpTex + "tif|" + simpTex + "exr"
            animTex = "%s_\d*_%s\d*.\d\d\d\d.\d\d\d\d." % ( doc_id, typ )
            animTex = animTex + "tif|" + animTex + "exr"
            pattern = "%s|%s" % ( simpTex, animTex )
                        
            if re.findall ( pattern, fname ):
                """check if the textures are builded"""
                texfile = ""
                fext = fname.split (".")[-1]
                                
                if fext != "tex":
                    for ext in ( "tif", "exr" ):
                        if fext == ext:
                            texfile = file.replace ( ".%s" % ext, ".tex" )
                        
                    if os.path.exists ( texfile ):
                        not_pushed.remove ( file )
                        not_pushed.remove ( texfile )  
                        print "textureCheck: %s OK" % fname
                    
                    else:
                        print "textureCheck: missing .tex for %s" % fname

    return not_pushed

def texturePush ( db = None, doc_id = "", path = "", description = "",
                  progressbar = False, msgbar = False, rename = False ) :
    
    lsdir = os.listdir ( path )
    files = list ()
    
    for file in lsdir:
        base, ext = os.path.splitext ( file )        
        
        if ext != ".mra":
            files.append ( os.path.join ( path, file ) )
        
        else:
            if not ( file.find ( doc_id ) == 0 ) :
                print file, "should begin with %s" % doc_id
                return 1
                
    texCheck = textureCheck ( doc_id, files )
    
    if len ( texCheck ) == 0 :  
        pushed = pushDir ( db, doc_id, path, description )        
        return pushed
    
    else :
        for tex in texCheck :
            print ( "texturePush(): %s is wrong" % tex )
            
        simptex = "%s_%s_%s.%s.%s" % ( doc_id, "<variation>", "<type>", "<udim>", "tif" )
        animtex = "%s_%s_%s.%s.%s.%s" % ( doc_id, "<variation>", "<type>", "<udim>","<frame>", "tif")
        print "texturePush(): expect %s or %s " % ( simptex , animtex)
        
        return False
       