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

import re

print "'"+re.sub("[a-z]","", "thisistest")+"'"