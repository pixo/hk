#!/usr/autodesk/maya2013-x64/bin/mayapy
       
import maya.standalone
maya.standalone.initialize ( name = 'python' )
import sys, os
import maya.cmds as cmds
import maya.mel as mel
import glob
import maya.standalone

def objExporter ( destination = "", start = 1, end = 1 ):    
        
    if start != end :
        base, ext = os.path.splitext ( destination )
        destination = base + ".%04d.obj"
    
    for frame in range ( start, ( end + 1 ) ):
        dst = ( destination % frame ) if start != end else destination
        cmds.currentTime ( frame )
        cmds.file ( dst, force = True, options = "groups=1;ptgroups=1;materials=0;smoothing=1;normals=1",
                    type = "OBJexport", pr = True, ea = True )

def abcExporter ( destination = "", start = "1", end = "1" ):
    attrs = "-attr asset -attr texture_version -attr variation"
    cmd = 'AbcExport -j "-frameRange %s %s %s -ro -uvWrite -file %s";' % ( str( start ), str ( end ), attrs,  destination )
    mel.eval ( cmd )

def gpjExporter ( destination = "", start = 1, end = 1 ):    
    cmds.GuerillaExport ( m = 1, a = 1, framesToExport = 3, customRange = ( start, end ), pf = destination )

def cli ( input = None, start = 1, end = 1, gpj = True, abc = True, obj = True ) :
    start = int ( start )
    end = int ( end )
    gpj = bool ( int ( gpj ) )
    abc = bool ( int ( abc ) )
    obj = bool ( int ( obj ) )
    
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

    """get maya plugins path"""
    mayaver = os.getenv ( "HK_MAYA_VER" )
    mayaloc = "/usr/autodesk/maya%s-x64/bin/plug-ins" % mayaver  
    
    """get guerilla plugins path"""
    guerillaver = os.getenv ( "HK_GUERILLA_VER" )
    guerillaloc = "/usr/local/soft/guerilla/%s/guerilla_for_maya/plug-ins" % guerillaver
    
    """get the input directory to change permission"""
    dirname = os.path.dirname ( input )
    os.chmod ( input, 0775 )
    os.chmod ( dirname, 0775 )
    
    """exporting obj abc gprj """
    if gpj:
        cmds.loadPlugin ( os.path.join ( guerillaloc, 'guerilla2013.so' ) )
        dst = base + ".gproject"
        gpjExporter ( destination = dst, start = start, end = end )
    
    if abc :
        cmds.loadPlugin ( os.path.join ( mayaloc, 'AbcExport.so' ) )
        dst = base + ".abc"
        abcExporter ( destination = dst, start = start, end = end )
        
    if obj :
        cmds.loadPlugin ( os.path.join ( mayaloc, 'objExport.so' ) )
        dst = base + ".obj"
        objExporter ( destination = dst, start = start, end = end )
    
    """file access setup"""
    files = glob.glob ( "%s/*" % dirname )
    files.append ( dirname )
    
    for file in files : os.chmod ( file, 0555 )
    
# faune
# input = "/homeworks/projects/fan/chr/faune/mod/a/002/fan_chr_faune_mod_a.mb"
# cli ( input = input, gpj = True, obj = False, abc = False, start = 1, end = 1 )

# lowwal
# input = "/homeworks/projects/fan/env/lowwall/mod/a/001/fan_env_lowwall_mod_a.mb"
# cli ( input = input, gpj = True, obj = False, abc = False, start = 1, end = 1 )

# main scene
# input = "/homeworks/projects/fan/cam/sit001/rca/a/003/fan_cam_sit001_rca_a.mb"
# cli ( input = input, gpj = True, obj = False, abc = False, start = 1, end = 1 )
   
# main scene
input = "/homeworks/projects/fan/shot/sit001/lay/a/001/fan_shot_sit001_lay_a.mb"
cli ( input = input, gpj = True, obj = False, abc = False, start = 1, end = 1 )