#!/usr/autodesk/maya2013-x64/bin/mayapy
       
import maya.standalone
maya.standalone.initialize ( name = 'python' )
import sys, os
import maya.cmds as cmds
import maya.mel as mel
import glob
        
def objExporter ( destination = "", start = 1, end = 1 ):    
    start = int ( start )
    end = int ( end )
    
    if start != end :
        base, ext = os.path.splitext ( destination )
        destination = base + ".%04d.obj"
    
    for frame in range ( start, (end+1) ):
        dst = ( destination % frame ) if start != end else destination
        cmds.currentTime ( frame )
        cmds.file ( dst, force = True, options = "groups=1;ptgroups=1;materials=0;smoothing=1;normals=1",
                    type = "OBJexport", pr = True, ea = True )

def abcExporter ( destination = "", start = 1, end = 1, renderOnly = True, stripNS = True ):
    
    strip = "-stripNamespaces"
    ro = "-ro"

    """Check if namespace is needed"""
    if not stripNS :
        strip = ""
    
    """Check if renderonly is needed"""    
    if not renderOnly :
        ro = ""
     
    attrs = "asset,texture_version,variation"
    attrs = "," + attrs
    attrs = attrs.replace( ",", " -attr ")
                     
    mel.eval ( 'AbcExport -j "-frameRange %s %s %s %s %s %s -file %s";' % ( start, end, attrs, ro, "-uvWrite", strip, destination ) )

def cli ( input = None, obj = True, abc = True, start = 1, end = 1, ro = 1, strip = 1 ) :

    """Load the input file"""
    if not os.path.isabs ( input ):
        input = os.path.abspath ( input )
    
    """check if file"""    
    if not os.path.isfile ( input ):
        return 1
    
    """check if correct ext"""
    base, ext = os.path.splitext ( input )
    if not (ext in ( ".mb", ".ma", ".obj" )):
        return 1
    
    """open the file"""
    cmds.file ( input, o = True )


    """Get maya plugins path"""
    mayaver = os.getenv ( "HK_MAYA_VER" )
    mayaloc = "/usr/autodesk/maya%s-x64/bin/plug-ins" % mayaver  
    
    """Load maya plugins"""
    cmds.loadPlugin ( os.path.join ( mayaloc, 'objExport.so' ) )
    cmds.loadPlugin ( os.path.join ( mayaloc, 'AbcExport.so' ) )
    
    """Get the input directory to change permission"""
    dirname = os.path.dirname ( input )
    os.chmod ( input, 0775 )
    os.chmod ( dirname, 0775 )
    
    """Exporting to obj abc """
    if obj :
        dst = base + ".obj"
        objExporter ( dst, start, end )

    if abc :
        dst = base + ".abc"
        abcExporter ( dst, start, end, renderOnly = 1, stripNS = 0 )
    
    files = glob.glob ( "%s/*" % dirname )
    files.append ( dirname )
    for file in files : os.chmod ( file, 0555 )
    
input = "/homeworks/projects/fan/shot/sit001/lay/a/001/fan_shot_sit001_lay_a.mb"
cli ( input = input, obj = False, abc = True, start = 1, end = 1, ro = 1, strip = strip )