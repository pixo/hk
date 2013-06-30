#!/usr/autodesk/maya2013-x64/bin/mayapy
       
import maya.standalone
maya.standalone.initialize ( name = 'python' )
import sys, os
import maya.cmds as cmds
import maya.mel as mel
import glob
import maya.standalone

def createCameraStructure ( doc_id ):
    
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
              
            #texture version attr
            cmds.addAttr ( root, shortName = "texture_version", attributeType = "short", dv = 1, min = 1 )
            cmds.setAttr ( "%s.%s" % ( root, "texture_version" ), lock = True )
            
            #variation attr
            cmds.addAttr ( root, shortName = "variation", attributeType = "short", dv = 1, min = 1 )
            
            #select root structure
            cmds.select ( root, r = True)
            
        else:
            print ( "%s exists" % doc_id )
            
    else:
        print ( "%s exists" % doc_id )
    
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
createCameraStructure ( "mickey" )