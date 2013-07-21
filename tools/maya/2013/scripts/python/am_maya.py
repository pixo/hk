'''
Created on Feb 9, 2013openFile

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

def assetExport ( source = "", gpj = True, obj = False, abc = True, first = 1, last = 1 ):
    cmd = """hk-asset-export -i %s -gpj %d -obj %d -abc %d -f %d -l %d """ % ( source, int ( gpj ), int(obj), int(abc), first, last )   
    return commands.getoutput( cmd )

def createAssetStructure ( doc_id, msgbar ):
    
    if not cmds.objExists ( "%s:root" % doc_id ) :
        
        if not cmds.objExists ( doc_id ) :
                        
            """Create structure"""
            root = cmds.createNode ( "transform", n = doc_id )
            trs_master = cmds.createNode ( "transform", n = "master_trs" )
            trs_shot = cmds.createNode ( "transform", n = "shot_trs" )
            trs_aux = cmds.createNode ( "transform", n = "aux_trs" )
            
            """Create the groups"""
            faceprim_grp = cmds.createNode ( "transform", n = "faceprim_grp" )
            bodyprim_grp = cmds.createNode ( "transform", n = "bodyprim_grp" )
            facemisc_grp = cmds.createNode ( "transform", n = "facemisc_grp" )
            bodymisc_grp = cmds.createNode ( "transform", n = "bodymisc_grp" )
            hair_grp = cmds.createNode ( "transform", n = "hair_grp" )
            cloth_grp = cmds.createNode ( "transform", n = "cloth_grp" )
            render_grp = cmds.createNode ( "transform", n = "render_grp" )
            model_grp = cmds.createNode ( "transform", n = "model_grp" )
            rig_grp = cmds.createNode ( "transform", n = "rig_grp" )
            look_grp = cmds.createNode ( "transform", n = "look_grp" )
            
            """Set attribute so the modeling can't move without any rig"""
            cmds.setAttr( "%s.inheritsTransform" % model_grp, 0 )
            
            """Guerilla attr"""
            cmds.addAttr ( rig_grp, shortName = "GuerillaExport", attributeType = "bool", dv = 0, min = 0, max = 1 )
            cmds.addAttr ( look_grp, shortName = "GuerillaExport", attributeType = "bool", dv = 0, min = 0, max = 1 )
            
            """Parent the groups"""
            cmds.parent ( faceprim_grp, render_grp )
            cmds.parent ( bodyprim_grp, render_grp )
            cmds.parent ( facemisc_grp, render_grp )
            cmds.parent ( bodymisc_grp, render_grp )
            cmds.parent ( hair_grp, render_grp )
            cmds.parent ( cloth_grp, render_grp )
            cmds.parent ( render_grp, model_grp )
            cmds.parent ( model_grp, rig_grp , look_grp, trs_aux )
            cmds.parent ( trs_aux, trs_shot )
            cmds.parent ( trs_shot, trs_master )
            cmds.parent ( trs_master, root )
            
            """create attributes"""
            #Lock and hide root transform attr
            for attr in ( "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy","sz" ):
                cmds.setAttr ( "%s.%s" % ( root, attr ), lock = True, keyable = False, channelBox = False )
            
            #asset attr
            cmds.addAttr ( root, shortName = "asset", dataType = "string" )
            cmds.setAttr ( "%s.%s" % ( root, "asset" ), doc_id, typ = "string" )
            cmds.setAttr ( "%s.%s" % ( root, "asset" ), lock = True )
            
            #texture version attr
            cmds.addAttr ( root, shortName = "texturever", attributeType = "short", dv = 1, min = 1 )
            cmds.setAttr ( "%s.%s" % ( root, "texturever" ), lock = True )
  
            #variation attr
            cmds.addAttr ( root, shortName = "variation", attributeType = "short", dv = 1, min = 1 )
                        
            #guerilla tag
            cmds.addAttr ( root, shortName = "GuerillaTags", dataType = "string" )
            cmds.setAttr ( "%s.%s" % ( root, "GuerillaTags" ), doc_id, typ = "string" )
            
            #guerilla attrs
            guerillaAttrToExport = "asset,texturever,variation"
            cmds.addAttr ( root, shortName = "GuerillaAttrToExport", dataType = "string" )
            cmds.setAttr ( "%s.%s" % ( root, "GuerillaAttrToExport" ), guerillaAttrToExport, typ = "string" )
            
            #select root structure
            cmds.select ( root, r = True)
            
        else:
            msgbar ( "%s exists" % doc_id )
            
    else:
        msgbar ( "%s exists" % doc_id )

def createCameraStructure ( doc_id, msgbar ):
    
    if not cmds.objExists ( "%s:root" % doc_id ) :
        
        if not cmds.objExists ( doc_id ) :
                        
            """Create structure"""
            root = cmds.createNode ( "transform", n = doc_id )
            trs_master = cmds.createNode ( "transform", n = "master_trs" )
            trs_shot = cmds.createNode ( "transform", n = "shot_trs" )
            trs_aux = cmds.createNode ( "transform", n = "aux_trs" )
            
            """Create the groups"""
            rig_grp = cmds.createNode ( "transform", n = "rig_grp" )
            render_grp = cmds.createNode ( "transform", n = "render_grp" )
            camera_grp = cmds.createNode ( "transform", n = "camera_grp" )
            cmds.setAttr ( "%s.inheritsTransform" % camera_grp, 0 )
            
            """Guerilla attr"""
            cmds.addAttr ( rig_grp, shortName = "GuerillaExport", attributeType = "bool", dv = 0, min = 0, max = 1 )
            
            """Create cameras"""
            anim_cam = cmds.camera ( n = "anim_cam" )[0]
            offset_cam = cmds.camera ( n = "offset_cam" )[0]
            shake_cam = cmds.camera ( n = "shake_cam" )[0]
            render_cam = cmds.camera ( n = "render_cam" )[0]
            
            for cam in ( anim_cam, offset_cam, shake_cam ) :
                cmds.setAttr ( "%s.visibility" % cam, 0 )

            """Parent camera"""                                    
            cmds.parent ( shake_cam, offset_cam )
            cmds.parent ( offset_cam, anim_cam )
            cmds.parent ( anim_cam, rig_grp )
            cmds.parent ( render_cam, camera_grp )
            constraint = cmds.parentConstraint ( shake_cam, camera_grp )
            cmds.addAttr ( constraint, shortName = "GuerillaExport", attributeType = "bool", dv = 0, min = 0, max = 1 )
                        
            """Parent the groups"""
            cmds.parent ( camera_grp, render_grp )
            cmds.parent ( render_grp, trs_aux )
            cmds.parent ( rig_grp, trs_aux )
            cmds.parent ( trs_aux, trs_shot )
            cmds.parent ( trs_shot, trs_master )
            cmds.parent ( trs_master, root )
            
            """create attribute"""
            #transform attr
            for attr in ( "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy","sz" ):
                cmds.setAttr ( "%s.%s" % ( root, attr ), lock = True, keyable = False, channelBox = False )
                        
            #asset attr
            cmds.addAttr ( root, shortName = "asset", dataType = "string" )
            cmds.setAttr ( "%s.%s" % ( root, "asset" ), doc_id, typ = "string" )
            cmds.setAttr ( "%s.%s" % ( root, "asset" ), lock = True )
                          
            #select root structure
            cmds.select ( root, r = True)
            
        else:
            msgbar ( "%s exists" % doc_id )
            
    else:
        msgbar ( "%s exists" % doc_id )

def createStructure ( doc_id, msgbar ):
    
    if doc_id.split( "_" )[1] == "cam":
        createCameraStructure ( doc_id, msgbar )
    else:
        createAssetStructure ( doc_id, msgbar )
    
def doScreenshot ( filename = "" ) :
    image = api.MImage ()
    view = apiUI.M3dView.active3dView ()
    view.readColorBuffer ( image, True )
    image.resize ( 640, 480, True )
    image.writeToFile ( filename, 'jpg' )
    
    return filename
    

def saveFile ( filename = "", exportsel = False, msgbar = None, doc_id = "" ) :
    
    if exportsel :
        
        assemblies = cmds.ls ( sl = True, l = True )
        
        if len ( assemblies) == 0:
            assemblies = cmds.ls ( assemblies= True )
            
        else :
            assemblies = [ assemblies[0].split("|")[1] ]
            
        asset = ""
        
        for obj in assemblies :
            assetUd = cmds.listAttr ( obj, ud = True )
             
            if not ( assetUd == None ) and "asset" in assetUd :
                assetId = cmds.getAttr ( "%s.asset" % obj ) 
                
                if assetId == doc_id :
                    asset = obj 
                    break
             
        if obj == "" :
            msgbar ( "There's no asset %s " % doc_id )
            return False
        
        cmds.rename ( asset, "root" )
        cmds.select ( "root", r =True )
            
    extension = { ".ma":"mayaAscii", ".mb":"mayaBinary", ".obj":"OBJ" }
    filename, ext = os.path.splitext ( filename )[-1]
    
    if exportsel :
        ext = ".mb"
    else:
        ext = ".ma"
         
    filename = filename + ext
    cmds.file ( filename, force=True, options="v=0;", type = extension[ext],
                pr = True, es = exportsel, ea = ( not exportsel ) )
    
    if exportsel :
        cmds.rename ( "root", asset )
        
    return os.path.exists ( filename )


def saveSelected ( filename = "", msgbar = None ) :
    saveFile ( filename, True, msgbar )


def openFile ( filename ):
    extension = { ".ma":"mayaAscii", ".mb":"mayaBinary", ".obj":"OBJ" }
    ext = os.path.splitext ( filename )[-1]
    cmds.file ( filename, f=True, options="v=0;", type = extension[ext], o = True )
    

def importFile ( filename ):
    extension = { ".ma":"mayaAscii", ".mb":"mayaBinary", ".obj":"OBJ" }
    ext = os.path.splitext ( filename )[-1]
    cmds.file ( filename, i=True, options="v=0;", type = extension[ext],
                ra=True, mergeNamespacesOnClash=True, namespace=":", pr=True,
                loadReferenceDepth="all" )

    
def referenceFile ( filename = "", namespace = "" ):
    extension = { ".ma":"mayaAscii", ".mb":"mayaBinary" }
    ext = os.path.splitext ( filename )[-1]
    cmds.file ( filename, r = True, type = extension[ext], gl = True, loadReferenceDepth = "all",
                mergeNamespacesOnClash = False, namespace = namespace, options = "v=0;" )
        
        
def instanceAsset ( namespace = "" ):
    """Find new namespace"""
    ns = namespace
    name ="%s:root" % ns
    
    i = 1
    while cmds.objExists ( name ) :
        ns = "%s%d" % ( namespace, i ) 
        name = "%s:root" % ns
        i += 1 
    
    """Make instance"""
    cmds.namespace ( add = ns )
    root = cmds.instance ( "%s:root" % namespace , name = name )[0]
    
    """Get model_grp path"""
    model_grp = "%s:root|%s:master_trs|%s:shot_trs|%s:aux_trs|%s:model_grp" % ( ns, namespace, namespace, namespace, namespace )
    
    """Lock attributes"""
    cmds.setAttr ( "%s.%s" % ( root, "asset" ), lock = True )
    cmds.setAttr ( "%s.%s" % ( root, "texture_version" ), lock = True )
    cmds.setAttr( "%s.inheritsTransform" % model_grp, 0 )
    
def referenceOrInstance ( file, doc_id ) :
    asset = "%s:root" % doc_id
    if  cmds.objExists ( asset ) :
        instanceAsset ( doc_id )                
    else:
        referenceFile ( file, doc_id )

def pushMaya ( db = None, doc_id = "", description = "", item = None,
                screenshot = "", msgbar = False, progressbar = False,
                selection = False, rename = True, extension = ".mb" ) :

    if not ( screenshot == "" ) :
      fname = os.path.join ( "/tmp", "%s%s" % ( core.hashTime (), extension ) )
      
      if saveFile ( fname, selection, msgbar, doc_id) :
          destination = core.push ( db, doc_id, fname, description, progressbar,
                        msgbar, rename )
          core.transfer ( screenshot, destination, doc_id )
          source = os.path.join ( destination, doc_id + extension )
          print "pushMaya():", source
          assetExport ( source )
          
          if msgbar :
              msgbar ( "Done" )
          
          return destination
      
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

def checkScene ( doc_id ):
    """We shouldn't have any node named 'root', Check if it's the case"""
    if cmds.objExists ( "root" ) :
    
        self.labelStatus.setText ( "You shouldn't have any named 'root' node in your scene" )
        return False       
    
    return True

def normalizeScene ( doc_id ) :
    """"""
    if cmds.objExists ( "root" ):
        cmds.rename ( "root", doc_id )
      
class UiPushMaya(apps.UiPush3dPack):
     
     
    launcher = "maya"
    screenshot = ""
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
              "render" : pushFile,
              "rendercam" : pushSelected,
              "projcam" : pushSelected
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
              'rca':'rendercam',
              'pca':'projcam',
             }
  

    def pushClicked ( self ) :
        doc_id = self.doc_id
        
        if checkScene ( doc_id ):
            """Set variables"""
            db = self.db
            description = self.plainTextEdit_comments.toPlainText ()
            item = self.item
            taskType = self.varpush [ doc_id.split ( "_" ) [3] ]
            screenshot = self.screenshot
            msgbar = self.labelStatus.setText
            progressbar = self.progressBar
        
            """Push asset"""
            pushed = self.fnPush[ taskType ] ( db, doc_id, description, item, screenshot, msgbar, progressbar )
  
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
        
        if checkScene ( doc_id ):
             
            self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str ( ver ) ) )
         
            path = core.getAssetPath ( doc_id, ver )
            files = glob.glob(os.path.join(path,"*.ma"))
            files.extend(glob.glob(os.path.join(path,"*.mb")))
             
            importFile ( files [0] )
            
            normalizeScene ( doc_id )
            
            self.statusbar.showMessage ( "%s pulled" % files[0] )

    def referenceVersion ( self ) :

        item = self.treeWidget_a.currentItem ()
        doc_id = item.parent().hkid
        ver = int ( item.text ( 0 ) )
        self.statusbar.showMessage ( "Reference %s %s" % ( doc_id, str ( ver ) ) )
     
        path = core.getAssetPath ( doc_id, ver )
        files = glob.glob(os.path.join(path,"*.ma"))
        files.extend(glob.glob(os.path.join(path,"*.mb")))
         
        referenceOrInstance ( files [0], doc_id )
        self.statusbar.showMessage("%s referenced" % files[0] )

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
        
        
    def createStructure ( self ) :
        
      item = self.treeWidget_a.currentItem ()
      doc_id = item.hkid
      createStructure ( doc_id, self.statusbar.showMessage )
        
        
    def openFile ( self, fname ) :
        
        openFile ( fname )


    def saveFile(self,fname):
        
        saveFile ( fname )
        
        
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
            icon_structure = QtGui.QIcon ( os.path.join ( CC_PATH, "structure.png" ) )
            actionStructure = menu.addAction ( icon_structure, 'Create asset structure' )
            actionStructure.triggered.connect ( self.createStructure )

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
        
        """reference version"""
        icon_import = QtGui.QIcon ( os.path.join ( CC_PATH, "reference.png" ) )
        action_import = menu.addAction ( icon_import, 'reference version %s' % item.text (0) )
        action_import.triggered.connect ( self.referenceVersion )
        
        menu.exec_( QtGui.QCursor.pos () )
        