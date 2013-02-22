'''
diffuse = diff
specular = spec
roughness = roug
sss = sss
bump = bump
normal = norm
displace = disp
mask = mask
'''
import pipeline.core as  core
import pipeline.utils as utils

# import glob, re
# 
# tex = list(("testing_ch_mickey_tex_diff.1001.tif",
#        "testing_ch_mickey_tex_spec.1001.tif",
#        "testing_ch_mickey_tex_norm.1001.tif",
#        "testing_ch_mickey_tex_norm2.1001.tif",
#        "testing_ch_mickey_tex_spic2.1001.tif"))
# 
# asset ="testing_ch_mickey_tex"
# 
# def textureCheck ( doc_id = "", files = list() ) :
#     textureType = ( "diff", "roug", "spec", "bump", "norm", "disp" )
#     
#     to_push = list()
#     not_pushed = list(files)
#         
#     for file in files :
#         for typ in textureType :
#     
#             pattern = "%s_%s\d*.\d*.tif$" % ( asset, typ )
#             
#             if re.findall ( pattern, file ) :
#                 to_push.append ( file )
#                 not_pushed.remove(file)
# 
#     return to_push
#     
# textureCheck ( asset, tex )

# name = "spare"
# description = "Projects done during my spare times"
# 
# createProject(db, name, description)

# core.createProject ( "bln", "The Belanus project is created to test 3dcoat and mari" )

core.getAssetVersions("testing_chr_mickey_mod_main")
