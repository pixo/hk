print "hk-nuke: initialize menu"

hkmenu_name="Homeworks"
hkmenu = nuke.menu( 'Nuke' ).addMenu(hkmenu_name)

nuke.menu( 'Nuke' ).addCommand( '%s/read' % hkmenu_name, lambda: hkReadCreate() )
hkmenu.addSeparator()
aboutmsg = "pipeline %s" % (os.getenv("HK_PIPELINE_VER"))
nuke.menu( 'Nuke' ).addCommand( '%s/about' % hkmenu_name, lambda: nuke.message(aboutmsg) )



