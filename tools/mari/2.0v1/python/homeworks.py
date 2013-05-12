import pipeline.utils as utils
import pipeline.core as core
import glob, PythonQt

def hkTextureExport ( pattern ):
    files = glob.glob ( pattern )
    #TODO: support progressbar for textures optimisation
    for file in files :
        # core.textureOptimise ( file )
        core.textureBuild ( file )

def hkExportChannel ( channel_name = None, wedge = "wedge1", geo = None, dialog = False, animation = False ):
	
	"Check input geo"
	if geo == None :
		geo = mari.geo.current ()

	"Get geo and channel"
	geo_name = geo.name ()

	"Check channel name"
	if channel_name == None :
		channel_name = geo.currentChannel().name() 

	"Reconstruct asset name"
	slugs = geo_name.split ("_")
	asset_id = "%s_%s_%s_%s_%s" % ( slugs[0], slugs[1], slugs[2], "tex", slugs[4] )

	"Get wedge name if needed"
	if dialog :
		wedge = PythonQt.QtGui.QInputDialog.getText ( PythonQt.QtGui.QDialog(), 'Input Dialog', 'Wedge name:')
		if wedge == "": wedge = "wedge"

	"Create template"
	root = core.getRootAssetPath ( asset_id, True )
	root = os.path.join ( root, wedge, "%s_%s." % ( asset_id, channel_name ) )
	
	if  animation :
		mri_pattern = "$UDIM.$FRAME.tif"
	else :
		mri_pattern = "$UDIM.tif"

	path = root + mri_pattern 

	"Exporting"
	chan = geo.channel ( channel_name )
	    
	"flatten and export each image in the channel"
	chan.exportImagesFlattened ( path )
	pattern = path.replace ( "$UDIM", "*" )
	hkTextureExport ( pattern )
	print "hkExportChannel () : %s %s " % ( root, channel_name )
	return True

def hkExportAllChannels ( wedge = "wedge1", geo = None, dialog = False, animation = False ):
	texture_type = utils.getTextureTypes ()
	exported = ""

	"Check input geo"
	if geo == None :
		geo = mari.geo.current ()

	"Processing export"
	channel_list = geo.channelList ()
	if dialog :
		wedge = PythonQt.QtGui.QInputDialog.getText ( PythonQt.QtGui.QDialog(), 'Input Dialog', 'Wedge name:')
		if wedge == "": wedge = "wedge"

	for chan in channel_list:
		channel_name = chan.name ()

		if channel_name in texture_type :
			hkExportChannel ( channel_name, wedge, geo )

		else:
			print "hkExportAllChannels (): %s channel skipped" % channel_name

	return True

"""Create Export Actions"""
def hkCreateExportActions ():
    """Export current flattened channel for current geometry"""
    actionExportChannel = mari.actions.create ( 'Homeworks/Export/Current Channel', 'hkExportChannel ( dialog = True )' )
    mari.menus.addAction ( actionExportChannel, "MainWindow/Homewor&ks/&Export" )
    actionExportChannel.setShortcut ( "Shift+E" )

    """Export all channels flattened for current geometry"""
    actionExportAllChannels = mari.actions.create ( 'Homeworks/Export/All Channels', 'hkExportAllChannels ( dialog = True )' )
    mari.menus.addAction ( actionExportAllChannels, "MainWindow/Homewor&ks/&Export" )
    actionExportAllChannels.setShortcut ( "Ctrl+Shift+E" )

    """Export current flattened channel for current geometry animation"""
    actionExportChannelAnim = mari.actions.create ( 'Homeworks/Export/Current Channel Animation', 'hkExportChannel ( dialog = True, animation = True )' )
    mari.menus.addAction ( actionExportChannelAnim, "MainWindow/Homewor&ks/&Export" )

    """Export all channels flattened for current geometry animation"""
    actionExportAllChannelsAnim = mari.actions.create ( 'Homeworks/Export/All Channels Animation', 'hkExportAllChannels ( dialog = True, animation = True )' )
    mari.menus.addAction ( actionExportAllChannelsAnim, "MainWindow/Homewor&ks/&Export" )

"""Create Actions"""
def hkCreateActions ():
    hkCreateExportActions ()

hkCreateActions ()
