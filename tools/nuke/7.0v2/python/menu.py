print "hk-nuke: initialize menu"

def hkCreateMenu ():
	hkmenu_name = "Homeworks"
	hkmenu = nuke.menu( 'Nuke' ).addMenu(hkmenu_name)
	nuke.menu ( 'Nuke' ).addCommand( '%s/asset manager' % hkmenu_name, lambda: ASSET_MANAGER.show () )
	nuke.menu ( 'Nuke' ).addCommand( '%s/2D/Read Images' % hkmenu_name, lambda: hkReadImagesCreate (), "r", "ReadAsset.png" )
	nuke.menu ( 'Nuke' ).addCommand( '%s/2D/Write Images' % hkmenu_name, lambda: hkWriteImagesCreate (), "w", "WriteAsset.png" )
	nuke.menu ( 'Nuke' ).addCommand( '%s/3D/Read Geometry' % hkmenu_name, lambda: hkReadGeometryCreate (), "", "ReadAsset.png" )
	nuke.menu ( 'Nuke' ).addCommand( '%s/3D/Read Camera' % hkmenu_name, lambda: hkReadCameraCreate (), "", "ReadAsset.png" )

	hkmenu.addSeparator ()
	aboutmsg = "pipeline %s" % ( os.getenv ( "HK_PIPELINE_VER" ) )
	nuke.menu ( 'Nuke' ).addCommand( '%s/about' % hkmenu_name, lambda: nuke.message ( aboutmsg ) )

def hkRegisterGizmo ():
	# Custom Lab Tools
	toolbar = nuke.toolbar("Nodes")
	m = toolbar.addMenu("Homeworks", icon="homeworks.png")
	m.addCommand ( "Lens Simulation", lambda: nuke.createNode ( 'LensSim' ), "", "LensSim.png" )
	m.addCommand ( 'Read Images', lambda: hkReadImagesCreate (), "", "ReadAsset.png")
	m.addCommand ( 'Write Images', lambda: hkWriteImagesCreate (), "", "WriteAsset.png")

hkCreateMenu ()
hkRegisterGizmo ()