'''
Created on Feb 17, 2013

@author: pixo
'''
def checkVersionType ( vtype = "" ):
    types = ["review", "release"]
    if vtype in types :
        return False
    else :
        print ( "utils.checkVersionType: wrong version type" )
        return True

def getTextureTypes() :
    return {  # TODO: Create a dict instead of a list for the type parameters
            "bump" : ( "R", "8-bit 16-bit", "rgb(127,127,127)", True, "bspline", "1" ),
            "bumpbk" : ( "R", "8-bit 16-bit", "rgb(127,127,127)", True, "bspline", "1" ),
            "cavt" : ( "R", "8-bit 16-bit", "rgb(127,127,127)", True, "bspline", "1" ),
            "cavtbk" : ( "R", "8-bit 16-bit", "rgb(127,127,127)", True, "bspline", "1" ),
            "disp" : ( "R", "8-bit 16-bit 32-bit", False, True, "bspline", "1" ),
            "diff1" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diff1bk" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diff1col" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diff1colbk" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diff1rgh" : ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "diff1rghbk": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "diff2" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diff2bk" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diff2col" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diff2colbk" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "diff2rgh" : ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "diff2rghbk": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "veltcol" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "velt": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "veltbcol" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "veltb": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "veltedg": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "veltbrgh": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "dirt" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "dirtcol" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "emis" : ( "R", "8-bit 16-bit", "rgb(0,0,0)", True, "triangle", "1" ),
            "emiscol" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "emisbk" : ( "R", "8-bit 16-bit", "rgb(0,0,0)", True, "triangle", "1" ),
            "emiscolbk" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "glascol" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "glasrgh": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "glasabscol" : ( "RGB", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "sRGB" ),
            "glasabsscl": ( "R", "8-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "mask" : ( "R", "8-bit", "rgb(0,0,0)", "Triangle", "1" ),
            "maskbk" : ( "R", "8-bit", "rgb(0,0,0)", True, "triangle", "1" ),
            "mtal" : ( "R", "8-bit 16-bit", "rgb(0,0,0)", True, "triangle", "1" ),
            "mtalcol" : ( "RGB", "8-bit 16-bit", "rgb(0,0,0)", True, "triangle", "sRGB" ),
            "mtalrgh" : ( "R", "8-bit 16-bit", "rgb(0,0,0)", True, "triangle", "1" ),
            "mtalirid" : ( "R", "8-bit 16-bit", "rgb(0,0,0)", True, "triangle", "1" ),
            "norm" : ( "RGB", "8-bit", "rgb(127,127,255)", True, "triangle", "1" ),
            "normbk" : ( "RGB", "8-bit", "rgb(127,127,255)", True, "triangle", "1" ),
            "spec1" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec1bk" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec1col" : ( "RGB", "8-bit", "rgb(127,127,255)", True, "triangle", "1" ),
            "spec1rgh" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec1rghbk" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec2" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec2bk" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec2col" : ( "RGB", "8-bit", "rgb(127,127,255)", True, "triangle", "1" ),
            "spec2rgh" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec2rghbk" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec1irid" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec2irid" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec2thick" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "spec2bmp" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "sss" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "ssswidth" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "sssbsct" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "trans" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" ),
            "transcol" : ( "RGB", "8-bit 16-bit", "rgb(127,127,255)", True, "triangle", "1" ),
            "dens" : ( "R", "8-bit 16-bit", "rgb(255,255,255)", True, "triangle", "1" )}

def getAssetTypes():
    return {'camera':'cam',
            'character':'chr',
            'prop':'prp',
            'vehicle':'vcl',
            'interior':'int',
            'exterior':'ext',
            'material':'mtl',
            'sequence':'seq',
            'scene':'scn',
            'shot':'sht',
            'visual-effect':'vfx'}

def getAssetTasks():
    return {'animation':'ani',
            'compositing':'cmp',
            'render':'ren',  # TODO: automate creation of main(CG)/COMP forks
            'matte-painting':'dmp',
            'dynamic':'dyn',
            'fluid':'fld',
            'ibl':'ibl',
            'layout':'lay',
            'lighting':'lit',
            'modeling':'mod',  # TODO: automate creation of main/sculpt/retopo forks
            'override' :'ovr',
            'particle':'pcl',
            'camera':'cam',  # TODO: automate creation of main(render)/projection forks
            'previz':"viz",
            'rig' : 'rig',
            'rotoscopy':'rot',
            'shader':'shd',
            'surfacing':'sur',
            'texturing':'tex',  # TODO: automate creation of main(surfacing)/grooming forks
            'grooming':'grm',
            'sound':'snd',
            'concept':'cpt',
            'model-sheet':'mst'}

def getDefaultTasks ():
    return {"chr":{'animation':'ani',
                'bash-comp':'bcp',
                'render-comp':'rcp',
                'render-cg':'rcg',
                'matte-painting':'dmp',
                'dynamic':'dyn',
                'fluid':'fld',
                'ibl':'ibl',
                'layout':'lay',
                'lighting':'lit',
                'modeling':'mod',
                'override' :'ovr',
                'particle':'pcl',
                'camera-projection':'cpj',
                'camera-render':'crn',
                'previz':"viz",
                'rig' : 'rig',
                'retopo':'rtp',
                'rotoscopy':'rot',
                'sculpt':'sct',
                'shader':'shd',
                'surfacing':'sur',
                'texture':'tex',
                'texture-grooming':'tgr',
                'sound':'snd',
                'concept':'cpt',
                'model-sheet':'mst'}}
