# import sys
# from PySide import QtGui
# import pipeline.apps as apps
# 
# if __name__ == '__main__':
#     app = QtGui.QApplication ( sys.argv )    
#     main = apps.UiAssetManager()
#     main.show()
#     app.exec_()
#     sys.exit()

import pipeline.utils as utils

# excludes = list( { "sct", "mod", "tex",".Trash-1000", "\#recycle", "*.pyc"} )
# source = "homeworks@89.92.153.132:/volume1/projects/tst"
# destination = "/norman/r.chikh/Documents"

# utils.rsync ( source = source, destination=destination, excludes=excludes )


tasks = list ()

a = utils.getAssetTasks()
for k in a : tasks.append ( a[k] )

tasks.remove('rot')
print tasks