'''
Created on Feb 9, 2013

@author: pixo
'''

import maya.cmds as cmds
import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI
import os

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
    