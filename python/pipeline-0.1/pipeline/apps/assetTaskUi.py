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
    
    def createWidgetList( self ):
        lspath = list()
        for key in self.dictpath:
            lspath.append( key )
            
        self.listWidget_file.addItems( lspath )
        for i in range( 0, self.listWidget_file.count() ):
            self.listWidget_file.item(i).setCheckState( QtCore.Qt.Unchecked )
            
    def pushClicked(self):
        lspush = list()
        
        for i in range( 0, self.listWidget_file.count() ):
            item = self.listWidget_file.item(i)
            
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                lspush.append( self.dictpath[item.text()] )
                
        textdoc = self.plainTextEdit_comments.document()
        comments = textdoc.toPlainText()
        core.hkrepository.push( self.db, self.doc_id, lspush,
                                comments, self.progressBar)
        self.progressBar.setValue(0)
        
    def fileLineChanged( self ):
        print " lineTextChanged changed "
        
    def commentsChanged( self ):        
        textdoc = self.plainTextEdit_comments.document()
        comments = textdoc.toPlainText()
        
        if not ( comments == "" ):
            self.pushButton.setEnabled(False)
        else :
            self.pushButton.setEnabled(True) 
        
    def listFileClicked(self):
        current_item = self.listWidget_file.currentItem()
        current_index = self.listWidget_file.currentIndex().row()
        if current_item.checkState() == QtCore.Qt.CheckState.Checked:
            for i in range( 0, self.listWidget_file.count() ):
                if current_index != i :
                    self.listWidget_file.item(i).setCheckState( QtCore.
                                                                Qt.Unchecked )
                
        print "act"
    def signalConnect(self):
        """ Connect the UI to the Ui_AssetWindow methods """
        self.listWidget_file.clicked.connect(self.listFileClicked)
        self.pushButton.clicked.connect( self.pushClicked )
        self.lineEdit_file.textChanged.connect( self.fileLineChanged )
        self.plainTextEdit_comments.textChanged.connect( self.commentsChanged )
        
    def setupUi( self, Form, db, doc_id, dictpath):
        self.db=db
        self.doc_id=doc_id
        self.dictpath=dictpath
        Form.setObjectName("Form")
        Form.resize(665, 573)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout_top = QtGui.QHBoxLayout()
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")
        self.label_file = QtGui.QLabel(Form)
        self.label_file.setAlignment(QtCore.Qt.AlignCenter)
        self.label_file.setObjectName("label_file")
        self.horizontalLayout_top.addWidget(self.label_file)
        self.label_comments = QtGui.QLabel(Form)
        self.label_comments.setAlignment(QtCore.Qt.AlignCenter)
        self.label_comments.setObjectName("label_comments")
        self.horizontalLayout_top.addWidget(self.label_comments)
        self.verticalLayout_main.addLayout(self.horizontalLayout_top)
        self.horizontalLayout_center = QtGui.QHBoxLayout()
        self.horizontalLayout_center.setObjectName("horizontalLayout_center")
        self.verticalLayout_file = QtGui.QVBoxLayout()
        self.verticalLayout_file.setObjectName("verticalLayout_file")
        self.lineEdit_file = QtGui.QLineEdit(Form)
        self.lineEdit_file.setObjectName("lineEdit_file")
        self.verticalLayout_file.addWidget(self.lineEdit_file)
        self.listWidget_file = QtGui.QListWidget(Form)
        self.listWidget_file.setObjectName("listWidget_file")
        self.listWidget_file.alternatingRowColors()
        self.listWidget_file.setSortingEnabled(True)
        self.verticalLayout_file.addWidget(self.listWidget_file)
        self.horizontalLayout_center.addLayout(self.verticalLayout_file)
        self.plainTextEdit_comments = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit_comments.setObjectName("plainTextEdit_comments")
        self.horizontalLayout_center.addWidget(self.plainTextEdit_comments)
        self.verticalLayout_main.addLayout(self.horizontalLayout_center)
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_bottom.addWidget(self.progressBar)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setEnabled(False)
        self.horizontalLayout_bottom.addWidget(self.pushButton)
        self.verticalLayout_main.addLayout(self.horizontalLayout_bottom)
        self.verticalLayout_2.addLayout(self.verticalLayout_main)

        self.createWidgetList()
        self.signalConnect()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Asset Push", None, QtGui.QApplication.UnicodeUTF8))
        self.label_file.setText(QtGui.QApplication.translate("Form", "File ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_comments.setText(QtGui.QApplication.translate("Form", "Comments", None, QtGui.QApplication.UnicodeUTF8))        
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Push", None, QtGui.QApplication.UnicodeUTF8))

class Ui_AssetWindow(object):
    
    
    db = dataBase.getDataBase ()
    doc_id = ""
    project = os.getenv ( "HK_PROJECT" )
    assetNamingConv = {"character":"chr",
                    "environment":"env",
                    "prop":"prp",
                    "vehicle":"vcl",}
    
    taskNamingConv = {"modeling":"mod",
                    "texturing":"tex",
                    "rigging":"rig",
                    "surfacing":"srf"}

    def setInfo(self):
        typ = self.listWidget_asset_type.currentItem()
        if typ :
            typ = self.assetNamingConv[ typ.text() ]
            name = typ
        else :
            typ = ""
        
        asset = self.listWidget_asset.currentItem()
        if asset :
            asset = self.listWidget_asset.currentItem().text()
            name = asset
        else :
            asset = ""
        
        taskType = self.listWidget_task_type.currentItem()    
        if taskType :
            taskType = self.taskNamingConv[taskType.text()]
            name = "%s_%s" % ( asset, taskType )
        else :
            taskType = ""
            
        task = self.listWidget_task.currentItem()
        if task :
            task = task.text()
            name=task
        else :
            task = ""
                
        self.label_doc_id.setText( name )
    
    def assetTypeClicked(self):
        filtr = self.assetNamingConv [(self.listWidget_asset_type.
                                       currentItem().text())]
        startkey = u"%s_%s" % ( self.project, filtr )
        endkey = u"%s_%s\u0fff" % ( self.project, filtr )
        curlist = dataBase.lsDb(self.db, filtr , startkey,endkey)
        self.listWidget_asset.clear()
        self.listWidget_task_type.clear()
        self.listWidget_task.clear()
        self.listWidget_asset.addItems(curlist)
        self.setInfo()
        self.pullButton.setDisabled(True)
        self.pushButton.setDisabled(True)
        
    def assetClicked(self):       
        self.listWidget_task_type.clear()
        taskType = list({"modeling", "texturing", "rigging", "surfacing"})
        self.listWidget_task_type.addItems(taskType)
        self.listWidget_task.clear()
        self.setInfo()
        self.pullButton.setDisabled(True)
        self.pushButton.setDisabled(True)

    def taskTypeClicked(self):
        taskType = (self.taskNamingConv[self.listWidget_task_type.
                                        currentItem().text()])
        asset = self.listWidget_asset.currentItem().text()
        startkey = u"%s_%s_%s" % ( self.project, asset, taskType )
        endkey = u"%s_%s_%s\u0fff" % ( self.project, asset, taskType )
        curlist = dataBase.lsDb(self.db, "asset_task" , startkey,endkey)
        self.listWidget_task.clear()
        self.listWidget_task.addItems(curlist)
        self.setInfo()
        self.pullButton.setDisabled(True)
        self.pushButton.setDisabled(True)
        
    def taskClicked(self):
        self.setInfo()
        self.doc_id="%s_%s" % (self.project,self.label_doc_id.text())
        self.workspace=core.hkrepository.getWorkspaceFromId(self.db,
                                                            self.doc_id)
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
        
        checkable = False
        self.widget_push = QtGui.QWidget()
        self.setupui = Ui_PushAsset()
        self.setupui.setupUi( self.widget_push, self.db,
                              self.doc_id, dictpath)
        self.widget_push.show()
        
    def pullClicked(self):
        ""
        
    def signalConnect(self):
        """Connect the UI to the Ui_AssetWindow methods"""
        self.listWidget_asset_type.clicked.connect(self.assetTypeClicked)
        self.listWidget_asset.clicked.connect(self.assetClicked)
        self.listWidget_task_type.clicked.connect(self.taskTypeClicked)
        self.listWidget_task.clicked.connect(self.taskClicked)
        self.pullButton.clicked.connect(self.pullClicked)
        self.pushButton.clicked.connect(self.pushClicked)
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(972, 806)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_top = QtGui.QHBoxLayout()
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")
        self.label_asset_type = QtGui.QLabel(self.centralwidget)
        self.label_asset_type.setAlignment(QtCore.Qt.AlignCenter)
        self.label_asset_type.setObjectName("label_asset_type")
        self.horizontalLayout_top.addWidget(self.label_asset_type)
        self.label_asset = QtGui.QLabel(self.centralwidget)
        self.label_asset.setAlignment(QtCore.Qt.AlignCenter)
        self.label_asset.setObjectName("label_asset")
        self.horizontalLayout_top.addWidget(self.label_asset)
        self.label_task_type = QtGui.QLabel(self.centralwidget)
        self.label_task_type.setAlignment(QtCore.Qt.AlignCenter)
        self.label_task_type.setObjectName("label_task_type")
        self.horizontalLayout_top.addWidget(self.label_task_type)
        self.label_task = QtGui.QLabel(self.centralwidget)
        self.label_task.setAlignment(QtCore.Qt.AlignCenter)
        self.label_task.setObjectName("label_task")
        self.horizontalLayout_top.addWidget(self.label_task)
        self.verticalLayout.addLayout(self.horizontalLayout_top)
        self.horizontalLayout_selector = QtGui.QHBoxLayout()
        self.horizontalLayout_selector.setObjectName("horizontalLayout_select")
        self.verticalLayout_assetType = QtGui.QVBoxLayout()
        self.verticalLayout_assetType.setObjectName("verticalLayout_assetType")
        self.lineEdit_asset_type = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_asset_type.setObjectName("lineEdit_asset_type")
        self.verticalLayout_assetType.addWidget(self.lineEdit_asset_type)
        self.listWidget_asset_type = QtGui.QListWidget(self.centralwidget)
        self.listWidget_asset_type.setObjectName("listWidget_asset_type")
        self.listWidget_asset_type.alternatingRowColors()
        self.listWidget_asset_type.setSortingEnabled(True)
        self.verticalLayout_assetType.addWidget(self.listWidget_asset_type)
        self.horizontalLayout_selector.addLayout(self.verticalLayout_assetType)
        self.verticalLayout_asset = QtGui.QVBoxLayout()
        self.verticalLayout_asset.setObjectName("verticalLayout_asset")
        self.lineEdit_asset = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_asset.setObjectName("lineEdit_asset")
        self.verticalLayout_asset.addWidget(self.lineEdit_asset)
        self.listWidget_asset = QtGui.QListWidget(self.centralwidget)
        self.listWidget_asset.setObjectName("listWidget_asset")
        self.listWidget_asset.alternatingRowColors()
        self.listWidget_asset.setSortingEnabled(True)
        self.verticalLayout_asset.addWidget(self.listWidget_asset)
        self.horizontalLayout_selector.addLayout(self.verticalLayout_asset)
        self.verticalLayout_taskType = QtGui.QVBoxLayout()
        self.verticalLayout_taskType.setObjectName("verticalLayout_taskType")
        self.lineEdit_task_type = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_task_type.setObjectName("lineEdit_task_type")
        self.verticalLayout_taskType.addWidget(self.lineEdit_task_type)
        self.listWidget_task_type = QtGui.QListWidget(self.centralwidget)
        self.listWidget_task_type.setObjectName("listWidget_task_type")
        self.listWidget_task_type.alternatingRowColors()
        self.listWidget_task_type.setSortingEnabled(True)
        self.verticalLayout_taskType.addWidget(self.listWidget_task_type)
        self.horizontalLayout_selector.addLayout(self.verticalLayout_taskType)
        self.verticalLayout_task = QtGui.QVBoxLayout()
        self.verticalLayout_task.setObjectName("verticalLayout_task")
        self.lineEdit_task = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_task.setObjectName("lineEdit_task")
        self.verticalLayout_task.addWidget(self.lineEdit_task)
        self.listWidget_task = QtGui.QListWidget(self.centralwidget)
        self.listWidget_task.setObjectName("listWidget_task")
        self.listWidget_task.alternatingRowColors()
        self.listWidget_task.setSortingEnabled(True)
        self.verticalLayout_task.addWidget(self.listWidget_task)
        self.horizontalLayout_selector.addLayout(self.verticalLayout_task)
        self.verticalLayout.addLayout(self.horizontalLayout_selector)
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        self.label_doc_id = QtGui.QLabel(self.centralwidget)
        self.label_doc_id.setObjectName("label_doc_id")
        self.horizontalLayout_bottom.addWidget(self.label_doc_id)
        self.pullButton = QtGui.QPushButton(self.centralwidget)
        self.pullButton.setObjectName("pullButton")
        self.horizontalLayout_bottom.addWidget(self.pullButton)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_bottom.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_bottom)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.listWidget_asset_type.addItems(list({"character","prop",
                                                "vehicle","environment"})) 
        self.signalConnect()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow",
                                                               "asset manager",
                                                               None, QtGui.
                                                               QApplication.
                                                               UnicodeUTF8))
        
        self.label_asset_type.setText(QtGui.QApplication.translate("MainWindow",
                                                                   "asset type",
                                                                   None, QtGui.
                                                                   QApplication.
                                                                   UnicodeUTF8))
        
        self.label_asset.setText(QtGui.QApplication.translate("MainWindow",
                                                              "asset", None,
                                                              QtGui.
                                                              QApplication.
                                                              UnicodeUTF8))
        
        self.label_task_type.setText(QtGui.QApplication.translate("MainWindow",
                                                                  "task type",
                                                                  None, QtGui.
                                                                  QApplication.
                                                                  UnicodeUTF8))
        
        self.label_task.setText(QtGui.QApplication.translate("MainWindow",
                                                             "task", None,QtGui.
                                                             QApplication.
                                                             UnicodeUTF8))
        
        self.label_doc_id.setText(QtGui.QApplication.translate("MainWindow",
                                                               "TextLabel",
                                                               None, QtGui.
                                                               QApplication.
                                                               UnicodeUTF8))
        
        self.pullButton.setText(QtGui.QApplication.translate("MainWindow",
                                                             "Pull", None,
                                                             QtGui.QApplication.
                                                             UnicodeUTF8))
        
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow",
                                                             "Push", None,
                                                             QtGui.QApplication.
                                                             UnicodeUTF8))


# Create a Qt application
app = QtGui.QApplication(sys.argv)

main=QtGui.QMainWindow()
setupui=Ui_AssetWindow()
setupui.setupUi(main)
main.show()

# Enter Qt application main loop
app.exec_()
sys.exit()

