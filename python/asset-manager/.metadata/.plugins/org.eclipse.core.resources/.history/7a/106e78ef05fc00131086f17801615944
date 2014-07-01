'''
Created on Jan 8, 2013

@author: pixo
'''

import os, time, shutil, re, commands, glob
import badass.utils as utils

class RepositoryError ( Exception ):
    """
    Error raised by the repository module.
    
    """

    def __init__ ( self, value ):
        self.value = value
    def __str__ ( self ):
        return repr ( self.value )

def getIdFromFile ( path = "" ):
    """
    This function return the asset id from a file.
    :param path: The asset file .
    :type path: str
    :returns:  str -- the asset code

    **Example:**
    
    >>> getIdFromFile ( doc_id = "/homeworks/projects/prod/chr/mickey/mod/a/prod_chr_mickey_mod_a.mb" )
    >>> 'prod_chr_mickey_mod_a'
    
    """

    # Check if the path exists
    if os.path.exists ( path ):
        raise RepositoryError ( "Can't get 'doc_id' from '%s', path doesn't exists." % path )

    basename = os.path.basename ( path )
    doc_id = os.path.splitext ( basename )[0]
    return doc_id

def getIdFromPath ( path = "" ):
    """
    This function return the asset id from path.

    :param path: The file path
    :type path: str
    :returns:  str -- Return the task code aka 'doc_id' from the user repository path
    :raises: RepositoryError if the path doesn't exists.

    **Example:**
    
    >>> getIdFromPath ( path = "/homeworks/user/jdoe/prod/ch/mickey/mod/a/anyfile.ext" )
    >>> 'prod_ch_mickey_mod_a'
    
    """

    # Check if the path exists
    if not os.path.exists ( path ):
        raise RepositoryError ( "Can't get 'doc_id' from '%s', path doesn't exists." % path )

    # Expand contained variables
    path = os.path.expandvars ( path )

    # Get user repository
    user_repo = os.getenv ( "HK_USER_REPO" ) + os.sep

    # Get the doc_id
    path = path.replace ( user_repo, "" )
    part = path.split ( os.sep )
    doc_id = "%s_%s_%s_%s_%s" % ( part[0], part[1], part[2], part[3], part[4] )

    return doc_id

def getPathFromId ( doc_id = "", local = False, vtype = "review" ):
    """
    This function return a path based from a provided 'doc_id'.

    :param doc_id: The asset code.
    :type doc_id: str
    :param local: If true return the user local repository path 
    :type local: bool
    :param vtype: Version type *trial/stock*
    :type vtype: str
    :returns:  str -- The asset or task path.

    **Example:**
    
    >>> #Repository
    >>> getPathFromId ( doc_id = "prod_chr_mickey_mod_a", local = False )
    >>> '/homeworks/projects/prod/chr/mickey/mod/a'
    >>>
    >>> #Local
    >>> getPathFromId ( doc_id = "prod_chr_mickey_mod_a", local = True )
    >>> '/homeworks/users/jdoe/projects/prod/chr/mickey/mod/a'    
    
    """
    if utils.checkVersionType ( vtype ) :
        return False

    # Get the last part of the path
    path = doc_id.replace ( "_", os.sep )

    # Get the first part of the path
    if local :
        # If true return the local project root
        root = os.getenv ( "HK_USER_REPO" )
    else:
        # If false return the repository project root
        root = os.getenv ( "HK_REPO" )

    # Check the root path value
    if ( not root ) or root == "" :
        raise RepositoryError ( "getPathFromId(): incorrect value for root path " )

    # Full path
    path = os.path.join ( root, path, vtype )

    return path

def getVersions ( db = None, doc_id = "", vtype = "review" ):
    """
    This function return all versions in a dictionnary of a particular asset.

    :param db: the database
    :type db: Database
    :param doc_id: The asset code.
    :type doc_id: str
    :param vtype: Version type *trial/stock*
    :type vtype: str
    :returns:  dict -- a dictionary with all versions of the asset,
                the key is a string with the version number without padding.

    **Example:**
    
    >>> db = utils.getDb()
    >>> getVersions ( db = db, doc_id = "bls_chr_belanus_mod_main" )
    >>> {'1': {'files': ['bls_chr_belanus_mod_main.mb'], 'path': '/homeworks/projects/bls/chr/belanus/mod/main/001',
        'created': '2013 Mar 08 21:16:34', 'description': 'names cleaned\nnormal softened', 'creator': 'pixo'},
        '3': {'files': ['bls_chr_belanus_mod_main.mb'], 'path': '/homeworks/projects/bls/chr/belanus/mod/main/003',
        'created': '2013 Mar 08 23:13:54', 'description': 'test export gproject etc', 'creator': 'pixo'},
        '2': {'files': ['bls_chr_belanus_mod_main.mb'] ... and so ... }
    """

    if utils.checkVersionType ( vtype ) :
        return False

    # If db is not provided get the current project DB
    if db == None :
        db = utils.getDb()

    # Get Versions from document
    versions = db [ doc_id ][ vtype ]

    return versions

def getVersionPath ( doc_id = "", version = "last", db = None, vtype = "review" ):
    """
    This function return the asset path of a particular version.

    :param db: the database
    :type db: Database
    :param doc_id: The asset code.
    :type doc_id: str
    :param version: The asset code.
    :type version: str/float/int -- 'last' or 1,2,3,4 etc
    :param vtype: Version type *trial/stock*
    :type vtype: str
    :returns:  str -- the asset directory

    **Example:**
    
    >>> db = utils.getDb()
    >>> getVersionPath ( db = db, doc_id = "bls_chr_belanus_mod_main", version = "last" )
    >>> '/homeworks/projects/bls/chr/belanus/mod/main/008'
    
    """
    # old getAssetPath

    if utils.checkVersionType ( vtype ) :
        return False

    # Get asset versions
    versions = getVersions ( db = db, doc_id = doc_id, vtype = vtype )
    num = None

    # If the queried version is the latest
    if version == "last" :
        num = int ( len ( versions ) )
    else:
        num = int ( version )

    # Get version num attr
    version = versions [ str ( num ) ]

    # Get the version path
    path = version ["path"]

    return path

def getLocalVersionPath ( doc_id = "", version = 1, vtype = "review" ):
    """
    This function return the path of a particular asset version into the user directory .

    :param doc_id: The asset code.
    :type doc_id: str
    :param version: The asset code.
    :type version: str/float/int -- 1,2,3,4 etc
    :param vtype: Version type *trial/stock*
    :type vtype: str
    :returns:  str -- the asset directory path

    **Example:**
    
    >>> getLocalVersionPath ( doc_id = "prod_chr_mickey_mod_a", version = 2 )
    >>> '/homeworks/users/jdoe/projects/prod/chr/mickey/mod/a/prod_chr_mickey_main_a.v002.base'
    
    """
    # old getAssetLocalPath

    # Make sure vtype exists
    if utils.checkVersionType ( vtype ) :
        return False

    # Make sure to get the right type for concatenation
    version = int ( version )

    # Get asset local path
    fdir = getPathFromId ( doc_id = doc_id, local = True, vtype = vtype )
    name = "%s.v%03d.base" % ( doc_id, version )
    dst = os.path.join ( fdir, name )

    # Return a path that doesn't exist
    count = 1
    while os.path.exists ( dst ) :
        dst = os.path.join ( fdir, name + str ( count ) )
        count += 1

    return dst

def getTypeFromId ( doc_id = None ):
    """
    This function return the asset path of a particular version.
    :param doc_id: The asset code.
    :type doc_id: str
    :returns:  str -- the asset type code

    **Example:**
    
    >>> getTypeFromId ( doc_id = "prod_chr_mickey_mod_a" )
    >>> 'chr'
    
    """

    if not ( doc_id ) :
        raise RepositoryError ( "getTypeFromId(): can't get type from wrong 'doc_id'" )

    return doc_id.split( "_" )[1]

def getTaskFromId ( doc_id = None ):
    """
    This function return the asset path of a particular version.
    :param doc_id: The asset code.
    :type doc_id: str
    :returns:  str -- the asset task code

    **Example:**
    
    >>> getTaskFromId ( doc_id = "prod_chr_mickey_mod_a" )
    >>> 'mod'
    
    """

    if not ( doc_id ) :
        raise RepositoryError ( "getTaskFromId(): can't get type from wrong 'doc_id'" )

    return doc_id.split( "_" )[3]

def createWorkspace ( doc_id = "", vtype = "review" ):
    """
    This function create the asset user path of a particular asset.
    :param doc_id: The asset code.
    :type doc_id: str
    :param vtype: Version type *trial/stock*
    :type vtype: str
    :returns:  str/bool -- Return the workspace path if path is created else False .

    **Example:**
    
    >>> createWorkspace ( doc_id = "prod_chr_mickey_mod_a" )
    >>> '/homeworks/users/jdoe/projects/prod/chr/mickey/mod/a'
    
    """
    # Make sure vtype exists
    if utils.checkVersionType ( vtype ) :
        return False

    # Get the local asset path to create from asset id
    path = getPathFromId ( doc_id = doc_id, local = True, vtype = vtype )

    # Check if the path exist
    if os.path.exists ( path ) :
        print ( "createWorkspace(): %s already exist" % path )
        return False

    # Create the asset path with the proper permission
    os.makedirs ( path, 0775 )

    # Check if the path was created
    if not os.path.exists ( path ) :
        raise RepositoryError ( "createWorkspace(): cannot create directory %s" % path )

    print ( "createWorkspace(): %s created" % path )
    return path

def transfer ( sources = list(), destination = "", doc_id = "", rename = True ) :

    """
    This function create the asset user path of a particular asset.
    :param doc_id: The asset code.
    :type doc_id: str
    :returns:  str/bool -- Return the workspace path if path is created else False .

    **Example:**
    
    >>> createWorkspace ( doc_id = "prod_chr_mickey_mod_a" )
    >>> '/homeworks/users/jdoe/projects/prod/chr/mickey/mod/a'
    
    """

    # Check the sources type is a list
    if type ( sources ) == str :
        sources = list ( [ sources ] )

    files = dict ()

    # Iterate over the file to transfer
    for src in sources :

        # Check if the source file exists
        if os.path.exists ( src ) :
            # TODO: Make it simpler
            # Create the destination path
            basename = os.path.basename ( src )
            filename = basename.replace ( basename.split ( "." )[0], doc_id )

            # Set filename as key value for source file
            files [src] = os.path.join ( destination, filename )

        else :
            print "Warning: %s doesn't exist" % src

    # Set the permission file
    os.chmod ( destination, 0775 )

    # Iterate over files
    for fil in files:
        dirname = os.path.dirname ( files [ fil ] )

        if not os.path.exists ( dirname ) :
            os.makedirs ( dirname )

        shutil.copy ( fil, files [ fil ] )
    os.system( "chmod -R 555  %s" % destination )

def pull ( db = None, doc_id = "", version = "last", extension = False,
           progressbar = False, msgbar = False, vtype = "review" ):

    """
    This function copy the desired file from repository to local workspace.

    :param db: the database
    :type db: Database
    :param doc_id: The asset code
    :type doc_id: str
    :param version: The asset version
    :type version: int/str
    :param extension: The file extension
    :type extension: int/str
    :param progressbar: The pyside progress bar
    :type progressbar: PySide progressbar
    :param msg: The pyside message bar
    :type progressbar: PySide messagebar
    :param vtype: Version type *trial/stock*
    :type vtype: str
    :returns: list -- a list of the pulled file.

    **Example:**
    
    >>> db = utils.getDb()
    >>> pull ( db = db, doc_id = "bls_chr_belanus_mod_main", version = 2 )
    >>> ['/homeworks/users/jdoe/projects/bls/chr/belanus/mod/main/bls_chr_belanus_mod_main.v002.base/bls_chr_belanus_mod_main.jpg',
    >>> '/homeworks/users/jdoe/projects/bls/chr/belanus/mod/main/bls_chr_belanus_mod_main.v002.base/bls_chr_belanus_mod_main.mb']

    """
    # Make sure vtype exists
    if utils.checkVersionType ( vtype ) :
        return False

    def echoMsg ( msg = "", msgbar = None ):
        print msg
        if msgbar :
            msgbar ( msg )

    # If db is not provided get the current project DB
    if db == None :
        db = utils.getDb()

    # Check id is respecting the homeworks naming convention
    docsplit = doc_id.split( "_" )
    if len ( docsplit ) < 5:
        echoMsg ( msg = "pull(): Wrong asset id", msgbar = msgbar )
        return False

    # Get asset repository and local asset path
    src = getVersionPath ( doc_id = doc_id, version = version, db = db, vtype = vtype )
    dst = getLocalVersionPath ( doc_id = doc_id, version = version, vtype = vtype )

    # Add/Check files to pull
    lsdir = list ()
    for root, subFolders, files in os.walk ( src ):

        for fil in files:
            curfile = os.path.join ( root, fil )

            if extension and extension != "" :
                if os.path.splitext ( curfile )[-1] == extension :
                    lsdir.append ( curfile )
            else :
                lsdir.append ( curfile )

    # Prepare the progress bar
    if progressbar :
        progress_value = 0
        progress_step = 100.0 / len( lsdir ) if len( lsdir ) != 0 else 1

    # Check there is something to pull
    if len ( lsdir ) > 0 :
        os.makedirs ( dst, 0775 )
        if not os.path.exists ( dst ):
            raise RepositoryError ( "Pull(): cannot create %s " % dst )

    # Pull lsdir file
    pulled = list()
    for fil in lsdir:
        fulldst = fil.replace ( src, dst )
#         dirname = os.path.dirname ( fulldst )

        shutil.copyfile ( fil, fulldst )
        pulled.append ( fulldst )

        # Echo message
        msg = "Pulled: %s" % fulldst
        echoMsg ( msg = msg, msgbar = msgbar )

        if progressbar :
            progress_value += progress_step
            progressbar.setProperty ( "value", progress_value )

    return pulled


def push ( db = "", doc_id = "", path = list(), description = "",
          progressbar = False, msgbar = False, rename = True, vtype = "review" ):
    """
    This function copy the desired file from local workspace to repository.

    :param db: the database
    :type db: Database
    :param doc_id: The asset code
    :type doc_id: str
    :param path: The list of files to push
    :type path: str/list of str
    :param description: This is the description of the push
    :type description: str
    :param progressbar: The pyside progress bar
    :type progressbar: PySide progressbar
    :param msg: The pyside message bar
    :type progressbar: PySide messagebar
    :param rename: Rename the file (default True)
    :type rename: bool -- if True rename the file(s)
    :param vtype: Version type *trial/stock*
    :type vtype: str
    :returns: str -- Return the published directory

    **Example:**
    
    >>> db = utils.getDb()
    >>> push ( db = db, doc_id = "bls_chr_belanus_mod_main",
    >>>        path = "/homeworks/users/jdoe/projects/bls/chr/belanus/mod/main/file_to_push.mb",
    >>>        description = "this is a modeling version of belanus" )

    """

    # Make sure vtype exists
    if utils.checkVersionType ( vtype ) :
        return False

    # TODO: Check push for auto screenshot publish
    # Check the path type is a list
    if type ( path ) == str :
        path = list ( [ path ] )

    # check if the source file exists in the repository
    file_list = list ()

    for src in path :
        if os.path.exists ( src ) :
            file_list.append ( src )

        else:
            print "Warning: %s doesn't exist" % src

    # Get root destination directory to push files
    dst_dir = getPathFromId ( doc_id, vtype = vtype )

    # Get temporary destination directory to push files
    tmp_dir = os.path.join ( dst_dir, utils.hashTime () )

    # Create temporary directory
    if not os.path.exists ( tmp_dir ):
        os.makedirs ( tmp_dir )

    # Copy all the files in the destination directory
    progress_value = 0
    progress_step = 100.0 / len ( file_list )
    files_attr = list ()
    wspace = getPathFromId ( doc_id = doc_id, local = True, vtype = vtype )

    # Iterate over all the provided source files
    for src in file_list :
        # Get file dir
        src_dir = os.path.dirname ( src )
        # file space in case we need to publish directories
        file_space = src_dir.replace ( wspace, "" )
        file_name = os.path.join ( file_space, os.path.basename ( src ) )

        # Get extension(s) ,UDIMs and frames are commonly separated with this char
        file_ext = "." + file_name.split ( "." )[-1]

        # Get screenshot file
        screenshot = False
        screenshot_exts = [ ".jpg", ".jpeg", ".png" ]
        screenshot_ext = ""

        for ext in screenshot_exts :
            screenpath = file_name + ext
            screenpath = os.path.join ( src_dir, screenpath )

            if os.path.exists ( screenpath ) :
                screenshot_ext = ext
                screenshot = screenpath
                break
            else :
                screenpath = screenpath.replace ( "." + file_ext, ext )
                if screenpath != file_name :
                    if os.path.exists ( screenpath ) :
                        screenshot_ext = ext
                        screenshot = screenpath

        # Creating the full filename
        if rename:
            dst_file = doc_id + file_ext
            dst_screenshot = doc_id + screenshot_ext

        else:
            dst_file = file_name
            dst_screenshot = screenshot

        if dst_file [0] == os.sep :
            dst_file = dst_file [1:]

        tmp_file = os.path.join ( tmp_dir, dst_file )

        # Store the files names in a list to avoid to call the database for each source file
        files_attr.append ( dst_file )

        # Copy files to temporary directory
        shutil.copy ( src, tmp_file )

        # Copy screenshot to temporary directory
        if screenshot :
            if dst_screenshot [0] == os.sep :
                dst_screenshot = dst_screenshot [1:]
            tmp_screenshot = os.path.join ( tmp_dir, dst_screenshot )
            shutil.copy ( screenshot, tmp_screenshot )

        # Set progress value
        progress_value += progress_step
        if progressbar :
            progressbar.setProperty ( "value", progress_value )
        else :
            print ( str ( progress_value ) + "%" )

        if msgbar :
            msgbar ( dst_file )

    # Get latest version
    doc = db [ doc_id ]
    ver_attr = getVersions ( db, doc_id, vtype = vtype )
    ver = len ( ver_attr ) + 1
    path_attr = os.path.join ( dst_dir, "%03d" % ver )
    repo = os.path.expandvars ( path_attr )

    # Rename the temp dir
    os.rename ( tmp_dir, repo )

    # TODO:Replace os.system ( "chmod -R 555  %s" % repo ) by python function
    os.system ( "chmod -R 555  %s" % repo )

    # Create the new version data for the "versions" document's attribute
    fileinfo = {
                "creator" : os.getenv ( "USER" ),
                "created" : time.time(),
                "description" : description ,
                "path" : path_attr ,
                "files" : files_attr
                }

    # Append the data into the document version attribute copy
    ver_attr [ ver ] = fileinfo

    # Replace the original "versions" attribute by our modified version
    doc [ vtype ] = ver_attr

    # Push the info into the db
    db [ doc_id ] = doc

    # print published file for the user
    for fil in files_attr:
        print os.path.join ( repo , fil )

    # Return the published directory
    return repo

def pushDir ( db = "", doc_id = "", path = list(), description = "", vtype = "review" ):
    """
    This function copy the desired file from local workspace to repository.

    :param db: the database
    :type db: Database
    :param doc_id: The asset code
    :type doc_id: str
    :param path: directory or The list of directories to push
    :type path: str/list of str
    :param description: This is the description of the push
    :type description: str
    :param vtype: Version type *trial/stock*
    :type vtype: str
    :returns: str -- Return the published directory

    **Example:**
    
    >>> db = utils.getDb()
    >>> pushDir ( db = db, doc_id = "bls_chr_belanus_mod_main",
    >>>            path = "/homeworks/users/jdoe/projects/bls/chr/belanus/tex/main/directory_to_push",
    >>>            description = "This is a publish" )

    """
    # Make sure vtype exists
    if utils.checkVersionType ( vtype ) :
        return False

    # check if the source file exists in the repository
    if not os.path.exists ( path ) :
        print "pushDir(): %s doesn't exist" % path
        return False

    # Get root destination directory to push files
    dst_dir = getPathFromId ( doc_id = doc_id, vtype = vtype )

    # Get temporary destination directory to push files
    tmp_dir = os.path.join ( dst_dir, utils.hashTime () )
    os.makedirs ( tmp_dir )

    # Copy all the files in the destination directory
    files_attr = list ()
    file_list = os.listdir ( path )

    for src in file_list :
        # file space in case we need to publish directories """
        path_src = os.path.join ( path, src )
        dst = os.path.join ( tmp_dir, src )

        if os.path.isfile ( path_src ):
            print  "pushDir(): copying file %s " % src
            shutil.copy ( path_src, dst )
        elif os.path.isdir ( path_src ):
            print  "pushDir(): copying directory %s " % src
            shutil.copytree ( path_src, dst )

        # Store the files names in a list to avoid to call the database for each source file
        files_attr.append ( src )

    # Get latest version number because somebody may push a new version during the process
    doc = db [ doc_id ]
    ver_attr = getVersions ( db = db, doc_id = doc_id, vtype = vtype )
    ver = len ( ver_attr ) + 1
    path_attr = os.path.join ( dst_dir, "%03d" % ver )
    repo = os.path.expandvars ( path_attr )

    # Rename the temp dir
    os.rename ( tmp_dir, repo )
    os.chmod ( repo, 0555 )

    # Create the new version data for the "versions" document's attribute
    fileinfo = {
                "creator" : os.getenv ( "USER" ),
                "created" : time.time(),
                "description" : description ,
                "path" : path_attr ,
                "files" : files_attr
                }

    # Append the data into the document version attribute copy
    ver_attr [ ver ] = fileinfo

    # Replace the original "versions" attribute by our modified version
    doc [ vtype ] = ver_attr

    # Push the info into the db
    db [ doc_id ] = doc

    # print published file for the user
    for fil in files_attr:
        print os.path.join ( repo , fil )

    # Return the published directory
    return repo

def pushFile ( db = None, doc_id = False, path = list (), description = "", rename = True, vtype = "review" ):
    """
    This function copy the desired file from local workspace to repository.

    :param db: the database
    :type db: Database
    :param doc_id: The asset code
    :type doc_id: str
    :param path: The list of files to push
    :type path: str/list of str
    :param description: This is the description of the push
    :type description: str
    :param rename: Rename the file (default True)
    :type rename: bool -- if True rename the file(s)
    :param vtype: Version type *trial/stock*
    :type vtype: str
    :returns: str -- Return the directory of the pushed files

    **Example:**
    
    >>> db = utils.getDb()
    >>> push ( db = db, doc_id = "bls_chr_belanus_mod_main",
    >>>        path = "/homeworks/users/jdoe/projects/bls/chr/belanus/mod/main/file_to_push.mb" )

    """
    # Make sure vtype exists
    if utils.checkVersionType ( vtype ) :
        return False

    # Check if DB is provided else get the project DB
    if ( not db )  or db == "" :
        db = utils.getDb()

    # Check if 'path' is a string
    if type ( path ) == str:

        # If 'path' is a string then append it in a list
        path = list ( [ path ] )

    # If doc_id not provided
    if not doc_id:

        # Get doc_id from path
        doc_id = getIdFromPath ( path = path[0] )

    # Return the directory of the pushed files
    result = push ( db = db , doc_id = doc_id , path = path ,
                  description = description, progressbar = False,
                  msgbar = False, rename = rename, vtype = vtype )
    return result


def getTextureAttr ( path = None ):
    """
    This function return a list containing the type of the texture
    and a list of attributes that should match the textures attribute.
    This is used to check if the texture have the right naming convention and the right attributes.

    :param path: The list of files to push
    :type path: str
    :returns: str -- Return the directory of the pushed files

    **Example:**
    >>> getTextureAttr ( path = "/homeworks/users/jdoe/projects/bls/chr/belanus/tex/main/bls_chr_belanus_tex_main_spec1.1001.tif" )
    >>> ('spec1', ('R', '8-bit 16-bit', 'rgb(255,255,255)', True, 'triangle', '1'))
    
    """

    # Get authorized texture types list
    textureType = utils.getTextureTypes ()

    # Get the texture filename
    fname = os.path.basename ( path )

    # Iterate over all the texture types
    for typ in textureType :

        # Define common texture patern
        simpTex = "%s\d*.\d\d\d\d." % typ

        # Define animated texture patern
        animTex = "%s\d*.\d\d\d\d.\d\d\d\d." % typ

        # Combine patterns
        pattern = "%s|%s" % ( simpTex, animTex )

        # Check the filename belong to one of the texture type
        if re.findall ( pattern, fname ) == []:
            return ( typ, textureType [ typ ] )

    return ( False, False )

def textureBuild ( path = "", mode = "ww", texfilter = None ):
    """
    This function build the textures.

    :param path: the path to the texture
    :type path: str
    :param mode: The texture wrap mode
    :type mode: str
    :param texfilter: The texture filter mode
    :type texfilter: str
    :returns: bool -- True if texture builded

    **Example:**
    >>> textureBuild ( path = "/homeworks/users/jdoe/projects/bls/chr/belanus/tex/main/bls_chr_belanus_tex_main_spec1.1001.tif" )

    **Note:**
        This function use a system command that calls the 'render' binary from guerilla.
        You can add your custom builder here.
        Make sure to have it in your PATH.
    """

    # TODO: Add Gamma support

    # Check the texture filter
    if ( texfilter == None ) and ( mode != "latlong" ) :
        # Get default texture filter for this texture
        texattr = getTextureAttr ( path )[1]

        if not texattr :
            # It means the texture is not conform to the naming convention
            return False

        texfilter = texattr[4]
        # texgamma = texattr[5]

    # If use for ibl set texture filter to triangle
    if mode == "latlong" :
            texfilter = "triangle"

    # Guerilla builder function
    def guerillaBuild ( path, mode, texfilter ):
        ''
        fil = os.path.splitext ( path )[0]
        tex = fil + ".tex"
        cmd = """render --buildtex --in %s --mode %s --filter %s --out %s""" % ( path, mode, texfilter, tex )
        os.system ( cmd )
        print "buildtex: building %s" % tex

    # Build guerilla texture file
    guerillaBuild ( path, mode, texfilter )

    # Here you can add your custom builder function

    return True

def textureOptimise ( path = None ):
    """
    This function optimise the provided texture.

    :param path: the path to the texture
    :type path: str

    **Example:**
    >>> textureOptimise ( path = "/homeworks/users/jdoe/projects/bls/chr/belanus/tex/main/bls_chr_belanus_tex_main_spec1.1001.tif" )

    **Note:**
        This function use system commands that calls 'imagemagick'.
        Make sure to have it installed.
        
    """
    # Get the filename
    fname = os.path.basename ( path )

    # Get the texture attributes
    texattr = getTextureAttr ( path )[1]

    if texattr :
        # Default texture attributes
        texchannel = texattr[0]
        texdepth = texattr[1]
        texbgcolor = texattr[2]
        texcompress = texattr[3]
        # texfilter = texattr[4]

        # Create imagemagick identify cmd to get the current image attributes
        cmd_identify = "identify %s" % path

        # Get the current image attributes
        imgattr = commands.getoutput ( cmd_identify ).split( "\n" )[-1]
        imgattr = imgattr.split ( " " )
        imgdepth = imgattr[4]
        imgformat = imgattr[1]
        # imgres = imgattr[2]

        if texcompress :
            # Zip aka Deflate compression with imagemagick mogrify
            cmd_compress = "mogrify -compress Zip %s" % path
            os.system ( cmd_compress )
            print "compress 'Deflate': %s" % fname

        elif texbgcolor != "" :
            # Remove image alpha with imagemagick mogrify
            cmd_alpharm = """mogrify -background "%s" -flatten +matte %s""" % ( path, texbgcolor )
            os.system ( cmd_alpharm )
            print "remove alpha: %s" % fname

        if texchannel == "R" :
            # Set to single channel with imagemagick mogrify
            cmd_channel = "mogrify -channel R -separate %s" % path
            os.system ( cmd_channel )
            print "grayscale: %s" % fname

        if texdepth.find ( imgdepth ) < 0 :
            # Check the image depth
            print "warning: wrong depth '%s', %s should be '%s'  " % ( imgdepth, fname, texdepth )

        # TODO:check if tiff format warning is working
        if imgformat != "TIFF":
            # Check image format
            print "warning: wrong format '%s', %s should be '%s'  " % ( imgformat, fname, "TIFF" )

    else:
        print "Can't find the '%s' texture type" % fname

def textureExport ( path = "", progressbar = False ):
    """
    This function optimise and build the 'tif' textures contained in the provided path.

    :param path: the path to the texture
    :type path: str
    :param progressbar: PySide progressbar
    :type progressbar: PySide progressbar
    :returns: bool -- True if created

    **Example:**
    >>> textureOptimise ( path = "/homeworks/users/jdoe/projects/bls/chr/belanus/tex/main/bls_chr_belanus_tex_main_spec1.1001.tif" )

    **Note:**
        This function use system commands that calls 'imagemagick'.
        Make sure to have it installed.
        
    """

    # Get all the tif files in the directory 'path'
    files = glob.glob ( os.path.join ( path, "*.tif" ) )

    # TODO: support progressbar for textures optimisation
    for fil in files :
        # Optimise the current texture 'fil'
        textureOptimise ( fil )

        # Build the current texture 'fil'
        textureBuild ( fil )

    return True

def textureCheck ( doc_id = "", files = list() ) :
    """
    This function check if textures respect the Homeworks rules.

    :param doc_id: The asset code
    :type doc_id: str
    :param files: File(s) to check
    :type files: str/list of str
    :returns: list -- Return a list of textures path that have not success the check

    **Example:**
    >>> textureOptimise ( path = "/homeworks/users/jdoe/projects/bls/chr/belanus/tex/main/bls_chr_belanus_tex_main_spec1.1001.tif" )

    **Note:**
        This function use system commands that calls 'imagemagick'.
        Make sure to have it installed.
        
    """

    # Get authorised textures types
    textureType = utils.getTextureTypes ()

    # Make sure files is a list
    not_success = list ( files )

    # Iterate over provided files
    for fil in files :

        # Get filename
        fname = os.path.basename ( fil )

        # Check the texture 'fil' is legal
        for typ in textureType :

            # Common texture pattern
            simpTex = "%s_\d*_%s\d*.\d\d\d\d." % ( doc_id, typ )
            simpTex = simpTex + "tif|" + simpTex + "exr"

            # Animated texture pattern
            animTex = "%s_\d*_%s\d*.\d\d\d\d.\d\d\d\d." % ( doc_id, typ )
            animTex = animTex + "tif|" + animTex + "exr"

            # Combine patterns
            pattern = "%s|%s" % ( simpTex, animTex )

            # If 'fil' texture respect one of the patterns
            if re.findall ( pattern, fname ):

                texfile = ""
                # Get the extension
                fext = fname.split ( "." )[-1]

                # Check if the texture is already built
                if fext != "tex":

                    # Replace the current extension by .tex
                    texfile = fil.replace ( ".%s" % fext, ".tex" )

                    # Check if texfile exist
                    if os.path.exists ( texfile ):

                        # Remove the textures from not_success
                        not_success.remove ( fil )
                        not_success.remove ( texfile )
                        print "textureCheck: %s OK" % fname

                    else:
                        print "textureCheck: missing .tex for %s" % fname

    return not_success

def texturePush ( db = None, doc_id = "", path = "", description = "",
                  progressbar = False, msgbar = False, rename = False, vtype = "review" ) :

    """
    This function copy the desired file from local workspace to repository.

    :param db: the database
    :type db: Database
    :param doc_id: The asset code
    :type doc_id: str
    :param path: The path that contains the textures
    :type path: str
    :param description: This is the description of the push
    :type description: str
    :param progressbar: The pyside progress bar
    :type progressbar: PySide progressbar
    :param msg: The pyside message bar
    :type msg: PySide messagebar
    :param rename: Rename the file (default True)
    :type rename: bool -- if True rename the file(s)
    :param vtype: Version type *trial/stock*
    :type vtype: str
    :returns: bool/list -- Return False if fail to push the textures else the list of success textures

    **Example:**
    
    >>> db = utils.getDb()
    >>> texturePush ( db = db, doc_id = "bls_chr_belanus_mod_main",
    >>>        path = "/homeworks/users/jdoe/projects/bls/chr/belanus/mod/main/file_to_push.mb",
    >>>        description = "this is a texture version of belanus" )

    """
    # Make sure vtype exists
    if utils.checkVersionType ( vtype ) :
        return False

    # List the directory
    # TODO: Use glob to get the right textures
    if not os.path.isdir ( path ):
        return False

    lsdir = os.listdir ( path )

    files = list ()
    # Iterate over files contained in the directory 'path'
    # and check if the file is a mra or psd
    for fil in lsdir:

        # Get file extension
        ext = os.path.splitext ( fil ) [-1]

        if ext in ( ".mra", ".psd" ):
            # If current file is a Mari or photoshop file
            # aka extraordinary textures files
            if not ( fil.find ( doc_id ) == 0 ) :
                print fil, "should begin with %s" % doc_id
                return False
        else:
            # else add the file for texture check
            files.append ( os.path.join ( path, fil ) )

    # Check the none extraordinary textures files
    texCheck = textureCheck ( doc_id, files )

    # If every textures success the check
    if len ( texCheck ) == 0 :
        # Push the directory containing the textures
        pushed = pushDir ( db = db, doc_id = doc_id, path = path, description = description, vtype = vtype )
        return pushed
    else :
        for tex in texCheck :
            print ( "texturePush(): %s is wrong" % tex )

        simptex = "%s_%s_%s.%s.%s" % ( doc_id, "<variation>", "<type>", "<udim>", "tif" )
        animtex = "%s_%s_%s.%s.%s.%s" % ( doc_id, "<variation>", "<type>", "<udim>", "<frame>", "tif" )
        print "texturePush(): expect %s or %s " % ( simptex , animtex )

        return False
