print "hk-nuke: importing reader"
import nuke,os
import pipeline.utils as utils

HK_ASSET_TYPE = utils.getAssetTypes ()
HK_TASK_TYPE = utils.getTaskTypes ()

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
        
     elif name == "repository":
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
                #Add check custom value
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

def hkReadUpdateAll ( node = None, params = ( "type", "asset", "task", "fork", "version", "layer", "aov" ) ) :
    for param in params :
        hkReadUpdate ( node=node, param = param )


def hkReadGetPath ( node = None ) :
    project = hkGetProject ()
    project = project.lower()
    project = project.replace( " ", "" )

    repo = str ( node.knob ( 'repository' ).value() )
    root = hkGetRepo ( repo )
    path = os.path.join ( root, project)
    fname = project
    params = hkGetParams ()

    for param in params:
        k = node.knob ( param )
        if k != None :
            value = str ( k.value() )

            if value != None :
                value = value.lower().replace ( " ", "" )
                fname += "_%s" % value
                path = os.path.join ( path, value )

    fname += ".%s.exr" % "%04d"
    path = os.path.join ( path, fname )

    return path
    
def hkWriteRender( node = None ):
    pass

def hkReadCreate () :
    group = nuke.createNode ( "Group" )
    group [ "name" ].setValue ( "ReadAsset" )
    group.begin ()
    reader = nuke.createNode ( "Read" )
    output = nuke.createNode ( "Output" )
    group.end ()

    #Setup file python expression
    params = ( "type", "asset", "task", "fork", "version", "layer", "aov" )
    filecmd = "[ python hkReadGetPath ( nuke.thisParent() ) ]"

    #Create and setup knobs
    repository = ( "network", "local" )
    krepo = nuke.Enumeration_Knob ( "repository", "repository", repository ) 
    repoup = "hkReadUpdateAll ()"
    krepoup = nuke.PyScript_Knob ( "repositoryup", "Update", repoup )
    group.addKnob ( krepo)
    group.addKnob ( krepoup)
    
    for param in params :
        knob = nuke.Enumeration_Knob ( param, param, list () )
        func = "hkReadUpdate ( param = '%s' )" % param
        group.addKnob ( knob )
    
    kfile = reader [ "file" ]
    kfile.setValue ( filecmd )
    klabel = group [ "label" ]
    klabel.setValue ("[value type]_[value asset]_[value task]_[value fork]_[value layer]_[value aov]")
    kpostage_stamp = group [ "postage_stamp" ]
    kpostage_stamp.setValue ( True )
    hkReadUpdateAll ( node = group )

def hkWriteCreate ():
    group = nuke.createNode ( "Group" )
    group [ "name" ].setValue ( "WriteAsset" )

    group.begin ()
    input = nuke.createNode ( "Input" )
    write = nuke.createNode ( "Write" )
    output = nuke.createNode ( "Output" )
    group.end ()

    #Setup file python expression
    params = ( "type", "asset", "task", "fork" )
    # filecmd = "[ python hkReadGetPath ( nuke.thisParent() ) ]"

    #Create and setup knobs
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

    filecmd = "[ python hkReadGetPath ( nuke.thisParent() ) ]"
    kfile = write [ "file" ]
    kfile.setValue ( filecmd )

    group.addKnob ( kversion )

    group.addKnob ( nuke.Text_Knob ("divName","",""))
    group.addKnob ( write["channels"])
    group.addKnob ( write["colorspace"])
    group.addKnob ( write["premultiplied"])
    group.addKnob ( write["raw"])
    group.addKnob ( write["file_type"])

    group.addKnob ( nuke.Text_Knob("divName","",""))
    group.addKnob ( write.knob("render_order") )
    group.addKnob ( write.knob("Render") )

    klabel = group [ "label" ]
    klabel.setValue ("[value type]_[value asset]_[value task]_[value fork]_[value version]")
    hkReadUpdateAll ( node = group, params = params )

hkWriteCreate ()