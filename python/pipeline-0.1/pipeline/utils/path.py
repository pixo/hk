'''
Created on Jan 6, 2013

@author: pixo
'''
import os

def getRootPath():
    return os.getenv("HK_ROOT")

def getProjectsPath():
    return os.getenv("HK_PROJECTS_PATH")