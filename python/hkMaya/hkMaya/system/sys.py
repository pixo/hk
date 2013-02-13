'''
Created on Feb 11, 2013

@author: pixo
'''
import os

def exportAsset ( source = "", destination = "", obj=True, abc=True, gproject = True ):
        
    fname = os.path.basename(source)
    name,ext = os.path.splitext(fname)
    
    if obj :
        fobj = os.path.join( destination, name + ".obj" )
        objExportCmd = """ maya -batch -file %s  -command "loadPlugin \\"/usr/autodesk/maya2013-x64/bin/plug-ins/objExport.so\\"; file -force -options \\"groups=1;ptgroups=1;materials=0;smoothing=1;normals=1\\" -type \\"OBJexport\\" -pr -ea \\"%s\\"; " """ % ( source, fobj )   
        os.system( objExportCmd )
     
    if abc :
        fabc = os.path.join( destination, name + ".abc" )
        abcExportCmd = """ maya -batch -file %s  -command "loadPlugin \\"/usr/autodesk/maya2013-x64/bin/plug-ins/AbcExport.so\\"; AbcExport -j \\"-frameRange 1 1 -file %s\\";" """ % ( source, fabc )
        os.system( abcExportCmd )
    
    if gproject :
        fgproject = os.path.join( destination, name + ".gproject" )
        gprojectExportCmd = """ maya -batch -file %s  -command "loadPlugin \\"/usr/autodesk/maya2013-x64/bin/plug-ins/guerilla2013.so\\"; GuerillaExport -m 1 -a 1 -pf \\"%s\\";file -f -save; " """ % ( source, fgproject )
        os.system( gprojectExportCmd )
            
    return True

# exportAsset ( source = "/home/pixo/test/test.mb", destination = "/home/pixo/test" )