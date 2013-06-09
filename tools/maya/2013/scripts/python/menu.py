import maya.cmds as cmds
import maya.mel
import maya.utils as mu
import am_maya

ASSET_MANAGER = None

def showAssetManager ( stat ):
	global ASSET_MANAGER
	ASSET_MANAGER = am_maya.UiMayaAM ()
 	ASSET_MANAGER.show()

def homeworksMenu ():
    gMainWindow = maya.mel.eval ( '$temp1=$gMainWindow' )
    showMyMenuCtrl = cmds.menu ( parent=gMainWindow, tearOff = True, label = 'Homeworks' )
    cmds.menuItem ( parent=showMyMenuCtrl, label='asset manager', c = showAssetManager )
 	    
mu.executeDeferred ( 'homeworksMenu()' )