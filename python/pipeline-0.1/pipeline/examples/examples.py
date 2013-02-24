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
import os
name = "testing"
description = "test"
db = utils.getDb ()

server=os.getenv("HK_DB_SERVER")
core.createProject (name = name, description=description, serveradress= server)

# description = "The Belanus project is created to test 3dcoat and mari"
# serveradress = utils.getServer()
# core.createProject ( name="bln", description=description, serveradress=serveradress, dbname="projects")

# core.getAssetVersions("testing_chr_mickey_mod_main")

# yop = utils.getDb ( dbname = "projects", serveradress = "http://admin:admin@127.0.0.1:5984/" )
# print yop

# utils.createProjEnv("testing")
