'''
Created on Feb 9, 2013

@author: pixo
'''

import pipeline.apps as apps
import pipeline.utils as utils
import pipeline.core as core
import hkMaya.cmds as hkcmds
import glob, os


CC_PATH = utils.getCCPath()
PROJECT = utils.getProjectName()

#TODO: Remove GuerillaNode when importing an asset

def pushMaya ( db = None, doc_id = "", description = "", item = None,
               screenshot = "", msgbar = False, progressbar = False,
               selection = False, rename = True, extension = ".mb") :
    filename = os.path.join ( "/tmp", "%s%s" % ( core.hashTime (), extension ) ) 
    if hkcmds.saveFile ( filename, selection, msgbar ) :
        repo = core.push ( db, doc_id, filename, description, progressbar,
                           msgbar, rename )
        core.transfer ( screenshot, repo, doc_id )
        core.assetExport ( os.path.join ( repo, doc_id + extension ), repo )
        msgbar ( "Done" )
        
        return True
    
    return False

def pullMaya (db = None, doc_id = "", ver = "latest" ):
    path = os.path.expandvars ( core.getAssetPath ( db, doc_id, ver ) )
    files = glob.glob ( os.path.join ( path, "*.ma" ) )
    files.extend ( glob.glob ( os.path.join ( path, "*.mb" ) ) )
    hkcmds.openFile ( files[0] )
        
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
    screenshot = hkcmds.doScreenshot ( os.path.join ( "/tmp", "%s.jpg" % core.hashTime() ) )
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
        self.screenshot = hkcmds.doScreenshot ( os.path.join ( "/tmp", "%s.jpg" % core.hashTime() ) )
        self.labelImage.setPixmap ( self.screenshot )
         
 
class UiMayaAM(apps.UiAssetManager):
     
    defaultfilter = "ma"
    launcher = "maya"
    defaultsuffix = "mb"
         
    def pushVersion ( self ) :
        item = self.treeWidget_a.currentItem ()
        doc_id = item.hkid
        self.pushVersionWidget = UiPushMaya ( None, self.db, doc_id, item )
        self.pushVersionWidget.show ()
      
    def importVersion ( self ) :
        item = self.treeWidget_a.currentItem ()
        doc_id = item.parent().hkid
        ver = int ( item.text ( 0 ) )
        self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str ( ver ) ) )
     
        path = os.path.expandvars(core.getAssetPath(self.db, doc_id, ver))
        files = glob.glob(os.path.join(path,"*.ma"))
        files.extend(glob.glob(os.path.join(path,"*.mb")))
         
        hkcmds.importFile(files[0])
        self.statusbar.showMessage("%s pulled" % files[0] )
        
        
    def pullVersion ( self ) :
        self.progressBar.setHidden ( False )
        item = self.treeWidget_a.currentItem ()
        doc_id = item.parent().hkid
        ver = int ( item.text ( 0 ) )
        self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str(ver) ) )
        
        pull = core.pull (self.db, doc_id = doc_id, ver = ver , extension = ".mb",
                                  progressbar = self.progressBar,
                                  msgbar = self.statusbar.showMessage)
        if pull :
            hkcmds.openFile ( pull [ 0 ] )
            self.statusbar.showMessage("%s %s pulled" % ( doc_id, str(ver) ))
         
        self.progressBar.setHidden ( True )
        
