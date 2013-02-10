'''
Created on Feb 9, 2013

@author: pixo
'''

import maya.cmds as cmds
import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI
import os

def screenshot ( filename = "" ) :
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
    base, ext = os.path.splitext ( filename )
    cmds.file ( filename, force=True, options="v=0;",
                type = extension[ext], pr = True, es = exportsel, ea = (not exportsel))
    
    return os.path.exists ( filename )

def openFile(filename):
    extension = { ".ma":"mayaAscii", ".mb":"mayaBinary", ".obj":"OBJ" }
    base, ext = os.path.splitext ( filename )
# # file -import -type "mayaBinary" -ra true -mergeNamespacesOnClash true -namespace ":" -options "v=0;"  -pr -loadReferenceDepth "all" "/home/pixo/mabite.mb";
#     cmds.file ( filename, i=True, options="v=0;", type = extension[ext],
#                 ra=True, mergeNamespacesOnClash=True, namespace=":", pr=True,
#                 loadReferenceDepth="all" )

 
#     file -f -options "v=0;"  -typ "mayaBinary" -o "/home/pixo/mabite.mb";
    cmds.file ( filename, f=True, options="v=0;", type = extension[ext], o = True )


