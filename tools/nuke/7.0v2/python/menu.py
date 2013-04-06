print "hk-nuke: initialize menu"

def hkCreateMenu ():
	hkmenu_name = "Homeworks"
	hkmenu = nuke.menu( 'Nuke' ).addMenu(hkmenu_name)
	nuke.menu ( 'Nuke' ).addCommand( '%s/asset manager' % hkmenu_name, lambda: ASSET_MANAGER.show() )
	hkmenu.addSeparator ()
	aboutmsg = "pipeline %s" % ( os.getenv ( "HK_PIPELINE_VER" ) )
	nuke.menu ( 'Nuke' ).addCommand( '%s/about' % hkmenu_name, lambda: nuke.message ( aboutmsg ) )

def hkRegisterGizmo ():
	# Custom Lab Tools
	toolbar = nuke.toolbar("Nodes")
	m = toolbar.addMenu("Homeworks", icon="homeworks.png")
	m.addCommand("WriteAsset", lambda: nuke.createNode( 'WriteAsset' ), 'w', "WriteAsset.png")
	m.addCommand("ReadAsset", lambda: nuke.createNode( 'ReadAsset' ), 'r', "ReadAsset.png")

hkCreateMenu ()
hkRegisterGizmo ()