'''
Created on Jan 13, 2013
ASSET tasks:
    modeling        : mod
    texturing       : tex
    rigging         : rig
    surfacing       : srf
    
SHOT tasks:    
    layouting       : lay
    lighting        : lit
    render          : rdr
    compositing     : cmp
    matte-painting  : dmp
    cam             : cam

ASSET type list:
    character       : chr
    vehicle         : vcl
    prop            : prp
    environment     : env
    freetype        : ***

@author: pixo
'''

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asset_task.ui'
#
# Created: Sun Jan 13 23:02:37 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template_task.ui'
#
# Created: Sun Jan 13 23:20:46 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!
import sys, os
from PySide import QtCore, QtGui
import pipeline.utils.dataBase as dataBase
import pipeline.core as core

class Ui_PushAsset(object):
    
    comments="caca"
    
    def createWidgetList(self):
        lspath=list()
        for key in self.dictpath:
            lspath.append(key)
            
        self.listWidget.addItems(lspath)
        for i in range(0,self.listWidget.count()):
            self.listWidget.item(i).setCheckState(QtCore.Qt.Unchecked)
            
    def pushClicked(self):
        lspush = list()
        for i in range(0,self.listWidget.count()):
            item=self.listWidget.item(i)
            if item.checkState()== QtCore.Qt.CheckState.Checked:
                lspush.append(self.dictpath[item.text()])
                
        core.hkrepository.push(self.db, self.doc_id, lspush, self.comments)
                        
        print lspush 
            
#             self.listWidget.item(i).setCheckState(QtCore.Qt.Unchecked)
            
    def setupUi(self, Form, db, doc_id, dictpath=dict()):
        self.db=db
        self.doc_id=doc_id
        self.dictpath=dictpath
        Form.setObjectName("Form")
        Form.resize(438, 392)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Push")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
       
        self.createWidgetList()
        self.pushButton.clicked.connect(self.pushClicked)
        QtCore.QMetaObject.connectSlotsByName(Form)


class Ui_MainWindow(object):
    
    
    project=os.getenv("HK_PROJECT")
    db=dataBase.getDataBase()
    assetConv = {"character":"chr",
                "environment":"env",
                "prop":"prp",
                "vehicle":"vcl",}
    
    taskConv = {"modeling":"mod",
                "texturing":"tex",
                "rigging":"rig",
                "surfacing":"srf"}
            
    def setInfo(self):
        "print setinfo"   
        typ = self.assetType.currentItem()
        if typ :
            typ = self.assetConv[ typ.text() ]
            name = typ
        else :
            typ = ""
        
        
        asset = self.asset.currentItem()
        if asset :
            asset = self.asset.currentItem().text()
            name = asset

        else :
            asset = ""
        
        taskType = self.taskType.currentItem()    
        if taskType :
            taskType = self.taskConv[taskType.text()]
            name = asset+"_" + taskType

        else :
            taskType = ""
            
        task = self.task.currentItem()
        if task :
            task = task.text()
            name=task

        else :
            task = ""
                
        self.label.setText( name )
    
    def assetTypeClicked(self):
        filtr = self.assetConv [self.assetType.currentItem().text()]
        startkey = u"%s_%s" % ( self.project, filtr )
        endkey = u"%s_%s\u0fff" % ( self.project, filtr )
        curlist = dataBase.lsDb(self.db, filtr , startkey,endkey)
        self.asset.clear()
        self.taskType.clear()
        self.task.clear()
        self.asset.addItems(curlist)
        self.setInfo()
        self.pullButton.setDisabled(True)
        self.pushButton.setDisabled(True)
        
    def assetClicked(self):       
        self.taskType.clear()
        taskType = list({"modeling", "texturing", "rigging", "surfacing"})
        self.taskType.addItems(taskType)
        self.task.clear()
        self.setInfo()
        self.pullButton.setDisabled(True)
        self.pushButton.setDisabled(True)

    def taskTypeClicked(self):
        taskType = self.taskConv[self.taskType.currentItem().text()]
        asset = self.asset.currentItem().text()
        startkey = u"%s_%s_%s" % ( self.project, asset, taskType )
        endkey = u"%s_%s_%s\u0fff" % ( self.project, asset, taskType )
        curlist = dataBase.lsDb(self.db, "asset_task" , startkey,endkey)
        self.task.clear()
        self.task.addItems(curlist)
        self.setInfo()
        self.pullButton.setDisabled(True)
        self.pushButton.setDisabled(True)
        
    def taskClicked(self):
        self.setInfo()
        self.doc_id="%s_%s" % (self.project,self.label.text())
        self.workspace=core.hkrepository.getWorkspaceFromId(self.db, self.doc_id)
        self.statusbar.showMessage(self.workspace)
        
        if os.path.exists(self.workspace):
            self.pushButton.setDisabled(False)
            
        
    def pushClicked(self):
        lsdir = os.listdir(self.workspace)
        dictpath=dict()
        
        for file in lsdir:
            path=os.path.join(self.workspace,file)
            if os.path.isfile(path):
                dictpath[file]=path
        
        self.widget = QtGui.QWidget()
        self.setupui = Ui_PushAsset()
        self.setupui.setupUi( self.widget,self.db,self.doc_id,dictpath )
        self.widget.show()
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(972, 806)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.assetType = QtGui.QListWidget(self.centralwidget)
        self.assetType.setObjectName("assettype")
        self.horizontalLayout_2.addWidget(self.assetType)
        self.asset = QtGui.QListWidget(self.centralwidget)
        self.asset.setObjectName("asset")
        self.horizontalLayout_2.addWidget(self.asset)
        self.taskType = QtGui.QListWidget(self.centralwidget)
        self.taskType.setObjectName("tasktype")
        self.horizontalLayout_2.addWidget(self.taskType)
        self.task = QtGui.QListWidget(self.centralwidget)
        self.task.setObjectName("task")
        self.horizontalLayout_2.addWidget(self.task)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.pullButton = QtGui.QPushButton(self.centralwidget)
        self.pullButton.setObjectName("pullButton")
        self.horizontalLayout_3.addWidget(self.pullButton)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.assetType.clicked.connect(self.assetTypeClicked)
        self.asset.clicked.connect(self.assetClicked)
        self.taskType.clicked.connect(self.taskTypeClicked)
        self.task.clicked.connect(self.taskClicked)
        self.pushButton.clicked.connect(self.pushClicked)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
  
        self.assetType.setSortingEnabled(True)        
        self.asset.setSortingEnabled(True)
        self.assetType.addItems(list({"character","prop","vehicle","environment"})) 
       
        self.label.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Push", None, QtGui.QApplication.UnicodeUTF8))
        self.pullButton.setText(QtGui.QApplication.translate("MainWindow", "Pull", None, QtGui.QApplication.UnicodeUTF8))


# Create a Qt application
app = QtGui.QApplication(sys.argv)

main=QtGui.QMainWindow()
setupui=Ui_MainWindow()
setupui.setupUi(main)
main.show()

# Enter Qt application main loop
app.exec_()
sys.exit()

