'''
Created on Feb 9, 2013

@author: pixo
'''
import glob, os, commands
import maya.cmds as cmds
import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI
import pipeline.apps as apps
import pipeline.utils as utils
import pipeline.core as core
import PySide.QtGui as QtGui

CC_PATH = utils.getCCPath()
PROJECT = utils.getProjectName()

def assetExport ( source = "", obj=True, abc=True, first= 1, last = 1 ):
    cmd = """hk-asset-export -i %s -obj %d -abc %d -f %d -l %d """ % ( source, int(obj), int(abc), first, last )   
    return commands.getoutput( cmd )

def createAssetStructure ( doc_id, msgbar ):

  assetList = cmds.ls ( "%s:*" % doc_id )
  if len ( assetList ) == 0 :

    """Set the root namespace"""
#     if not cmds.namespace ( exists = doc_id ) :
#         cmds.namespace ( add = doc_id )
#         cmds.namespace ( set = doc_id )

    """create structure"""
    root = cmds.createNode ( "transform", n = "root" )
    trs_master = cmds.createNode ( "transform", n = "master_trs" )
    trs_shot = cmds.createNode ( "transform", n = "shot_trs" )
    trs_aux = cmds.createNode ( "transform", n = "aux_trs" )

    grp_model = cmds.createNode ( "transform", n = "model_grp" )
    grp_rig = cmds.createNode ( "transform", n = "rig_grp" )
    grp_look = cmds.createNode ( "transform", n = "look_grp" )
    grp_render = cmds.createNode ( "transform", n = "render_grp" )
#     cmds.namespace ( set = ":" )

    cmds.parent ( render_grp, model)
    cmds.parent ( model, rig , look, trs_aux )
    cmds.parent ( trs_aux, trs_shot )
    cmds.parent ( trs_shot, trs_master )
    cmds.parent ( trs_master, root )

    """create attribute"""
    cmds.addAttr ( root, shortName = "asset", dataType = "string" )
    cmds.setAttr ( "%s.%s" % ( root, "asset" ), doc_id, typ = "string" )
    cmds.setAttr ( "%s.%s" % ( root, "asset" ), lock = True )
    cmds.addAttr ( root, shortName = "version", attributeType = "short" )
    cmds.setAttr ( "%s.%s" % ( root, "version" ), lock = True )

  else:

    msgbar ( "%s already exists" % doc_id )


def doScreenshot ( filename = "" ) :

    image = api.MImage ()
    view = apiUI.M3dView.active3dView ()
    view.readColorBuffer ( image, True )
    image.resize ( 640, 480, True )
    image.writeToFile ( filename, 'jpg' )
    return filename
    

def saveFile ( filename = "", exportsel = False, msgbar = None ) :
    
    if exportsel :
        if len ( cmds.ls ( sl = True ) ) == 0 :
            msgbar ( "Please select an asset to export" )
            return False
            
    extension = { ".ma":"mayaAscii", ".mb":"mayaBinary", ".obj":"OBJ" }
    ext = os.path.splitext ( filename )[-1]
    
    if ext == "" :
        ext = ".ma"
         
    cmds.file ( filename, force=True, options="v=0;", type = extension[ext],
                pr = True, es = exportsel, ea = (not exportsel))
    
    return os.path.exists ( filename )

def saveSelected ( filename = "", msgbar = None ) :

    saveFile ( filename, True, msgbar )


def openFile ( filename ):

    extension = { ".ma":"mayaAscii", ".mb":"mayaBinary", ".obj":"OBJ" }
    ext = os.path.splitext ( filename )[-1]
    cmds.file ( filename, f=True, options="v=0;", type = extension[ext], o = True )
    

def importFile(filename):

    extension = { ".ma":"mayaAscii", ".mb":"mayaBinary", ".obj":"OBJ" }
    ext = os.path.splitext ( filename )[-1]
    cmds.file ( filename, i=True, options="v=0;", type = extension[ext],
                ra=True, mergeNamespacesOnClash=True, namespace=":", pr=True,
                loadReferenceDepth="all" )  

def pushMaya ( db = None, doc_id = "", description = "", item = None,
               screenshot = "", msgbar = False, progressbar = False,
               selection = False, rename = True, extension = ".mb" ) :

    if not ( screenshot == "" ) :
    
      fname = os.path.join ( "/tmp", "%s%s" % ( core.hashTime (), extension ) )
      
      if saveFile ( fname, selection, msgbar ) :
          destination = core.push ( db, doc_id, fname, description, progressbar,
                             msgbar, rename )
          
          core.transfer ( screenshot, destination, doc_id )
          source = os.path.join ( destination, doc_id + extension )
          
          print "pushMaya():", source
          assetExport ( source )
          
          if msgbar :
              msgbar ( "Done" )
          
          return True
      
      return False

    else :
      msgbar ( "Please make a screenshot" )

def pullMaya (db = None, doc_id = "", ver = "latest" ):

    path = core.getAssetPath ( doc_id, ver )
    files = glob.glob ( os.path.join ( path, "*.ma" ) )
    files.extend ( glob.glob ( os.path.join ( path, "*.mb" ) ) )
    openFile ( files[0] )


def pushFile ( db = None, doc_id = "", description = "", item = None, 
               screenshot = "", msgbar = False, progressbar = False ) :

    return pushMaya ( db , doc_id, description, item, screenshot, msgbar,
                      progressbar, selection = False, rename = True, extension = ".mb" )


def pushSelected ( db = None, doc_id = "", description = "", item = None,
                   screenshot = "", msgbar = False, progressbar = False ) :
    return pushMaya ( db , doc_id, description, item, screenshot, msgbar,
                      progressbar, selection = True, rename = True, extension = ".mb" )

         
class UiPushMaya(apps.UiPush3dPack):
     
     
    launcher = "maya"
    screenshot = "" #doScreenshot ( os.path.join ( "/tmp", "%s.jpg" % core.hashTime() ) )
    fnPush = {
              "model" : pushSelected,
              "retopo" : pushFile,
              "rig" : pushSelected,
              "sculpt" : pushSelected,
              "surface" : pushSelected,
              "texture" : pushFile,
              "animation" : pushFile,
              "camera" : pushSelected,
              "compout" : pushFile,
              "compositing" : pushFile,
              "effect" : pushFile,
              "layout" : pushFile,
              "lighting" : pushFile,
              "matte-paint" : pushFile,
              "render" : pushFile
              }

                
    varpush = {
              'dmp':'mattepaint',
              'mod':'model',
              'rig':'rig',
              'rtp':'retopo',
              'sct':'sculpt',
              'tex':'texture',
              'vfx':'effect',
              'lay':'layout',
              'cam':'camera'
             }
         

    def pushClicked ( self ) :

        db = self.db
        doc_id = self.doc_id
        description = self.plainTextEdit_comments.toPlainText ()
        item = self.item
        taskType = self.varpush [ doc_id.split ( "_" ) [3] ]
        screenshot = self.screenshot
        msgbar = self.labelStatus.setText
        progressbar = self.progressBar
        
        pushed = self.fnPush[ taskType ] ( db, doc_id, description, item,
                                           screenshot, msgbar, progressbar )

        if pushed :
            self.close()
     

    def screenshotClicked ( self ) :
        self.screenshot = doScreenshot ( os.path.join ( "/tmp", "%s.jpg" % core.hashTime() ) )
        self.labelImage.setPixmap ( self.screenshot )
         
 
class UiMayaAM(apps.UiAssetManager):


    defaultfilter = "ma"
    launcher = "maya"
    defaultsuffix = "mb"
    
    def importVersion ( self ) :

        item = self.treeWidget_a.currentItem ()
        doc_id = item.parent().hkid
        ver = int ( item.text ( 0 ) )
        self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str ( ver ) ) )
     
        path = core.getAssetPath ( doc_id, ver )
        files = glob.glob(os.path.join(path,"*.ma"))
        files.extend(glob.glob(os.path.join(path,"*.mb")))
         
        importFile ( files [0] )

        self.statusbar.showMessage("%s pulled" % files[0] )

    def pushVersion ( self ) :

        item = self.treeWidget_a.currentItem ()
        doc_id = item.hkid
        self.pushVersionWidget = UiPushMaya ( None, self.db, doc_id, item )
        self.pushVersionWidget.show ()
        

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
            openFile ( pull [ 0 ] )
            self.statusbar.showMessage("%s %s pulled" % ( doc_id, str(ver) ))
         
        self.progressBar.setHidden ( True )
        

    def openFile ( self, fname ) :

        openFile ( fname )


    def createAssetStructure ( self ) :

      item = self.treeWidget_a.currentItem ()
      doc_id = item.hkid
      createAssetStructure ( doc_id, self.statusbar.showMessage )


    def contextMenuTask ( self, item ) :

        item = self.treeWidget_a.currentItem ()
        menu = QtGui.QMenu ()
        
        """Get workspace"""
        doc_id = item.hkid
        path = core.getWorkspaceFromId ( doc_id )
        
        if os.path.exists ( path ) :
            """Check if workspace exists"""

            """push an asset"""
            icon_push = QtGui.QIcon ( os.path.join ( CC_PATH, "push.png" ) )
            actionPush = menu.addAction ( icon_push, 'Push a new %s version' % doc_id )
            actionPush.triggered.connect ( self.pushVersion )

            """open from workspace"""
            icon_open = QtGui.QIcon ( os.path.join ( CC_PATH, "open.png" ) )
            actionOpen = menu.addAction ( icon_open, 'Open from Workspace' )
            actionOpen.triggered.connect ( self.openFileDialog )

            """save to workspace"""
            icon_saveas = QtGui.QIcon ( os.path.join ( CC_PATH, "save.png" ) )
            actionSaveas = menu.addAction ( icon_saveas, 'Save to Workspace' )
            actionSaveas.triggered.connect ( self.saveFileDialog )

            """save to workspace"""
            icon_create = QtGui.QIcon ( os.path.join ( CC_PATH, "create.png" ) )
            actionSaveas = menu.addAction ( icon_create, 'Create asset structure' )
            actionSaveas.triggered.connect ( self.createAssetStructure )

        else:
            """If not existing create action createWorkspace """
            icon_new = QtGui.QIcon ( os.path.join ( CC_PATH, "add.png" ) )
            createWorkspace = menu.addAction ( icon_new, 'Create workspace' )
            createWorkspace.triggered.connect ( self.createWorkspace )
                    
        menu.exec_ ( QtGui.QCursor.pos () )


    def contextMenuVersion ( self, item ) :

        menu = QtGui.QMenu ()

        """pull asset"""
        icon_pull = QtGui.QIcon ( os.path.join ( CC_PATH, "pull.png" ) )
        action_pull = menu.addAction ( icon_pull, 'Pull version %s' % item.text (0) )
        action_pull.triggered.connect ( self.pullVersion )
        
        """import version"""
        icon_import = QtGui.QIcon ( os.path.join ( CC_PATH, "import.png" ) )
        action_import = menu.addAction ( icon_import, 'Import version %s' % item.text (0) )
        action_import.triggered.connect ( self.importVersion )
        
        menu.exec_( QtGui.QCursor.pos () )
        