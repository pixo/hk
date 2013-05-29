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

#TODO:remove GuerillaNode when importing an asset

def assetExport ( source = "", obj=True, abc=True, gpj = True, first= 1, last = 1 ):
    cmd = """hk-asset-export -i %s -obj %d -abc %d -gpj %d -f %d -l %d """ % ( source, int(obj), int(abc), int( gpj ), first, last )   
    return commands.getoutput( cmd )
    

def pushMaya ( db = None, doc_id = "", description = "", item = None,
               screenshot = "", msgbar = False, progressbar = False,
               selection = False, rename = True, extension = ".mb" ) :
    
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
    screenshot = doScreenshot ( os.path.join ( "/tmp", "%s.jpg" % core.hashTime() ) )
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
         
    def pushClicked ( self ) :
        db = self.db
        doc_id = self.doc_id
        description = self.plainTextEdit_comments.toPlainText ()
        item = self.item
        taskType = self.item.parent().text(0)
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
         
        importFile(files[0])
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


    def contextMenuFork ( self, item ) :
        item = self.treeWidget_a.currentItem ()       
        menu = QtGui.QMenu ()   
        icon_new = QtGui.QIcon ( os.path.join ( CC_PATH, "add.png" ) )
        icon_push = QtGui.QIcon ( os.path.join ( CC_PATH, "push.png" ) )
        icon_open = QtGui.QIcon ( os.path.join ( CC_PATH, "open.png" ) )
        icon_saveas = QtGui.QIcon ( os.path.join ( CC_PATH, "save.png" ) )
        
        doc_id = item.hkid
        path = core.getWorkspaceFromId ( doc_id )
        
        if os.path.exists ( path ) :
            actionPush = menu.addAction ( icon_push, 'Push a new %s %s %s version' % 
                                      ( item.parent().parent().text(0),
                                        item.parent().text(0), item.text(0)) )
            actionPush.triggered.connect ( self.pushVersion )
            actionOpen = menu.addAction ( icon_open, 'Open from Workspace' )
            actionOpen.triggered.connect ( self.openFileDialog )
            actionSaveas = menu.addAction ( icon_saveas, 'Save to Workspace' )
            actionSaveas.triggered.connect ( self.saveFileDialog )
            
        else:
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
        