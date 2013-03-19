'''
Created on Feb 17, 2013

@author: pixo
'''

def getTextureTypes () :
    return {"diff": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diffback": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "droug": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "drougback": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "spec": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "specback": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1"), 
            "sroug": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "srougback": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "emis": ( "RGB", "8-bit", "rgb(0,0,0)", True, "triangle", "1"),
            "emisback" : ( "RGB", "8-bit", "rgb(0,0,0)", True, "triangle", "1"),
            "mask": ( "R", "8-bit", "rgb(0,0,0)", "Triangle" ),
            "maskback": ( "R", "8-bit", "rgb(0,0,0)", True, "triangle", "1"),
            "albe": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "sRGB"),
            "albeback": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "sRGB"),
            "ssss": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "ssssback": ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "bump": ( "R", "8-bit 16-bit","rgb(127,127,127)",True, "bspline", "1"),
            "bumpback": ( "R", "8-bit 16-bit", "rgb(127,127,127)", True, "bspline", "1"),
            "norm": ( "RGB", "8-bit", "rgb(127,127,255)", True, "triangle", "1"),
            "normback": ("RGB","8-bit","rgb(127,127,255)",True, "triangle", "1"),
            "disp": ( "R", "16-bit 32-bit", False, True, "bspline", "1")}

def getAssetTypes ():
    return {'chr': 'character',
            'env': 'environment',
            'mtl': 'material',
            'prp': 'prop',
            'seq': 'sequence',
            'shot': 'shot',
            'vcl': 'vehicle',
            'vfx': 'effect'}
        
def getTaskTypes ():                    
    return {'bsh': 'bashcomp',
            'cam': 'camera',
            'cmp': 'comp',
            'dmp': 'mattepaint',
            'lay': 'layout',
            'lit': 'lighting',
            'mod': 'modeling',
            'ren': 'render',
            'rig': 'rig',
            'rtp': 'retopo',
            'sct': 'sculpt',
            'sur': 'surfacing',
            'tex': 'texture'}
