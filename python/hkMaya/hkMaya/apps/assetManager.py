'''
Created on Feb 9, 2013

@author: pixo
'''

import sys, os
import pipeline.apps as apps
import pipeline.utils as utils
import pipeline.core as core
import hkMaya.cmds as hkcmds
import glob


CC_PATH = utils.getCCPath()
PROJECT = utils.getProjectName()

def pushMaya ( db = None, doc_id = "", description = "",
               item = None, screenshot = "", msgbar = False,
               progressbar = False ) :
     
    selection = False
    extension = ".mb"
    rename = True
 
    filename = os.path.join( "/tmp", "%s%s" % ( core.hashTime (), extension ) ) 
     
    if hkcmds.saveFile ( filename, selection, msgbar ) :
        repo = core.push ( db, doc_id, filename, description, progressbar,
                           msgbar, rename )
         
        core.transfer ( screenshot, repo, doc_id )
        msgbar ( "Done" )
        
def pullMaya (db = None, doc_id = "", ver = "latest" ):
    path = os.path.expandvars(core.getAssetPath(db, doc_id, ver))
    files = glob.glob(os.path.join(path,"*.ma"))
    files.extend(glob.glob(os.path.join(path,"*.mb")))
    hkcmds.openFile(files[0])
 
class UiPushMaya(apps.UiPush3dPack):
     
     
    launcher = "maya"
    screenshot = hkcmds.screenshot ( os.path.join ( "/tmp", "%s.jpg" % core.hashTime() ) )
         
    def pushClicked ( self ) :
         
        db = self.db
        doc_id = self.doc_id
        description = self.plainTextEdit_comments.toPlainText ()
        item = self.item
        screenshot = self.screenshot
        msgbar = self.labelStatus.setText
        progressbar = self.progressBar
        
        pushMaya ( db, doc_id, description, item,
                   screenshot, msgbar, progressbar )
        
        self.close()
     
    def screenshotClicked ( self ) :
        self.screenshot = hkcmds.screenshot ( os.path.join ( "/tmp", "%s.jpg" % core.hashTime() ) )
        self.labelImage.setPixmap ( self.screenshot )
         
 
class UiMayaAM(apps.UiAssetManager):
     
     
    launcher = "maya"
         
    def pushVersion ( self ) :
        item = self.treeWidget_a.currentItem()
        task = item.parent().text(0)
        doc_id = item.hkid
        self.pushVersionWidget = UiPushMaya ( None, self.db, doc_id, item )
        self.pushVersionWidget.show ()
      
#     def pullVersion ( self ) :
#         print "pullVersion"
# #         self.progressBar.setHidden ( False )
#         item = self.treeWidget_a.currentItem ()
#         doc_id = item.parent().hkid
#         ver = int ( item.text ( 0 ) )
#         self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str ( ver ) ) )
#     
#         path = os.path.expandvars(core.getAssetPath(self.db, doc_id, ver))
#         files = glob.glob(os.path.join(path,"*.ma"))
#         files.extend(glob.glob(os.path.join(path,"*.mb")))
#         
#         hkcmds.openFile(files[0])
#         self.statusbar.showMessage("%s pulled" % files[0] )
        
        
    def pullVersion ( self ) :
        self.progressBar.setHidden ( False )
        item = self.treeWidget_a.currentItem ()
        doc_id = item.parent().hkid
        ver = int ( item.text ( 0 ) )
        self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str(ver) ) )
        #TODO:REWRITE PULL with glob
        pull = core.pull (self.db, doc_id = doc_id, ver = ver , extension = ".mb",
                                  progressbar = self.progressBar,
                                  msgbar = self.statusbar.showMessage)
        if pull :
            hkcmds.openFile(pull[0])
            self.statusbar.showMessage("%s %s pulled" % ( doc_id, str(ver) ))
        
        self.progressBar.setHidden ( True )
        
#         self.progressBar.setHidden ( True )


# # app = QtGui.QApplication ( sys.argv )    
# # main = UiMayaAM()
# # main.show()
# # app.exec_()
# # sys.exit()
