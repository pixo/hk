import pipeline.apps as apps
import pipeline.utils as utils
import pipeline.core as core
import glob, os, PythonQt
import PySide.QtGui as QtGui 
import commands

CC_PATH = utils.getCCPath()
PROJECT = utils.getProjectName()

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
	root = os.path.join ( root, wedge, "%s_%s_%s." % ( asset_id, "$VARIATION",channel_name ) )
	
	if  animation :
		mri_pattern = "$UDIM.$FRAME.tif"

	else :
		mri_pattern = "$UDIM.tif"

	path = root + mri_pattern 

	"Exporting"
	chan = geo.channel ( channel_name )
	    
	"flatten and export each image in the channel"
	chan.exportImagesFlattened ( path )
	pattern = path.replace ( "$VARIATION", "*" )
	pattern = pattern.replace ( "$UDIM", "*" )
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

def hkImportChannel ( path = "", doc_id = "", channel_name = None, variation = 1, geo = None, animation = False ):
	"Check input geo"
	if geo == None :
		geo = mari.geo.current ()

	"Get geo and channel"
	geo_name = geo.name ()

	"Check channel name"
	if channel_name == None :
		channel_name = geo.currentChannel().name()

	if not channel_name in geo.channelList () :
		geo.createChannel ( channel_name, 4096, 4096, 16 )
		
	chan = geo.channel ( channel_name )
	shd = geo.findShader("Norman")

	"Create template"
	root = os.path.join ( path, "%s_%s_%s." % ( doc_id, variation, channel_name ) )
	
	if  animation :
		mri_pattern = "$UDIM.$FRAME.tif"

	else :
		mri_pattern = "$UDIM.tif"

	path = root + mri_pattern 

	"Importing"
	chan.importImages ( path )

	"link channel to shader input"

	if channel_name in ( "diff1col", "spec1", "spec1rgh", "dirt", "dirtcol" ):
		shd.setInput ( channel_name, chan )
	
	print "hkImportChannel () : %s %s " % ( root, channel_name )
	return True

def hkImportChannels ( path, doc_id, ver ):
	""""""
	texture_type = utils.getTextureTypes ()

	print "doc_id:", doc_id
	geo = mari.geo.current ()
	variation = PythonQt.QtGui.QInputDialog.getText ( PythonQt.QtGui.QDialog(), 'Input Dialog', 'Variation:')
	#TODO:check if ID exists
	gid = geo.metadata ("id")
	ismod = ( gid.replace ( "mod", "tex" ) == doc_id )
	isrig = ( gid.replace ( "rig", "tex" ) == doc_id )

	if ismod or isrig :
		
		for channel_name in texture_type :
			texls = glob.glob ( os.path.join ( path, "*_%s_%s.*.tif" % ( variation, channel_name ) ) )

			if len ( texls ) > 0 :
				hkImportChannel ( path, doc_id, channel_name, variation, geo, False )

	else:
		print "Not a proper asset"

def hkImportGeo ( path, doc_id, ver ):
	files = glob.glob ( os.path.join( path, "*.mb" ) )
	file = files[0] 
	subd = PythonQt.QtGui.QInputDialog.getText ( PythonQt.QtGui.QDialog(), 'Input Dialog', 'Subd level:')
	print "importing %s " % file

	dst = core.getWorkspaceFromId ( doc_id )
	fname = os.path.basename ( file ) 
	fobj, ext = os.path.splitext ( fname ) 
	fobj = "%s_subd%s.obj" % ( fobj, subd )
	dst = os.path.join ( dst, fobj)
	cmds = "hk-asset-subd -i %s -s %s -o %s" % ( file, subd, dst )
	print "cmds ", cmds
	commands.getoutput ( cmds )
	geos = mari.geo.load ( dst )

	for geo in geos :
		geo.setMetadata ( "assetversion", ver )
		geo.setMetadata ( "textureversion", ver )
		geo.setMetadata ( "id", doc_id )
		geo.setMetadataEnabled ( "assetversion", False )
		geo.setMetadataEnabled ( "textureversion", False )
		geo.setMetadataEnabled ( "id", False )
		shd = geo.createShader( "Norman", "Lighting/Standalone/Norman" )
		shd.makeCurrent ()

def hkImportFile ( path, doc_id, ver ):
	project, typ, asset, task, fork = doc_id.split("_")
	
	if task == "tex":
		hkImportChannels ( path, doc_id, ver )

	else:
		hkImportGeo ( path, doc_id, ver )

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""Asset Manager"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def assetExport ( source = "", obj=True, abc=True, gpj = True, first= 1, last = 1 ):
    cmd = """hk-asset-export -i %s -obj %d -abc %d -gpj %d -f %d -l %d """ % ( source, int(obj), int(abc), int( gpj ), first, last )   
    return commands.getoutput( cmd )
    

def pushMari ( db = None, doc_id = "", description = "", item = None,
               screenshot = "", msgbar = False, progressbar = False,
               selection = False, rename = True, extension = ".mb" ) :

    
    fname = os.path.join ( "/tmp", "%s%s" % ( core.hashTime (), extension ) )
    return True

def pullMari (db = None, doc_id = "", ver = "latest" ):
    path = core.getAssetPath ( doc_id, ver )
    files = glob.glob ( os.path.join ( path, "*.mra" ) )
    hkcmds.openFile ( files[0] )
        
def pushFile ( db = None, doc_id = "", description = "", item = None, 
               screenshot = "", msgbar = False, progressbar = False ) :
    return pushMari ( db , doc_id, description, item, screenshot, msgbar,
                      progressbar, selection = False, rename = True, extension = ".mb" )
        
def pushSelected ( db = None, doc_id = "", description = "", item = None,
                   screenshot = "", msgbar = False, progressbar = False ) :
    return pushMari ( db , doc_id, description, item, screenshot, msgbar,
                      progressbar, selection = True, rename = True, extension = ".mb" )
           
class UiMariAM(apps.UiAssetManager):
     
    defaultfilter = "ma"
    launcher = "mari"
    defaultsuffix = "mb"
         
    def importVersion ( self ) :
        item = self.treeWidget_a.currentItem ()
        doc_id = item.parent().hkid
        ver = int ( item.text ( 0 ) )
        self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str ( ver ) ) )
     
        path = core.getAssetPath ( doc_id, ver )
        print "importVersion():", path, doc_id, ver       
        hkImportFile ( path, doc_id = doc_id, ver = ver )
        self.statusbar.showMessage("%s pulled" % path )

    def pushVersion ( self ) :
        item = self.treeWidget_a.currentItem ()
        doc_id = item.hkid
        # self.pushVersionWidget = UipushMari ( None, self.db, doc_id, item )
        # self.pushVersionWidget.show ()
        
    def pullVersion ( self ) :
        self.progressBar.setHidden ( False )
        item = self.treeWidget_a.currentItem ()
        doc_id = item.parent().hkid
        ver = int ( item.text ( 0 ) )
        self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str(ver) ) )
        
        pull = core.pull ( doc_id = doc_id, ver = ver , extension = ".mb",
                           progressbar = self.progressBar,
                           msgbar = self.statusbar.showMessage)
        if pull :
            # hkcmds.openFile ( pull [ 0 ] )
            self.statusbar.showMessage("%s %s pulled" % ( doc_id, str(ver) ))
         
        self.progressBar.setHidden ( True )
        
    def openFile ( self, fname ) :
        hkcmds.openFile ( fname )

    def contextMenuFork ( self, item ) :
		item = self.treeWidget_a.currentItem ()       
		menu = QtGui.QMenu ()   

		doc_id = item.hkid
		path = core.getWorkspaceFromId ( doc_id )

		if os.path.exists ( path ) :
			icon_push = QtGui.QIcon ( os.path.join ( CC_PATH, "push.png" ) )
			actionPush = menu.addAction ( icon_push, 'Push a new %s version' % doc_id )
			actionPush.triggered.connect ( self.pushVersion )

			icon_open = QtGui.QIcon ( os.path.join ( CC_PATH, "open.png" ) )
			actionOpen = menu.addAction ( icon_open, 'Open from Workspace' )
			actionOpen.triggered.connect ( self.openFileDialog )

			icon_saveas = QtGui.QIcon ( os.path.join ( CC_PATH, "save.png" ) )
			actionSaveas = menu.addAction ( icon_saveas, 'Save to Workspace' )
			actionSaveas.triggered.connect ( self.saveFileDialog )

		else:
			icon_new = QtGui.QIcon ( os.path.join ( CC_PATH, "add.png" ) )
			action = menu.addAction ( icon_new, 'Create workspace' )
			action.triggered.connect ( self.createWorkspace )
		        
		menu.exec_ ( QtGui.QCursor.pos () )

    def contextMenuVersion ( self, item ) :
        menu = QtGui.QMenu ()
        
        icon_pull = QtGui.QIcon ( os.path.join ( CC_PATH, "pull.png" ) )
        action_pull = menu.addAction ( icon_pull, 'Pull version %s' % item.text (0) )
        action_pull.triggered.connect ( self.pullVersion )
        
        icon_import = QtGui.QIcon ( os.path.join ( CC_PATH, "import.png" ) )
        action_import = menu.addAction ( icon_import, 'Import version %s' % item.text (0) )
        action_import.triggered.connect ( self.importVersion )
        
        menu.exec_( QtGui.QCursor.pos () )
        
ASSET_MANAGER = UiMariAM ()

"""Create Export Actions"""
def hkCreateExportActions ():

	"""Open Asset Manager"""
	actionAssetManager = mari.actions.create ( 'Homeworks/AssetManager', 'ASSET_MANAGER.show ()')
	mari.menus.addAction ( actionAssetManager, "MainWindow/Homewor&ks" )
    
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