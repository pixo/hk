#!/usr/autodesk/maya2013-x64/bin/mayapy
       
import maya.standalone
maya.standalone.initialize ( name = 'python' )

import sys, os
import maya.cmds as cmds
import maya.mel as mel
import glob
import maya.standalone

cmds.file ( "/homeworks/users/pixo/projects/testing/shot/op001/lay/a/testing_shot_op001_lay_a.v001.base1/testing_shot_op001_lay_a.ma", o=True )
