'''
Created on Feb 17, 2013

@author: pixo
'''

def getTextureTypes () :
    return {"diff" : ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diffback" : ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "droug" : ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "drougback": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "spec" : ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "specback" : ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1"), 
            "sroug" : ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "srougback" : ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "emis" : ( "RGB", "8-bit", "rgb(0,0,0)", True, "triangle", "1"),
            "emisback" : ( "RGB", "8-bit", "rgb(0,0,0)", True, "triangle", "1"),
            "mask" : ( "R", "8-bit", "rgb(0,0,0)", "Triangle" ),
            "maskback" : ( "R", "8-bit", "rgb(0,0,0)", True, "triangle", "1"),
            "albe" : ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "sRGB"),
            "albeback" : ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "sRGB"),
            "ssss" : ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "ssssback" : ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "bump" : ( "R", "8-bit 16-bit","rgb(127,127,127)",True, "bspline", "1"),
            "bumpback" : ( "R", "8-bit 16-bit", "rgb(127,127,127)", True, "bspline", "1"),
            "norm" : ( "RGB", "8-bit", "rgb(127,127,255)", True, "triangle", "1"),
            "normback" : ("RGB","8-bit","rgb(127,127,255)",True, "triangle", "1"),
            "disp" : ( "R", "16-bit 32-bit", False, True, "bspline", "1")}

def getAssetTypes ():
    return {'character':'chr',
            'environment':'env',
            'material':'mtl',
            'prop':'prp',
            'sequence':'seq',
            'shot':'shot',
            'vehicle':'vcl',
            'effect':'vfx'}
        
def getTaskTypes ():                    
    return {'animation':'ani',
            'bashcomp':'bcmp',
            'camera':'cam',
            'composite':'rcmp',
            'mattepaint':'dmp',
            'dynamic':'dyn',
            'fluid':'fld',
            'layout':'lay',
            'lighting':'lit',
            'model':'mod',
            'override' : 'ovr',
            'particle':'pcl',
            'render':'ren',
            'rig' : 'rig',
            'retopo':'rtp',
            'rotoscopy':'rot',
            'sculpt':'sct',
            'shader':'shd',
            'surface':'sur',
            'texture':'tex',
            'effect':'vfx'}
