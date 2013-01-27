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
    typ = {"character":"chr",
    "vehicle":"vcl",
    "prop":"prp",
    "environment":"env",
    "effect":"vfx"}
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
import pipeline.utils as utils
import pipeline.core as core

class UiPull(object):
    
    def searchLineChanged(self, lineEdit, listWidget):
        filter = lineEdit.text()
        if filter != "" :
            for i in range( 0, listWidget.count() ):
                text = listWidget.item(i).text()
                item = listWidget.item(i)
                
                if text.find(filter) >= 0 :
                    item.setHidden (False)
                else:
                    item.setHidden (True)
        else:
            for i in range( 0, listWidget.count() ):
                item = listWidget.item(i)
                item.setHidden(False)
            
    def searchVersion(self):
        self.searchLineChanged(self.lineEdit_version, self.listWidget_version)
        
    def createWorkspace(self):
        self.progressBar.setValue(0)
        core.hkrepository.createWorkspace( self.db, self.doc_id )
        self.progressBar.setValue(100)
        
    def createWidgetList( self ):
        if not (len(self.versions) == 0):
            lspath = list()
            self.convDict = dict()
            
            for key in self.versions:
                ver = "v%03d" % float(key)
                self.convDict[ver] = key
                lspath.append( ver )
                
            self.listWidget_version.addItems( lspath )
            self.pullButton.clicked.connect( self.pullClicked )
            self.pullButton.setText("Pull")
            
        else :
            self.pullButton.setDisabled(False)
            self.pullButton.setText("Create workspace")
            self.pullButton.clicked.connect( self.createWorkspace )
        
    def listWidgetClicked(self):
        self.pullButton.setDisabled(False)
        item = self.listWidget_version.currentItem()
        dbver = self.convDict[item.text()]
        comment = self.versions[ dbver ]["comments"]
        self.plainTextEdit_comment.setPlainText(comment)

        path = self.versions[ dbver ]["path"]
        path = os.path.expandvars(path)
        path = os.path.join (path, "%s_%s.scr" % ( self.doc_id, item.text() ))
        
        if os.path.exists(path):  
            qpix = QtGui.QPixmap()
            qpix.load( path )
            self.labelImage.setPixmap( qpix )
        
    def pullClicked(self):
        self.progressBar.setValue(0)
        item =self.listWidget_version.currentItem()
        ver = self.convDict[item.text()]
        core.hkrepository.pull(self.db, self.doc_id, ver, self.progressBar)
        
    def signalConnect(self):
        """ Connect methods """
        self.lineEdit_version.textChanged.connect( self.searchVersion )
        self.listWidget_version.clicked.connect(self.listWidgetClicked)
    
    def setupUi(self, Form, db, doc_id):
        self.db = db
        self.doc_id = doc_id
        self.versions = self.db[self.doc_id]["versions"]
        Form.setObjectName("Pull")
        Form.resize(556, 532)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_version = QtGui.QLineEdit(Form)
        self.lineEdit_version.setObjectName("lineEdit_version")
        self.verticalLayout.addWidget(self.lineEdit_version)
        self.listWidget_version = QtGui.QListWidget(Form)
        self.listWidget_version.setSortingEnabled(True)
        self.listWidget_version.setObjectName("listWidget_version")
        self.verticalLayout.addWidget(self.listWidget_version)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelImage = QtGui.QLabel(Form)
        self.labelImage.setMinimumSize(QtCore.QSize(300, 300))
        self.labelImage.setText("")
        self.labelImage.setObjectName("labelImage")
        self.verticalLayout_2.addWidget(self.labelImage)
        self.plainTextEdit_comment = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit_comment.setEnabled(False)
        self.plainTextEdit_comment.setObjectName("plainTextEdit_comment")
        self.verticalLayout_2.addWidget(self.plainTextEdit_comment)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_main.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.pullButton = QtGui.QPushButton(Form)
        self.pullButton.setDisabled(True)
        self.pullButton.setObjectName("pullButton")
        self.horizontalLayout_3.addWidget(self.pullButton)
        self.verticalLayout_main.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_main)

        self.createWidgetList()
        self.signalConnect()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Pull", "Pull", None, QtGui.QApplication.UnicodeUTF8))
        
#         self.pullButton.setText(QtGui.QApplication.translate("Form", "Pull", None, QtGui.QApplication.UnicodeUTF8))

            

                        
class UiPush(object):

    
    def searchLineChanged(self, lineEdit, listWidget):
        filter = lineEdit.text()
        if filter != "" :
            for i in range( 0, listWidget.count() ):
                text = listWidget.item(i).text()
                item = listWidget.item(i)
                
                if text.find(filter) >= 0 :
                    item.setHidden (False)
                else:
                    item.setHidden (True)
        else:
            for i in range( 0, listWidget.count() ):
                item = listWidget.item(i)
                item.setHidden(False)
                
    def fileLineChanged( self ):
        self.searchLineChanged(self.lineEdit_file, self.listWidget_file)
        
    def createWidgetList( self ):
        self.workspace = core.hkrepository.getWorkspaceFromId(self.db,
                                                            self.doc_id)
        lsdir = os.listdir(self.workspace)
        dictpath = dict()
        
        for file in lsdir :
            path = os.path.join (self.workspace, file)
            if os.path.isfile (path) :
                dictpath[file] = path
        self.dictpath=dictpath
                
        lspath = list()
        for key in self.dictpath:
            lspath.append( key )
            
        self.listWidget_file.addItems( lspath )
            
    def pushClicked(self):
        lspush = list()
        self.progressBar.setValue(0)
        
        item = self.listWidget_file.currentItem()
        lspush.append( self.dictpath[item.text()] )
                
        comments = self.plainTextEdit_comments.toPlainText()
        core.hkrepository.push( self.db, self.doc_id, lspush,
                                comments, self.progressBar)
        
    def commentsChanged( self ):        
        textdoc = self.plainTextEdit_comments.document()
        comments = textdoc.toPlainText()
        
        if comments == "" :
            self.pushButton.setEnabled(False)
        else :
            self.pushButton.setEnabled(True) 
        
    def signalConnect(self):
        """ Connect the UI to the Ui_AssetWindow methods """
        self.pushButton.clicked.connect( self.pushClicked )
        self.lineEdit_file.textChanged.connect( self.fileLineChanged )
        self.plainTextEdit_comments.textChanged.connect( self.commentsChanged )
        
    def setupUi( self, Form, db, doc_id):
        #TODO add push button select all
        self.db=db
        self.doc_id=doc_id
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
        self.pushButton.setToolTip("Make sure to leave a comment")
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
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Push", None, QtGui.QApplication.UnicodeUTF8))
        self.label_file.setText(QtGui.QApplication.translate("Form", "File ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_comments.setText(QtGui.QApplication.translate("Form", "Comments", None, QtGui.QApplication.UnicodeUTF8))        
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Push", None, QtGui.QApplication.UnicodeUTF8))

class UiPushLs(UiPush):
    
    def createWidgetList( self ):
        self.workspace = core.hkrepository.getWorkspaceFromId(self.db,
                                                            self.doc_id)        
        self.dictpath = utils.system.lsSeq(self.workspace)
        
        lspath = list()
        for key in self.dictpath:
            lspath.append( key )
            
        self.listWidget_file.addItems( lspath )
        for i in range( 0, self.listWidget_file.count() ):
            self.listWidget_file.item(i).setCheckState( QtCore.Qt.Unchecked )
            
    def pushClicked(self):
        lspush = list()
        self.progressBar.setValue(0)
        
        for i in range( 0, self.listWidget_file.count() ):
            item = self.listWidget_file.item(i)
            
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                lspush.extend( self.dictpath[item.text()] )
                
        textdoc = self.plainTextEdit_comments.document()
        comments = textdoc.toPlainText()
        core.hkrepository.push( self.db, self.doc_id, lspush,
                                comments, self.progressBar, False)
        

class Ui_MainWindow(object):
    
    
    db = dataBase.getDataBase ()
    doc_id = ""
    project = os.getenv ( "HK_PROJECT" )
    
    app_name = "main window"
    list_a_name = "list_a"
    list_b_name = "list_b"
    list_c_name = "list_c"
    list_d_name = "list_d"
    
    def buildUi(self):
        self.listWidget_a.addItems(self.get_list_a()) 
    
    def searchLineChanged(self, lineEdit, listWidget):
        filter = lineEdit.text()
        if filter != "" :
            for i in range( 0, listWidget.count() ):
                text = listWidget.item(i).text()
                item = listWidget.item(i)
                
                if text.find(filter) >= 0 :
                    item.setHidden (False)
                else:
                    item.setHidden (True)
        else:
            for i in range( 0, listWidget.count() ):
                item = listWidget.item(i)
                item.setHidden(False)
                
    def get_list_a(self):
        return list(["list_a_1", "list_a_2", "list_a_3", "list_a_4"])
        
    def get_list_b(self):
        return list(["list_b_1", "list_b_2", "list_b_3", "list_b_4"])
    
    def get_list_c(self):
        return list(["list_c_1", "list_c_2", "list_c_3", "list_c_4"])
    
    def get_list_d(self):
        return list(["list_d_1", "list_d_2", "list_d_3", "list_d_4"])
        
    def clicked_a(self):
        self.listWidget_b.clear()
        self.listWidget_c.clear()
        self.listWidget_d.clear()
        
        item = self.listWidget_a.currentItem()
        self.part_a = item.text() if item else ""
        self.listWidget_b.addItems(self.get_list_b())

        self.pullButton.setDisabled(True)
        self.pushButton.setDisabled(True)
        
    def clicked_b(self):       
        self.listWidget_c.clear()
        self.listWidget_d.clear()
        
        item = self.listWidget_b.currentItem()
        self.part_b = item.text() if item else ""
        self.listWidget_c.addItems(self.get_list_c())

        self.pullButton.setDisabled(True)
        self.pushButton.setDisabled(True)
        
    def clicked_c(self):
        self.listWidget_d.clear()
        
        item = self.listWidget_c.currentItem()
        self.part_c = item.text() if item else ""
        self.listWidget_d.addItems(self.get_list_d())
                
        self.pullButton.setDisabled(True)
        self.pushButton.setDisabled(True)
        
    def clicked_d(self):
        item =  self.listWidget_d.currentItem()
        self.part_d= item.text() if item else ""
        
        self.doc_id ="%s_%s" % (self.project,self.part_d)
        self.workspace=core.hkrepository.getWorkspaceFromId(self.db,
                                                            self.doc_id)
        self.statusbar.showMessage(self.workspace)
        if os.path.exists(self.workspace):
            self.pushButton.setDisabled(False)
            
        #TODO:Activate only if a version is available               
        self.pullButton.setDisabled(False)
            
    def pushClicked(self):
      
        self.widget_push = QtGui.QWidget()
#         self.uiPushAsset = UiPush()
        self.uiPushAsset = UiPushLs()
        self.uiPushAsset.setupUi( self.widget_push, self.db,
                                  self.doc_id)
        self.widget_push.show()
        
    def pullClicked(self):
        versions = self.db[self.doc_id]["versions"]
        self.widget_pull = QtGui.QWidget()
        self.uiPullAsset = UiPull()
        self.uiPullAsset.setupUi( self.widget_pull, self.db, self.doc_id)
        self.widget_pull.show()
        
    def filter_a(self):
        self.searchLineChanged(self.lineEdit_a, self.listWidget_a)
        
    def filter_b(self):
        self.searchLineChanged(self.lineEdit_b, self.listWidget_b)
        
    def filter_c(self):
        self.searchLineChanged(self.lineEdit_c, self.listWidget_c)
            
    def filter_d(self):
        self.searchLineChanged(self.lineEdit_d, self.listWidget_d)
        
    def signalConnect(self):
        """Connect the UI to the Ui_AssetWindow methods"""
        self.listWidget_a.clicked.connect(self.clicked_a)
        self.listWidget_b.clicked.connect(self.clicked_b)
        self.listWidget_c.clicked.connect(self.clicked_c)
        self.listWidget_d.clicked.connect(self.clicked_d)
        self.lineEdit_a.textChanged.connect(self.filter_a)
        self.lineEdit_b.textChanged.connect(self.filter_b)
        self.lineEdit_c.textChanged.connect(self.filter_c)
        self.lineEdit_d.textChanged.connect(self.filter_d)
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
        self.label_a = QtGui.QLabel(self.centralwidget)
        self.label_a.setAlignment(QtCore.Qt.AlignCenter)
        self.label_a.setObjectName("label_a")
        self.horizontalLayout_top.addWidget(self.label_a)
        self.label_b = QtGui.QLabel(self.centralwidget)
        self.label_b.setAlignment(QtCore.Qt.AlignCenter)
        self.label_b.setObjectName("label_b")
        self.horizontalLayout_top.addWidget(self.label_b)
        self.label_c = QtGui.QLabel(self.centralwidget)
        self.label_c.setAlignment(QtCore.Qt.AlignCenter)
        self.label_c.setObjectName("label_c")
        self.horizontalLayout_top.addWidget(self.label_c)
        self.label_d = QtGui.QLabel(self.centralwidget)
        self.label_d.setAlignment(QtCore.Qt.AlignCenter)
        self.label_d.setObjectName("label_d")
        self.horizontalLayout_top.addWidget(self.label_d)
        self.verticalLayout.addLayout(self.horizontalLayout_top)
        self.horizontalLayout_selector = QtGui.QHBoxLayout()
        self.horizontalLayout_selector.setObjectName("horizontalLayout_select")
        self.verticalLayout_a = QtGui.QVBoxLayout()
        self.verticalLayout_a.setObjectName("verticalLayout_a")
        self.lineEdit_a = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_a.setObjectName("lineEdit_a")
        self.verticalLayout_a.addWidget(self.lineEdit_a)
        self.listWidget_a = QtGui.QListWidget(self.centralwidget)
        self.listWidget_a.setObjectName("listWidget_a")
        self.listWidget_a.alternatingRowColors()
        self.listWidget_a.setSortingEnabled(True)
        self.verticalLayout_a.addWidget(self.listWidget_a)
        self.horizontalLayout_selector.addLayout(self.verticalLayout_a)
        self.verticalLayout_b = QtGui.QVBoxLayout()
        self.verticalLayout_b.setObjectName("verticalLayout_b")
        self.lineEdit_b = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_b.setObjectName("lineEdit_b")
        self.verticalLayout_b.addWidget(self.lineEdit_b)
        self.listWidget_b = QtGui.QListWidget(self.centralwidget)
        self.listWidget_b.setObjectName("listWidget_b")
        self.listWidget_b.alternatingRowColors()
        self.listWidget_b.setSortingEnabled(True)
        self.verticalLayout_b.addWidget(self.listWidget_b)
        self.horizontalLayout_selector.addLayout(self.verticalLayout_b)
        self.verticalLayout_c = QtGui.QVBoxLayout()
        self.verticalLayout_c.setObjectName("verticalLayout_c")
        self.lineEdit_c = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_c.setObjectName("lineEdit_c")
        self.verticalLayout_c.addWidget(self.lineEdit_c)
        self.listWidget_c = QtGui.QListWidget(self.centralwidget)
        self.listWidget_c.setObjectName("listWidget_c")
        self.listWidget_c.alternatingRowColors()
        self.listWidget_c.setSortingEnabled(True)
        self.verticalLayout_c.addWidget(self.listWidget_c)
        self.horizontalLayout_selector.addLayout(self.verticalLayout_c)
        self.verticalLayout_d = QtGui.QVBoxLayout()
        self.verticalLayout_d.setObjectName("verticalLayout_d")
        self.lineEdit_d = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_d.setObjectName("lineEdit_d")
        self.verticalLayout_d.addWidget(self.lineEdit_d)
        self.listWidget_d = QtGui.QListWidget(self.centralwidget)
        self.listWidget_d.setObjectName("listWidget_d")
        self.listWidget_d.alternatingRowColors()
        self.listWidget_d.setSortingEnabled(True)
        self.verticalLayout_d.addWidget(self.listWidget_d)
        self.horizontalLayout_selector.addLayout(self.verticalLayout_d)
        self.verticalLayout.addLayout(self.horizontalLayout_selector)
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        self.label_doc_id = QtGui.QLabel(self.centralwidget)
        self.label_doc_id.setObjectName("label_doc_id")
        self.horizontalLayout_bottom.addWidget(self.label_doc_id)
        self.pullButton = QtGui.QPushButton(self.centralwidget)
        self.pullButton.setObjectName("pullButton")
        self.pullButton.setDisabled(True)
        self.horizontalLayout_bottom.addWidget(self.pullButton)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setDisabled(True)
        self.horizontalLayout_bottom.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_bottom)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.buildUi()
        self.signalConnect()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow",
                                                               self.app_name,
                                                               None, QtGui.
                                                               QApplication.
                                                               UnicodeUTF8))
        
        self.label_a.setText(QtGui.QApplication.translate("MainWindow",
                                                           self.list_a_name,
                                                           None, QtGui.
                                                           QApplication.
                                                           UnicodeUTF8))
        
        self.label_b.setText(QtGui.QApplication.translate("MainWindow",
                                                          self.list_b_name,
                                                          None, QtGui.
                                                          QApplication.
                                                          UnicodeUTF8))
        
        self.label_c.setText(QtGui.QApplication.translate("MainWindow",
                                                          self.list_c_name,
                                                          None, QtGui.
                                                          QApplication.
                                                          UnicodeUTF8))
        
        self.label_d.setText(QtGui.QApplication.translate("MainWindow",
                                                          self.list_d_name,
                                                          None,QtGui.
                                                          QApplication.
                                                          UnicodeUTF8))
        
        self.label_doc_id.setText(QtGui.QApplication.translate("MainWindow",
                                                               "Welcome",
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
        
class Ui_AssetWindow(Ui_MainWindow):
    """ """
    assetNamingConv = {"character":"chr",
                    "environment":"env",
                    "prop":"prp",
                    "vehicle":"vcl",
                    "effect":"vfx",}
    
    taskNamingConv = {"modeling":"mod",
                    "texturing":"tex",
                    "rigging":"rig",
                    "surfacing":"srf"}
    
    app_name = "asset manager"
    list_a_name = "asset type"
    list_b_name = "asset"
    list_c_name = "task type"
    list_d_name = "task"   
                        
    def get_list_a(self):
        return list(["character", "prop", "vehicle", "environment"])
        
    def get_list_b(self):
        self.part_a = self.assetNamingConv [self.part_a]
        startkey = u"%s_%s" % ( self.project, self.part_a )
        endkey = u"%s_%s\u0fff" % ( self.project, self.part_a )
        result = dataBase.lsDb(self.db, self.part_a , startkey,endkey)
        return result
    
    def get_list_c(self):
        return list(["modeling", "texturing", "rigging", "surfacing"])
    
    def get_list_d(self):
        self.part_c = self.taskNamingConv[self.part_c]
        startkey = u"%s_%s_%s" % ( self.project, self.part_b, self.part_c )
        endkey = u"%s_%s_%s\u0fff" % ( self.project, self.part_b, self.part_c )
        result = dataBase.lsDb(self.db, "asset_task" , startkey,endkey)
        return result
    
        
class Ui_ShotWindow(Ui_MainWindow):
    """ """
    assetNamingConv = {"character":"chr",
                    "environment":"env",
                    "prop":"prp",
                    "vehicle":"vcl",
                    "effect":"vfx",}
    
    taskNamingConv = {"layout":"lay",
                    "lighting":"lit",
                    "compositing":"cmp",
                    "rendering":"rdr",
                    "matte-painting":"dmp",
                    "camera":"cam",
                    "texturing":"tex",
                    "effect":"vfx"}
    
    app_name = "shot manager"
    list_a_name = "sequence"
    list_b_name = "shot"
    list_c_name = "task type"
    list_d_name = "task"   
                        
    def get_list_a(self):
        return core.hksequence.lsDbSeq(self.db, self.project)
        
    def get_list_b(self):
        startkey = u"%s_%s" % ( self.project, self.part_a )
        endkey = u"%s_%s\u0fff" % ( self.project, self.part_a )
        result = dataBase.lsDb(self.db, "shot" , startkey,endkey)
        return result
    
    def get_list_c(self):
        return list(["layout", "lighting", "compositing", "rendering",
                     "matte-painting","camera","texturing","effect"])
    
    def get_list_d(self):
        self.part_c = self.taskNamingConv[self.part_c]
        startkey = u"%s_%s_%s" % ( self.project, self.part_b, self.part_c )
        endkey = u"%s_%s_%s\u0fff" % ( self.project, self.part_b, self.part_c )
        result = dataBase.lsDb(self.db, "shot_task" , startkey,endkey)
        return result


# # Create a Qt application
# app = QtGui.QApplication(sys.argv)
#  
# main=QtGui.QMainWindow()
# setupui=Ui_AssetWindow()
# setupui.setupUi(main)
# main.show()
#  
# # Enter Qt application main loop
# app.exec_()
# sys.exit()
