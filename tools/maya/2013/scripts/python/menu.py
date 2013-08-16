import os
import maya.cmds as cmds
import maya.mel
import maya.utils as mu
import am_maya
import checkDeps_maya

ASSET_MANAGER = None
CHECK_DEPS = None

def showAssetManager ( stat ):
	global ASSET_MANAGER
	ASSET_MANAGER = am_maya.UiMayaAM ()
 	ASSET_MANAGER.show ()

def showDependenciesManager ( stat ):
	global CHECK_DEPS
	fpath = cmds.file ( q = True, sn = True )
	cmds.file ( s = True )
	
	if os.path.exists ( fpath ):
		CHECK_DEPS = checkDeps_maya.UiCheckDependenciesMaya ( fpath )
 		CHECK_DEPS.show ()

def homeworksMenu ():
    gMainWindow = maya.mel.eval ( '$temp1=$gMainWindow' )
    menuCtrl = cmds.menu ( parent = gMainWindow, tearOff = True, label = 'Homeworks' )
    cmds.menuItem ( parent = menuCtrl, label='Asset Manager', c = showAssetManager )
    cmds.menuItem ( parent = menuCtrl, label='Check Dependencies', c = showDependenciesManager )
 	    
mu.executeDeferred ( 'homeworksMenu()' )