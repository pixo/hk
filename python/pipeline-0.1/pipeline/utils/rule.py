'''
Created on Feb 17, 2013

@author: pixo
'''

def getTextureTypes () :
    return {
            "bump" : ( "R", "8-bit 16-bit","rgb(127,127,127)", True, "bspline", "1"),
            "bumpbk" : ( "R", "8-bit 16-bit", "rgb(127,127,127)", True, "bspline", "1"),
            "cavt" : ( "R", "8-bit 16-bit","rgb(127,127,127)", True, "bspline", "1"),
            "cavtbk" : ( "R", "8-bit 16-bit","rgb(127,127,127)", True, "bspline", "1"),
            "disp" : ( "R", "8-bit 16-bit 32-bit", False, True, "bspline", "1"),
            "diff" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diffbk" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "drgh" : ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "drghbk": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "dirt" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "dirtco" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "emis" : ( "R", "8-bit 16-bit", "rgb(0,0,0)", True, "triangle", "1"),
            "emisco" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "emisbk" : ( "R", "8-bit 16-bit", "rgb(0,0,0)", True, "triangle", "1"),
            "emiscobk" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "mask" : ( "R", "8-bit", "rgb(0,0,0)", "Triangle", "1" ),
            "maskbk" : ( "R", "8-bit", "rgb(0,0,0)", True, "triangle", "1" ),
            "mtal" : ( "R", "8-bit 16-bit", "rgb(0,0,0)", True, "triangle", "1" ),
            "mtalco" : ( "RGB", "8-bit 16-bit", "rgb(0,0,0)", True, "triangle", "sRGB" ),
            "norm" : ( "RGB", "8-bit", "rgb(127,127,255)", True, "triangle", "1"),
            "normbk" : ("RGB","8-bit","rgb(127,127,255)",True, "triangle", "1"),
            "spec" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "specbk" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1"), 
            "srgh" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "srghbk" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "sssc" : ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "sRGB"),
            "ssscbk" : ( "RGB", "8-bit", "rgb(255,255,255)", True, "triangle", "sRGB"),
            "ssss" : ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1"),
            "ssssbk" : ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1")
            }

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
