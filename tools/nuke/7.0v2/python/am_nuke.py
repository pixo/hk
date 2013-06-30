print "hk-nuke: importing reader"
import nuke, os, glob, re
import pipeline.apps as apps
import pipeline.utils as utils

ASSET_MANAGER = apps.UiAssetManager ()

def getAssetTypes():
    params = utils.getAssetTypes ()
    result = dict()
    for param in params :
        result[ params [param] ] = param
    return result

def getAssetTasks():
    params = utils.getAssetTasks ()
    result = dict()
    for param in params :
        result[ params [param] ] = param
    return result

def createOutDirs ():
    trgDir = os.path.dirname( nuke.filename( nuke.thisNode() ) )    
    if not os.path.isdir( trgDir ):
        os.makedirs( trgDir )

def hkGetRepo ( space = "network" ) :
    repository = { "network":"HK_REPO", "local":"HK_USER_REPO" }
    root = os.getenv ( repository [ space ] )
    return root

def hkGetProject () :
    return os.getenv ( "HK_PROJECT" )

def hkGetParams ( nodeclass ):
    if nodeclass == "Write" :
        return ( "type", "asset", "task", "fork", "versions" )

    elif nodeclass in ( "Read") :
        return ( "type", "asset", "task", "fork", "versions", "layer", "aov" )

    elif nodeclass in ( "ReadGeo2", "Camera2" ) :
        return ( "type", "asset", "task", "fork", "versions" )

def hkSetNodes () :

    node = nuke.thisNode()
    #Get path from node
    filepath = hkGetPath ( node )

    if node.Class () == "Read":
        path, rang = getFileSeq ( filepath ).split()
        first,last = rang.split ( '-' )
        node['file'].setValue( path )
        node['first'].setValue( int ( first ) )
        node['last'].setValue( int ( last ) )
    
    elif node.Class () == "Write":
        node['file'].setValue ( filepath )
        node['first'].setValue( 1 )
        node['last'].setValue( 1 )

    elif node.Class () == "ReadGeo2":
        path, rang = getFileSeq ( filepath ).split()
        first,last = rang.split ( '-' )
        node['geofile'].setValue( path )

    elif node.Class () == "Camera2":
        path, rang = getFileSeq ( filepath ).split()
        first,last = rang.split ( '-' )
        node['file'].setValue( path )

def hkAssetChanged ():
    n = nuke.thisNode()
    k = nuke.thisKnob()
    name = k.name()

    params = hkGetParams ( n.Class () )

    values = list ()
    if name in params :

        for i in range ( params.index ( name ), len ( params ) ) :
            param = params[i]
            values = hkAssetUpdate ( param = param )

        hkSetNodes ()

    elif name in ( "repository", "extension", ) :
        hkAssetUpdateAll ( node = n )

def hkAssetUpdate ( node = None, param = "" ) :
    #Get param filter
    paramfilter = { "type":getAssetTypes () , "task":getAssetTasks () }

    #Check the arg are provided
    if node == None :
        node = nuke.thisNode ()

    #Get params in function of the class node
    params = hkGetParams ( node.Class () )
    
    #Get the knob parameter
    knob = node.knob ( param )

    if ( type ( knob ) != type ( None ) ) :
        #Get repository local or network
        krepo = node.knob  ( "repository" )
        space = krepo.enumName ( int ( krepo.getValue () ) )
        root = hkGetRepo ( space )

        #Get project name
        project = hkGetProject ()

        #Get project repository path
        path = os.path.join ( root, project )
        if ( knob.Class() == "Enumeration_Knob" ) :
            it = 0
            kcurval = None
            next = True
            #Get the path till the current parameters
            while it < params.index ( param ) and next  :
                #Get current knob
                kcur = node.knob ( params [ it ] )

                #Get current knob value
                kcurval = kcur.enumName ( int ( kcur.getValue () ) )
                
                #Increment iterator                    
                it += 1

                #reconstruct the path
                if kcurval != None :
                    path = os.path.join ( path, kcurval )
                else:
                    next = False

            # Collect all directories in reconstructed path
            values = list ()
            if os.path.exists ( path ) and os.path.isdir ( path ) and next:

                # List 'path'
                files = os.listdir ( path )

                # Iterate over 'files'
                for file in files :

                    # Get directories in file
                    if os.path.isdir ( os.path.join ( path, file ) ):
                        
                        # Check if current  knob is type or task
                        if ( param in paramfilter ):

                            # Add directories if they have the good value eg type: chr,prp,etc or task: lit,tex, etc
                            if ( file in paramfilter [ param ]) :
                                values.append ( file )
                        else:
                            #Adding others folders
                            values.append ( file )

            #Set the current knob values
            knob.setValues (values)

            #Check that the current knob values is not set to None if it contains data 
            if (len ( values ) > 0) and knob.enumName ( int ( knob.getValue () ) ) == None :
                knob.setValue ( values[0] )


def hkAssetUpdateAll ( node = None, params = "" ) :
    if params == "" :
        params = hkGetParams ( node.Class () )
    
    for param in params :
        hkAssetUpdate ( node = node, param = param )

    hkSetNodes ()

def getFileSeq ( path ):
    '''Return file sequence with same name as the parent directory. Very loose example!!'''
    dirPath = path
    if not os.path.isdir ( path ):
        dirPath = os.path.dirname( path )

    # COLLECT ALL FILES IN THE DIRECTORY THAT HVE THE SAME NAME AS THE DIRECTORY
#     files = glob.glob( os.path.join( dirPath, '%s.*.*' % doc_id ) )
    files = glob.glob ( os.path.join( dirPath, '*' ) )
    files.sort ()

    # GRAB THE RIGHT MOST DIGIT IN THE FIRST FRAME'S FILE NAME
    # print "files", files
    if not len (files) > 0:
        return path + " 1-1"

    file = files[0] 
    firstString = re.findall ( r'\d+', os.path.basename ( file ) )

    if not len ( firstString ) > 0 :
        return file + " 1-1" 
    
    firstString = firstString[-1]

    # GET THE PADDING FROM THE AMOUNT OF DIGITS
    padding = len ( firstString )

    # CREATE PADDING STRING FRO SEQUENCE NOTATION
    paddingString = '%02s' % padding

    # CONVERT TO INTEGER
    first = int ( firstString )

    # GET LAST FRAME
    last = re.findall( r'\d+', os.path.basename ( files[-1] ) )[-1]
    last = int ( last.replace ( ".", "" ) )

    # GET EXTENSION
    ext = os.path.splitext ( file )[-1]
    file =  files[0].replace ( ext, "" )
    if ext == ".tex":
        ext = ".tif"

    # BUILD SEQUENCE NOTATION
    filsplit = file.split (".")

    if len ( filsplit ) > 2:
        base = file.replace( filsplit[-1],"")
        fileName = '%s%%%sd%s %s-%s' % ( base, str(padding).zfill(2), ext, first, last )
    
    elif len ( filsplit ) == 2:
        base = file.replace( filsplit[1],"")
        fileName = '%s%%%sd%s %s-%s' % ( base, str(padding).zfill(2), ext, first, last )
    else :
        base = file
        fileName = '%s%s %s-%s' % ( base, ext, first, last )

    # RETURN FULL PATH AS SEQUENCE NOTATION
    return os.path.join ( dirPath, fileName )

def hkGetPath ( node = None ) :

    project = hkGetProject ()
    project = project.lower()
    project = project.replace( " ", "" )

    krepo = node.knob ( 'repository' )
    if krepo != None :

        # Get repository local or network
        repo = str ( krepo.value () )
        root = hkGetRepo ( repo )
        path = os.path.join ( root, project)

        # Iterate over the parameters to get filename
        fname = project
        params = hkGetParams ( node.Class () )

        for param in params:
            k = node.knob ( param )
            
            if k != None :
                value = str ( k.value () )

                if value != None and value != "0" :
                    value = value.lower().replace ( " ", "" )
                    
                    # Get the file name
                    if param != "versions":
                        fname += "_%s" % value
                    
                    # Get file path
                    path = os.path.join ( path, value )

        ext = ""
        kextension = node.knob ( 'extension' )
        if kextension != None :
            ext = "." + kextension.enumName ( int ( kextension.getValue() ) )

        fname += ".%s%s" % ( "%04d", ext  )
        path = os.path.join ( path, fname )

        return path
    
def hkReadImagesCreate () :
    #Setup file python expression
    params = hkGetParams ( "Read" )

    # Create main node    
    node_asset = nuke.createNode ( "Read" )
    node_asset [ "name" ].setValue ( "ReadImagesAsset" )
    assetTab = nuke.Tab_Knob ( "Asset" )

    #Create and setup knobs
    node_asset.addKnob ( assetTab )
    repository = ( "network", "local" )
    krepo = nuke.Enumeration_Knob ( "repository", "repository", repository ) 
    repoup = "hkAssetUpdateAll ( nuke.thisNode () )"
    krepoup = nuke.PyScript_Knob ( "repositoryup", "Update", repoup )
    node_asset.addKnob ( krepo )
    node_asset.addKnob ( krepoup )
    
    for param in params :
        knob = nuke.Enumeration_Knob ( param, param, list () )
        node_asset.addKnob ( knob )
    
    # kextension = nuke.Enumeration_Knob ( "extension", "extension", list(("exr","tif","png","jpg")) )
    # node_asset.addKnob ( kextension )

    kpostage_stamp = node_asset [ "postage_stamp" ]
    kpostage_stamp.setValue ( True )

    #Update everything
    hkAssetUpdateAll ( node = node_asset )

def hkWriteImagesCreate ():

    #Create the main node
    node_asset = nuke.createNode ( "Write" )
    node_asset [ "name" ].setValue ( "WriteAsset" )
    node_asset["beforeRender"].setValue ( "createOutDirs()" )
    
    #Create tabs
    assetTab = nuke.Tab_Knob ( "Asset" )
    
    #Setup file python expression
    params = ( "type", "asset", "task", "fork" )
    
    #Create and setup knobs
    node_asset.addKnob ( assetTab )
    repository = ["local"]
    krepo = nuke.Enumeration_Knob ( "repository", "repository", repository ) 
    repoup = "hkAssetUpdateAll ( params = ( 'type', 'asset', 'task', 'fork' ) )"
    krepoup = nuke.PyScript_Knob ( "repositoryup", "Update", repoup )
    node_asset.addKnob ( krepo)
    node_asset.addKnob ( krepoup)
    
    for param in params :
        knob = nuke.Enumeration_Knob ( param, param, list () )
        node_asset.addKnob ( knob )
           
    kversion = nuke.String_Knob ("versions","versions","wedge")
    kextension = nuke.Enumeration_Knob ( "extension", "extension", list ( ("exr", "tif", "png", "jpg") ) )

    for k in (kversion, kextension):
        node_asset.addKnob ( k )

    #Update everything
    hkAssetUpdateAll ( node = node_asset ) #, params = params )


def hkReadGeometryCreate () :
    #Setup file python expression
    params = hkGetParams ( "ReadGeo2" )

    # Create main node    
    node_asset = nuke.createNode ( "ReadGeo2" )
    node_asset [ "name" ].setValue ( "ReadGeoAsset" )
    assetTab = nuke.Tab_Knob ( "Asset" )

    #Create and setup knobs
    node_asset.addKnob ( assetTab )
    repository = ( "network", "local" )
    krepo = nuke.Enumeration_Knob ( "repository", "repository", repository ) 
    repoup = "hkAssetUpdateAll ( nuke.thisNode () )"
    krepoup = nuke.PyScript_Knob ( "repositoryup", "Update", repoup )
    node_asset.addKnob ( krepo )
    node_asset.addKnob ( krepoup )
    
    for param in params :
        knob = nuke.Enumeration_Knob ( param, param, list () )
        node_asset.addKnob ( knob )
    
    # kextension = nuke.Enumeration_Knob ( "extension", "extension", list(("exr","tif","png","jpg")) )
    # node_asset.addKnob ( kextension )

    kpostage_stamp = node_asset [ "postage_stamp" ]
    kpostage_stamp.setValue ( True )

    kgeofile = nuke.File_Knob ("geofile","geofile")
    node_asset.addKnob ( kgeofile )

    loadgeo = "hkLoadAbc()"
    kloadgeo = nuke.PyScript_Knob ( "kgeoload", "Loadgeo", loadgeo )
    node_asset.addKnob ( kloadgeo )

    #Update everything
    hkAssetUpdateAll ( node = node_asset )

def hkReadCameraCreate () :
    #Setup file python expression
    params = hkGetParams ( "Camera2" )

    # Create main node    
    node_asset = nuke.createNode ( "Camera2" )
    node_asset [ 'name' ].setValue ( "ReadCameraAsset" )
    node_asset [ 'read_from_file' ].setValue ( True )
    assetTab = nuke.Tab_Knob ( "Asset" )

    #Create and setup knobs
    node_asset.addKnob ( assetTab )
    repository = ( "network", "local" )
    krepo = nuke.Enumeration_Knob ( "repository", "repository", repository ) 
    repoup = "hkAssetUpdateAll ( nuke.thisNode () )"
    krepoup = nuke.PyScript_Knob ( "repositoryup", "Update", repoup )
    node_asset.addKnob ( krepo )
    node_asset.addKnob ( krepoup )
    
    for param in params :
        knob = nuke.Enumeration_Knob ( param, param, list () )
        node_asset.addKnob ( knob )

    #Update everything
    hkAssetUpdateAll ( node = node_asset )

#####################CALL BACK
#Add callback
for nclass in ( "Read","Write", "ReadGeo2", "Camera2" ):
    nuke.addKnobChanged ( hkAssetChanged , nodeClass= nclass )
    
def hkLoadAbc ():
    node = nuke.thisNode()
    node['file'].setValue(node['geofile'].getValue()) 
    # nuke.createScenefileBrowser( node['geofile'].value(), "ReadAsset" )