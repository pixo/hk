import pipeline.utils as utils
import pipeline.core as core
import glob

def hkTextureExport ( pattern ):
    files = glob.glob ( pattern )
    #TODO: support progressbar for textures optimisation
    for file in files :
        # core.textureOptimise ( file )
        core.textureBuild ( file )

def hkExportChannel ( channel_name = None, wedge = "wedge1", geo = None ):
	
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
	asset_id = "%s_%s_%s_%s_%s_tex" % ( slugs[0], slugs[1], slugs[2], slugs[3], slugs[4] )

	"Create template"
	root = core.getRootAssetPath ( asset_id, True )
	root = os.path.join ( root, wedge, "%s_%s." % ( asset_id, channel_name ) )
	# TODO : support animation $FRAME
	path = root + "$UDIM.tif" 

	"Exporting"
	chan = geo.channel ( channel_name )
	    
	"flatten and export each image in the channel"
	chan.exportImagesFlattened ( path )
	pattern = path.replace ( "$UDIM", "*" )
	hkTextureExport ( pattern )
	print "hkExportChannel () : %s %s " % ( root, channel_name )
	return True

def hkExportAllChannels ( wedge = "wedge1", geo = None ):
	texture_type = utils.getTextureTypes ()
	exported = ""

	"Check input geo"
	if geo == None :
		geo = mari.geo.current ()

	"Processing export"
	channel_list = geo.channelList ()

	for chan in channel_list:
		channel_name = chan.name ()

		if channel_name in texture_type :
			hkExportChannel ( channel_name, wedge, geo )

		else:
			print "hkExportAllChannels (): %s channel skipped" % channel_name

	return True

"""Create Export Actions"""
def hkCreateExportActions ():
    """Export all channels flattened for current geometry"""
    actionExportChannel = mari.actions.create ( 'Homeworks/Export/Export Flattened For Current Geo', 'hkExportChannel ()' )
    mari.menus.addAction ( actionExportChannel, "MainWindow/Homewor&ks/&Export" )
    actionExportChannel.setShortcut ( "Shift+E" )

    """Export all channels flattened for current geometry"""
    actionExportAllChannels = mari.actions.create ( 'Homeworks/Export/Export All Flattened For Current Geo', 'hkExportAllChannels ()' )
    mari.menus.addAction ( actionExportAllChannels, "MainWindow/Homewor&ks/&Export" )
    actionExportAllChannels.setShortcut ( "Ctrl+Shift+E" )

"""Create Actions"""
def hkCreateActions ():
    hkCreateExportActions ()

hkCreateActions ()
