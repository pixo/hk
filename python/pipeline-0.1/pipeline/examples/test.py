import pipeline.utils as utils
import glob
import os

path = "/homeworks/projects/testing/repository/chr/chr_mickey/chr_mickey_mod/chr_mickey_mod_main/039"
files = glob.glob(os.path.join(path,"*.ma"))
files.extend(glob.glob(os.path.join(path,"*.mb")))
print files
# print utils.lsSeq( "/homeworks/users/pixo/projects/testing/chr/chr_mickey/chr_mickey_tex/chr_mickey_tex_main", True )