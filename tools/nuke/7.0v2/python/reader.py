print "hk-nuke: importing reader"
import nuke,os
import pipeline.utils as utils

def getAssetTypes():
    params = utils.getAssetTypes ()
    result = dict()
    for param in params :
        result[ params [param] ] = param
    return result

def getTaskTypes():
    params = utils.getTaskTypes ()
    result = dict()
    for param in params :
        result[ params [param] ] = param
    return result

HK_ASSET_TYPE = getAssetTypes ()
HK_TASK_TYPE = getTaskTypes ()

def hkGetRepo ( space = "network" ) :
    repository = { "network":"HK_REPO", "local":"HK_USER_REPO" }
    root = os.getenv ( repository [ space ] )
    return root

def hkGetProject () :
    return os.getenv ( "HK_PROJECT" )

def hkGetParams ():
    return ( "type", "asset", "task", "fork", "version", "layer", "aov" )

def hkReadChanged () :
    n = nuke.thisNode()
    k = nuke.thisKnob()
    name = k.name()
    params = hkGetParams ()

    if name in params :
        for i in range ( params.index ( name ), 7 ) :
            param = params[i]
            hkReadUpdate ( param = param )
        
    elif name in ( "repository", "extension" ) :
        hkReadUpdateAll ()

nuke.addKnobChanged ( hkReadChanged )#, nodeClass="ColorCorrect")

def hkReadUpdate ( node = None, param = "") :
    params = hkGetParams ()
    paramfilter = { "type":HK_ASSET_TYPE , "task":HK_TASK_TYPE }

    if node == None :
        n = nuke.thisNode ()
    else:
        n = node

    k = n.knob ( param )

    if ( type ( k ) != type ( None ) ) and ( k.Class() == "Enumeration_Knob" ) :
        krepo = n.knob  ( "repository" )
        kpath = n.knob  ( "path" )

        space = krepo.enumName ( int ( krepo.getValue () ) )
        root = hkGetRepo ( space )
        project = hkGetProject ()
        path = os.path.join ( root, project ) 

        it = 0
        klastval = None
        
        while it < params.index ( param )  :        
            klast = n.knob ( params [ max ( 0, it-1 ) ] )
            klastval = klast.enumName ( int( klast.getValue () ) )
            kcur = n.knob ( params [ it ] )
            
            if not ( klastval == None )  :
                kcurval = kcur.enumName ( int( kcur.getValue () ) )
                if not ( kcurval == None ) : 
                    path = os.path.join ( path, kcurval )
            
            else :
                klastval = None
            
            kcur = None        
            it += 1
        
        updated = list ()
    
        if ( klastval != None ) or (it == 0):
            if os.path.exists ( path ) :
                
                if os.path.isdir ( path ):
                    lsdir = os.listdir ( path )
                    
                    for f in lsdir:
                        fpath = os.path.join ( path, f )
                        
                        if os.path.isdir ( fpath ) :

                            if param in paramfilter :

                                if f in paramfilter [ param ] :
                                    updated.append ( f )                            
                            else :
                                updated.append ( f )

                k.setValues ( updated )

        values = k.values ()

        if ( len ( values ) > 0 ) and  ( k.enumName ( int ( k.getValue () ) ) == None ) :
            k.setValue ( values[0] )

        kpath.setValue ( hkGetPath ( n ) )


def hkReadUpdateAll ( node = None, params = ( "type", "asset", "task", "fork", "version", "layer", "aov" ) ) :
    for param in params :
        hkReadUpdate ( node = node, param = param )

def hkGetPath ( node = None ) :

    project = hkGetProject ()
    project = project.lower()
    project = project.replace( " ", "" )

    krepo = node.knob ( 'repository' )
    kextension = node.knob ( 'extension' )
    
    if node == None or kextension == None :
        return

    if krepo != None :
        repo = str ( krepo.value () )
        root = hkGetRepo ( repo )
        path = os.path.join ( root, project)
        fname = project
        params = hkGetParams ()

        for param in params:
            k = node.knob ( param )
            if k != None :
                value = str ( k.value () )

                if value != None and value != "0" :
                    value = value.lower().replace ( " ", "" )
                    
                    if param != "version":
                        fname += "_%s" % value
                    
                    path = os.path.join ( path, value )

        fname += ".%s.%s" % ( "%04d", kextension.enumName ( int ( kextension.getValue() ) ) )
        path = os.path.join ( path, fname )

        return path
    
def hkWriteRender( node = None ):
    pass

def hkReadCreate () :
    group = nuke.createNode ( "Group" )
    group [ "name" ].setValue ( "ReadAsset" )
    group.begin ()
    read = nuke.createNode ( "Read" )
    output = nuke.createNode ( "Output" )
    group.end ()
    
    assetTab = nuke.Tab_Knob ( "Asset" )
    settingsTab = nuke.Tab_Knob ( "Settings" )

    #Setup file python expression
    params = ( "type", "asset", "task", "fork", "version", "layer", "aov" )
    filecmd = "[ value parent.path ]"

    #Create and setup knobs
    group.addKnob ( assetTab )
    repository = ( "network", "local" )
    krepo = nuke.Enumeration_Knob ( "repository", "repository", repository ) 
    repoup = "hkReadUpdateAll ()"
    krepoup = nuke.PyScript_Knob ( "repositoryup", "Update", repoup )
    group.addKnob ( krepo )
    group.addKnob ( krepoup )
    
    for param in params :
        knob = nuke.Enumeration_Knob ( param, param, list () )
        func = "hkReadUpdate ( param = '%s' )" % param
        group.addKnob ( knob )
    
    kextension = nuke.Enumeration_Knob ( "extension", "extension", list(("exr","tif","jpg")) )
    kpath = nuke.File_Knob ( "path", "path" )
    group.addKnob ( kextension )
    group.addKnob ( kpath )
    
    kfile = read [ "file" ]
    kfile.setValue ( filecmd )
    klabel = group [ "label" ]
    klabel.setValue ("[value type]_[value asset]_[value task]_[value fork]_[value layer]_[value aov]")
    kpostage_stamp = group [ "postage_stamp" ]
    kpostage_stamp.setValue ( True )

    group.addKnob ( settingsTab )
    # group.addKnob ( nuke.Text_Knob ("divName","",""))
    group.addKnob ( read["cacheLocal"])
    group.addKnob ( read["format"])
    group.addKnob ( read["first"])
    group.addKnob ( read["before"])
    group.addKnob ( read["last"])
    group.addKnob ( read["after"])
    group.addKnob ( read["frame_mode"])
    group.addKnob ( read["frame"])
    group.addKnob ( read["origfirst"])
    group.addKnob ( read["origlast"])
    group.addKnob ( read["on_error"])
    group.addKnob ( read["reload"])
    group.addKnob ( read["colorspace"])
    group.addKnob ( read["premultiplied"])
    group.addKnob ( read["raw"])
    group.addKnob ( read["auto_alpha"])
    hkReadUpdateAll ( node = group )

def hkWriteCreate ():
    group = nuke.createNode ( "Group" )
    group [ "name" ].setValue ( "WriteAsset" )

    #Create the gizmo
    group.begin ()
    input = nuke.createNode ( "Input" )
    input["name"].setValue("Input")
    write = nuke.createNode ( "Write" )
    write["name"].setValue("Write")
    output = nuke.createNode ( "Output" )
    output["name"].setValue("Output")
    group.end ()

    #Create tabs
    assetTab = nuke.Tab_Knob ( "Asset" )
    settingsTab = nuke.Tab_Knob ( "Settings" )

    #Setup file python expression
    params = ( "type", "asset", "task", "fork" )
    
    #Create and setup knobs
    group.addKnob ( assetTab )
    repository = ["local"]
    krepo = nuke.Enumeration_Knob ( "repository", "repository", repository ) 
    repoup = "hkReadUpdateAll ()"
    krepoup = nuke.PyScript_Knob ( "repositoryup", "Update", repoup )
    group.addKnob ( krepo)
    group.addKnob ( krepoup)
    
    for param in params :
        knob = nuke.Enumeration_Knob ( param, param, list () )
        func = "hkReadUpdate ( param = '%s' )" % param
        group.addKnob ( knob )
           
    kversion = nuke.String_Knob ("version","version","default")
    kextension = nuke.Enumeration_Knob ( "extension", "extension", list ( ("exr", "tif", "jpg") ) )
    kpath = nuke.File_Knob ( "path", "path" )

    filecmd = "[ value parent.path ]"
    kfile = write [ "file" ]
    kfile.setValue ( filecmd )
    group.addKnob ( kversion )
    group.addKnob ( kextension )
    group.addKnob ( kpath )

    group.addKnob ( settingsTab )
    # group.addKnob ( nuke.Text_Knob ("divName","",""))
    group.addKnob ( write["channels"])
    group.addKnob ( write["colorspace"])
    group.addKnob ( write["premultiplied"])
    group.addKnob ( write["raw"])
    
    group.addKnob ( nuke.Text_Knob("divName","",""))
    group.addKnob ( write.knob("render_order") )
    group.addKnob ( write.knob("Render") )
    group.addKnob ( write.knob("first") )
    group.addKnob ( write.knob("last") )
    group.addKnob ( write.knob("use_limit") )
    group.addKnob ( write.knob("reading") )
    group.addKnob ( write.knob("checkHashOnRead") )
    group.addKnob ( write.knob("on_error") )
    group.addKnob ( write.knob("reload") )

    # klabel = group [ "label" ]
    # klabel.setValue ("[value type]_[value asset]_[value task]_[value fork]_[value version]")
    hkReadUpdateAll ( node = group, params = params )

# hkReadCreate ()