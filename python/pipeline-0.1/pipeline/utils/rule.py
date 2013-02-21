'''
Created on Feb 17, 2013

@author: pixo
'''

def getTextureTypes () :
    
    res = { "diff": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle" ),
            "diffback": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle" ),
            "roug": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle" ),
            "rougback": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle" ),
            "spec": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle" ),
            "specback": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle" ), 
            "emis": ( "RGB", "8-bit", "rgb(0,0,0)", True, "triangle" ),
            "emisback" : ( "RGB", "8-bit", "rgb(0,0,0)", True, "triangle" ),
            "mask": ( "R", "8-bit", "rgb(0,0,0)", "Triangle" ),
            "maskback": ( "R", "8-bit", "rgb(0,0,0)", True, "triangle" ),
            "albe": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle" ),
            "albeback": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle" ),
            "ssss": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle" ),
            "ssssback": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle" ),
            "bump": ( "R", "8-bit 16-bit","rgb(127,127,127)",True, "bspline" ),
            "bumpback": ( "R", "8-bit 16-bit", "rgb(127,127,127)", True, "bspline" ),
            "norm": ( "RGB", "8-bit", "rgb(127,127,255)", True, "triangle" ),
            "normback": ("RGB","8-bit","rgb(127,127,255)",True, "triangle" ),
            "disp": ( "R", "16-bit 32-bit", False, True, "bspline" ) }
    
    return res

def getAssetTypes ():
    #TODO:Asset list
    res = list ( ( "model" ) )
    
    return res

def getTaskTypes ():
    #TODO:Task list
    res = list ( ( "layout","lighting","render","compositing","compout" ) )
    
    return res