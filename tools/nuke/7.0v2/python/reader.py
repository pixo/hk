print "hk-nuke: importing reader"
import nuke,os
import pipeline.utils as utils

HK_ASSET_TYPE = utils.getAssetTypes ()
HK_TASK_TYPE = utils.getTaskTypes ()

def hkReadChanged () :
     n = nuke.thisNode()
     k = nuke.thisKnob()

     if k.name() in ( "type", "asset", "task", "fork", "version", "layer", "aov" ):
        pass
       # print "version"
       # n['gain'].setValue(k.value())
     elif k.name() == "dir":
        pass
        # print "directory"
       # n['gamma'].setValue(k.value())
    # nuke.addKnobChanged(gangGammaGainSliders, nodeClass="ColorCorrect")

nuke.addKnobChanged ( hkReadChanged )

def hkGetRepo ( space = "network" ) :
    repository = { "network":"HK_REPO", "local":"HK_USER_REPO" }
    root = os.getenv ( repository [ space ] )
    return root

def hkGetProject () :
    return os.getenv ( "HK_PROJECT" )

def hkReadUpdate ( part ) :
    param = ( "type", "asset", "task", "fork", "version", "layer", "aov" )
    paramfilter = { "type":HK_ASSET_TYPE , "task":HK_TASK_TYPE }
    n = nuke.thisNode ()
    k = n.knob ( part )
    krepo = n.knob  ( "repository" )
    space = krepo.enumName ( int ( krepo.getValue () ) )
    root = hkGetRepo ( space )
    project = hkGetProject ()
    path = os.path.join ( root, project ) 
    # print path

    print "//////////////////////////////////////",part
    it = 0
    klastval = None
    while it < param.index ( part )  :        
        klast = n.knob ( param [ max ( 0, it-1 ) ] )
        klastval = klast.enumName ( int( klast.getValue () ) )
        kcur = n.knob ( param [ it ] )
        
        if not ( klastval == None )  :
            print klastval,  " not ( klastval == None ) or not ( klastval == list () ) "
            kcurval = kcur.enumName ( int( kcur.getValue () ) )

            if not ( kcurval == None ) : 
              path = os.path.join ( path, kcurval )
              # print "while:", param [ it ], path
        else :
            klastval = None
        # print param [ max ( 0, it-1 ) ], "klast", klast.enumName ( int( klast.getValue () ) ), max(it-1,0)
        # print part, "kcur", kcur.enumName ( int( kcur.getValue () ) ), it

        kcur = None        
        it += 1

    updated = list ()

    
    if ( klastval != None ) or (it == 0):
        print "entering",klastval
        if os.path.exists ( path ) :
            print path 
            
            if os.path.isdir ( path ):
                lsdir = os.listdir ( path )
                
                for f in lsdir:
                    fpath = os.path.join ( path, f )
                    
                    if os.path.isdir ( fpath ) :

                        if part in paramfilter :

                            if f in paramfilter [ part ] :
                                updated.append ( f )
                        
                        else :
                            updated.append ( f )

    k.setValues ( updated )

def hkReadUpdateAll () :
    param = ( "type", "asset", "task", "fork", "version", "layer", "aov" )
    for p in param :
        hkReadUpdate ( p )

def hkReadGetPath ( repo ="network", assettype = "shot", asset = "Empty", task = "ren", fork = "main", version = "001",  layer = "fg", aov = "beauty" ) :
    root = hkGetRepo ( repo )
    project = hkGetProject ()
    project = project.lower()
    project = project.replace( " ", "" )
    assettype = assettype.lower().replace ( " ", "" )
    asset = asset.lower().replace ( " ", "" )
    task = task.lower().replace ( " ", "" )
    fork = fork.lower().replace ( " ", "" )
    layer = layer.lower().replace ( " ", "" )
    aov = aov.lower().replace ( " ", "" )
    fname = "%s_%s_%s_%s_%s_%s_%s.%s.exr" % ( project, assettype, asset, task, fork, layer, aov, "%04d" )
    # print fname

    path = os.path.join ( root, project, assettype, asset, task, fork, version, layer, aov, fname )
    return path

def hkReadCreate () :
    group = nuke.createNode ( "Group" )
    group [ "name" ].setValue ( "hkRead" )
    group.begin ()
    reader = nuke.createNode ( "Read" )
    output = nuke.createNode ( "Output" )
    group.end ()

    #Setup file python expression
    params = ( "type", "asset", "task", "fork", "version", "layer", "aov" )
    filecmd = "[ python hkReadGetPath ( "

    #Create and setup knobs
    repository = ( "network", "local" )
    krepo = nuke.Enumeration_Knob ( "repository", "repository", repository ) 
    repoup = "hkReadUpdateAll ()"
    krepoup = nuke.PyScript_Knob ( "repositoryup", "Update All", repoup )
    group.addKnob ( krepo)
    group.addKnob ( krepoup)
    filecmd += "nuke.thisParent().knob('repository').value(),"
    
    for param in params :
        knob = nuke.Enumeration_Knob ( param, param, list () )
        func = "hkReadUpdate ( '%s' )" % param
        knobup = nuke.PyScript_Knob ( "%s_up" % param, "Update", func )
        group.addKnob ( knob )
        group.addKnob ( knobup )
        filecmd += "nuke.thisParent().knob('%s').value()" % param
        
        if param != params[-1] :
            filecmd += ","

    filecmd += " ) ]"
    kfile = reader [ "file" ]
    kfile.setValue ( filecmd )

# hkReadCreate ()