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

import sys, os
from PySide import QtCore, QtGui
import pipeline.utils as utils
import pipeline.core as core

CC_PATH = utils.getCCPath()
PROJECT = utils.getProjectName()

class UiPush ( QtGui.QWidget ) :

    
    def searchLineChanged ( self, lineEdit, listWidget ) :
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
                
    def fileLineChanged ( self ) :
        self.searchLineChanged(self.lineEdit_file, self.listWidget_file)
        
    def createWidgetList( self ):
        self.workspace = core.getWorkspaceFromId ( self.db, self.doc_id )
        lsdir = os.listdir ( self.workspace )
        dictpath = dict()
        
        for file in lsdir :
            path = os.path.join ( self.workspace, file )
            
            if os.path.isfile (path) :
                dictpath[file] = path
        self.dictpath=dictpath
                
        lspath = list()
        for key in self.dictpath:
            lspath.append( key )
            
        self.listWidget_file.addItems( lspath )
        self.listWidget_file.setSortingEnabled(True)
            
    def liswidget_clicked(self):
        pass
        
    def pushClicked(self):
        lspush = list ()
        self.progressBar.setHidden ( False )
        self.progressBar.setValue (0)
        
        item = self.listWidget_file.currentItem ()
        lspush.append ( self.dictpath[ item.text () ] )
        description = self.plainTextEdit_description.toPlainText()
        core.push( self.db, self.doc_id, lspush,
                                description, self.progressBar,
                                self.labelStatus.setText )
        
        self.progressBar.setHidden ( True )
        self.labelStatus.setText ( "Done" )
        
    def descriptionChanged( self ):        
        textdoc = self.plainTextEdit_description.document()
        description = textdoc.toPlainText()
        
        if description == "" :
            self.pushButton.setEnabled ( False )
        else :
            self.pushButton.setEnabled ( True )
    
    def checkBoxClicked ( self ):
        print "checked"
        
    def signalConnect(self):
        """ Connect the UI to the Ui_AssetWindow methods """
        self.pushButton.clicked.connect( self.pushClicked )
        self.lineEdit_file.textChanged.connect( self.fileLineChanged )
        self.plainTextEdit_description.textChanged.connect( self.descriptionChanged )
        self.listWidget_file.clicked.connect( self.liswidget_clicked)
        self.checkBox.clicked.connect(self.checkBoxClicked)
        
    def setupUi( self, Form, db, doc_id):
        Form.setObjectName("Form")
        Form.resize(600, 600)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout_center = QtGui.QHBoxLayout()
        self.horizontalLayout_center.setObjectName("horizontalLayout_center")
        self.verticalLayout_file = QtGui.QVBoxLayout()
        self.verticalLayout_file.setObjectName("verticalLayout_file")
        self.label_proj = QtGui.QLabel(Form)
        self.label_proj.setObjectName("label_proj")
        self.verticalLayout_file.addWidget(self.label_proj)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox = QtGui.QCheckBox(Form)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.label_search = QtGui.QLabel(Form)
        self.label_search.setMaximumSize(QtCore.QSize(16, 16))
        self.label_search.setObjectName("label_search")
        self.horizontalLayout.addWidget(self.label_search)
        self.lineEdit_file = QtGui.QLineEdit(Form)
        self.lineEdit_file.setObjectName("lineEdit_file")
        self.horizontalLayout.addWidget(self.lineEdit_file)
        self.verticalLayout_file.addLayout(self.horizontalLayout)
        self.listWidget_file = QtGui.QListWidget(Form)
        self.listWidget_file.setMinimumSize(QtCore.QSize(300, 0))
        self.listWidget_file.setObjectName("listWidget_file")
        self.verticalLayout_file.addWidget(self.listWidget_file)
        self.horizontalLayout_center.addLayout(self.verticalLayout_file)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_description = QtGui.QLabel(Form)
        self.label_description.setAlignment(QtCore.Qt.AlignCenter)
        self.label_description.setObjectName("label_description")
        self.verticalLayout.addWidget(self.label_description)
        self.plainTextEdit_description = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit_description.setMinimumSize(QtCore.QSize(300, 0))
        self.plainTextEdit_description.setObjectName("plainTextEdit_description")
        self.verticalLayout.addWidget(self.plainTextEdit_description)
        self.horizontalLayout_center.addLayout(self.verticalLayout)
        self.verticalLayout_main.addLayout(self.horizontalLayout_center)
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setMinimumSize(QtCore.QSize(550, 0))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_bottom.addWidget(self.progressBar)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_bottom.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_bottom.addWidget(self.pushButton)
        self.verticalLayout_main.addLayout(self.horizontalLayout_bottom)
        self.labelStatus = QtGui.QLabel(Form)
        self.labelStatus.setText("")
        self.labelStatus.setObjectName("labelStatus")
        self.verticalLayout_main.addWidget(self.labelStatus)
        self.verticalLayout_2.addLayout(self.verticalLayout_main)
        
        #Default setup
        self.db = db
        self.doc_id = doc_id
        Form.setWindowTitle ( "Asset Pusher" )
        
        self.label_proj.setText ( """<html><head/><body><p><span style=\" 
                                font-size:12pt; font-weight:600;\">Asset Push :
                                </span><span style=\" font-size:12pt;
                                \"> '%s'</span></p></body></html>""" % self.doc_id )
        
        self.label_description.setText ( """<html><head/><body><p><span style=
                                    \" font-weight:600;\">Description</span>
                                    </p></body></html>""" )
        
        self.listWidget_file.setSortingEnabled ( True )
        self.checkBox.setIcon( QtGui.QIcon ( os.path.join ( CC_PATH, "all.png" )))
        self.checkBox.setVisible(False)
        self.progressBar.setHidden(True)
        self.label_search.setPixmap( os.path.join ( CC_PATH, "search.png" ) )
        self.pushButton.setText("Push")
        self.pushButton.setDisabled(True)
        icon_push = QtGui.QIcon(os.path.join(CC_PATH,"push.png"))
        self.pushButton.setIcon(icon_push)
        self.createWidgetList()
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName(Form)
           
class UiPushLs(UiPush):
    
    def checkBoxClicked ( self ):
        checkState = self.checkBox.checkState()
        for i in range( 0, self.listWidget_file.count () ):
            self.listWidget_file.item(i).setCheckState( checkState )
    
    def createWidgetList( self ):
        self.checkBox.setVisible(True)
        self.workspace = core.getWorkspaceFromId(self.db,
                                                            self.doc_id)        
        self.dictpath = utils.lsSeq(self.workspace)
        
        lspath = list()
        for key in self.dictpath:
            lspath.append( key )
            
        self.listWidget_file.addItems( lspath )
        
        font = QtGui.QFont ()
        font.setPointSize ( 9 )
        font.setWeight ( 75 )
        font.setBold ( True )
        
        for i in range( 0, self.listWidget_file.count() ):
            item = self.listWidget_file.item(i)
            item.setCheckState( QtCore.Qt.Unchecked )
            if item.text().find(os.sep) > -1:
                item.setFont(font)
            
    def pushClicked(self):
        lspush = list()
        self.progressBar.setHidden(False)
        self.progressBar.setValue(0)
        
        for i in range( 0, self.listWidget_file.count() ):
            item = self.listWidget_file.item(i)
            
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                lspush.extend( self.dictpath[item.text()] )
                
        textdoc = self.plainTextEdit_description.document()
        description = textdoc.toPlainText()
        core.push( self.db, self.doc_id, lspush,
                                description, self.progressBar,
                                self.labelStatus.setText, rename = False)
        self.progressBar.setHidden(True)
        self.labelStatus.setText ( "Done")
        
class UiPush3dPack ( QtGui.QWidget ) :
    
    
    screenshot = os.path.join ( CC_PATH, "hk_title_medium.png" )
    
    def __init__( self, parent = None, db = None, doc_id = "", item = "" ):
        
        super ( UiPush3dPack, self ).__init__( parent )
        self.setObjectName("Form")
        self.resize(394, 666)
        self.verticalLayout_2 = QtGui.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_launcher = QtGui.QLabel(self)
        self.label_launcher.setMaximumSize(QtCore.QSize(21, 21))
        self.label_launcher.setText("")
        self.label_launcher.setObjectName("label_launcher")
        self.horizontalLayout_2.addWidget(self.label_launcher)
        self.label_proj = QtGui.QLabel(self)
        self.label_proj.setObjectName("label_proj")
        self.horizontalLayout_2.addWidget(self.label_proj)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.labelImage = QtGui.QLabel(self)
        self.labelImage.setMinimumSize(QtCore.QSize(300, 300))
        self.labelImage.setText("")
        self.labelImage.setObjectName("labelImage")
        self.verticalLayout_3.addWidget(self.labelImage)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.screenshotButton = QtGui.QPushButton(self)
        self.screenshotButton.setObjectName("screenshotButton")
        self.horizontalLayout.addWidget(self.screenshotButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_comments = QtGui.QLabel(self)
        self.label_comments.setAlignment(QtCore.Qt.AlignCenter)
        self.label_comments.setObjectName("label_comments")
        self.verticalLayout_3.addWidget(self.label_comments)
        self.plainTextEdit_comments = QtGui.QPlainTextEdit(self)
        self.plainTextEdit_comments.setMinimumSize(QtCore.QSize(300, 0))
        self.plainTextEdit_comments.setObjectName("plainTextEdit_comments")
        self.verticalLayout_3.addWidget(self.plainTextEdit_comments)
        self.verticalLayout_main.addLayout(self.verticalLayout_3)
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setMinimumSize(QtCore.QSize(300, 0))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_bottom.addWidget(self.progressBar)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_bottom.addItem(spacerItem1)
        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_bottom.addWidget(self.pushButton)
        self.verticalLayout_main.addLayout(self.horizontalLayout_bottom)
        self.labelStatus = QtGui.QLabel(self)
        self.labelStatus.setText("")
        self.labelStatus.setObjectName("labelStatus")
        self.verticalLayout_main.addWidget(self.labelStatus)
        self.verticalLayout_2.addLayout(self.verticalLayout_main)
         
        self.item = item
        self.db = db
        self.doc_id = doc_id
        self.setupUi()
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setupUi(self):
        self.setWindowTitle("Asset Push")
        
        self.label_proj.setText( """<html><head/><body><p><span style=\" font-size:12pt;
                                font-weight:600;\">Push Asset :</span><span style=\"
                                font-size:12pt;\"> '%s'</span></p></body></html>""" % self.doc_id )
                
        self.label_comments.setText("""<html><head/><body><p><span style=\" font-weight:600;
                                    \">User comments</span></p></body></html>""")
        
        self.progressBar.setHidden ( True )
        
        self.label_launcher.setPixmap(os.path.join ( CC_PATH, "%s.png" % self.launcher ))
        self.pushButton.setText ( "Push" )
        icon_push = QtGui.QIcon ( os.path.join ( CC_PATH, "push.png" ) )
        self.pushButton.setIcon ( icon_push )
        self.pushButton.setDisabled ( True )
        
        self.screenshotButton.setText( "Screenshot" )
        icon_push_2 = QtGui.QIcon ( os.path.join ( CC_PATH, "screenshot.png" ) )
        self.screenshotButton.setIcon ( icon_push_2 )

        self.labelImage.setPixmap(self.screenshot)
        
    def signalConnect(self):
        self.pushButton.clicked.connect( self.pushClicked )
        self.screenshotButton.clicked.connect( self.screenshotClicked )
        self.plainTextEdit_comments.textChanged.connect( self.commentsChanged )
                
    def pushClicked ( self ) :
        print self.doc_id
    
    def screenshotClicked ( self ) :
        print "screenshot"

    def commentsChanged ( self ) :
        textdoc = self.plainTextEdit_comments.document()
        description = textdoc.toPlainText()
        
        if description == "" :
            self.pushButton.setEnabled ( False )
        else :
            self.pushButton.setEnabled ( True )
            
class UiCreateOnDb ( QtGui.QWidget ) :
    
    
    def pushButtonClicked(self):
        print "push button clicked"
        
    def plainTextEditChanged( self ):        
        descriptions = self.plainTextEdit.toPlainText()
        
        if descriptions == "" :
            self.pushButton.setEnabled(False)
        else :
            self.pushButton.setEnabled(True) 
    
    def signalConnect(self):
        self.pushButton.clicked.connect ( self.pushButtonClicked )
        self.plainTextEdit.textChanged.connect ( self.plainTextEditChanged )
                
                
    def __init__(self, parent=None, typ = ( "Type", "typ" )):
        super(UiMainManager, self).__init__(parent)
        
        self.typ = typ
        self.setObjectName("Form")
        self.resize(486, 429)
        self.setWindowTitle("Create on database")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_lineedit = QtGui.QLabel(self)
        self.label_lineedit.setObjectName("label_lineedit")
        self.label_lineedit.setText("Create new %s" % self.typ[0])
        self.horizontalLayout.addWidget(self.label_lineedit)
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("create")
        self.pushButton.setToolTip("Make sure to create a description")
        self.pushButton.setEnabled(False)
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_description = QtGui.QLabel(self)
        self.label_description.setObjectName("label_description")
        self.label_description.setText("Description:")
        self.verticalLayout.addWidget(self.label_description)
        self.plainTextEdit = QtGui.QPlainTextEdit(self)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.label_status = QtGui.QLabel(self)
        self.label_status.setObjectName("label_status")
        self.label_status.setText("")
        self.verticalLayout.addWidget(self.label_status)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName(self)


class UiCreateAsset(UiCreateOnDb):
        
    def pushButtonClicked(self):
        self.label_status.setText("")
        dbtyp = self.typ[1]
        name = self.lineEdit.text()
        
        if name.find("_") >= 0:
            msg = "Can't create asset '%s' name shouldn't contain underscore"
            self.label_status.setText(msg % name)
            return
        
        if name.find(" ") >= 0:
            msg = "Can't create asset '%s' name shouldn't contain space"
            self.label_status.setText(msg % name)
            return
            
        description = self.plainTextEdit.toPlainText()    
        doc_id = "%s_%s_%s" % ( PROJECT, dbtyp, name )
        doc = core.createAsset ( doc_id = doc_id, description = description)
        if doc :
            self.label_status.setText("%s created" % doc_id)
        
class UiCreateTask(UiCreateOnDb):
        
    def pushButtonClicked(self):
        self.label_status.setText("")   
        dbtyp = self.typ[1]
        name = self.lineEdit.text()
        description = self.plainTextEdit.toPlainText()    
        doc_id = "%s_%s" % ( dbtyp, name )
        doc = core.createTask(doc_id = doc_id, description = description)
        if doc : 
            self.label_status.setText("%s created" % doc_id)
    
    
class UiMainManager(QtGui.QMainWindow):
        
    db = utils.getDataBase()
    launcher = "terminal"
        
    def searchLine_a_Changed ( self, lineEdit, treeWidget ) :
        it = QtGui.QTreeWidgetItemIterator(treeWidget)
        text = self.lineEdit_a.text()
        
        while it.value () :
            item = it.value()
            if not item.parent() :
                if filter != "" :
                    itemtext = item.text(0)
                    if itemtext.find(text)>=0:
                        item.setHidden (False)
                    else :
                        item.setHidden (True)
                else :
                    item.setHidden (False)       
            it.next()
            
    def searchLine_b_Changed ( self, lineEdit, treeWidget ) :
        it = QtGui.QTreeWidgetItemIterator(treeWidget)
        text = self.lineEdit_b.text()
        
        while it.value () :
            item = it.value()
            if item.hktype == "fork" :
                if filter != "" :
                    itemtext = item.text(0)
                    if itemtext.find(text) >=0 :
                        item.setHidden ( False )
                    else :
                        item.setHidden ( True )
                else :
                    item.setHidden ( False )       
            it.next()
                
    def searchLine_a ( self ) :
        self.searchLine_a_Changed(self.lineEdit_a, self.treeWidget_a)
        
    def searchLine_b ( self ) :
        self.searchLine_b_Changed(self.lineEdit_b, self.treeWidget_a)
                
    def itemExpanded(self,item):
        print item.text(0)
        
    def createWidget(self):
        pass
    
    def comboTaskChange(self):
        pass
    
    def comboTypeChange(self):
        print self.comboBox_a.currentText()      
        
    def itemClicked(self, item):
        print "item clicked"
                
    def contextMenuEvent(self):
        itCurr=self.treeWidget_a.currentItem()
        menu = QtGui.QMenu()
        menu.addAction('Add')
        menu.addAction('Delete')
        menu.exec_(QtGui.QCursor.pos())
        
    def signalConnect(self):
        self.comboBox_a.currentIndexChanged.connect(self.comboTypeChange)
        self.comboBox_b.currentIndexChanged.connect(self.comboTaskChange)
        self.lineEdit_a.textChanged.connect(self.searchLine_a)
        self.lineEdit_b.textChanged.connect(self.searchLine_b)
        self.treeWidget_a.itemExpanded.connect(self.itemExpanded)
        self.treeWidget_a.itemClicked.connect(self.itemClicked)
        self.treeWidget_a.customContextMenuRequested.connect(self.contextMenuEvent)
        
    def __init__(self, parent=None):
        super(UiMainManager, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.setWindowTitle("asset manager")
        self.resize(600, 700)
        
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_sys = QtGui.QLabel(self.centralwidget)
        self.label_sys.setMaximumSize(QtCore.QSize(21, 21))
        self.label_sys.setObjectName("label_sys")
        self.horizontalLayout_6.addWidget(self.label_sys)
        self.label_proj = QtGui.QLabel(self.centralwidget)
        self.label_proj.setObjectName("label_proj")
        self.horizontalLayout_6.addWidget(self.label_proj)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_filter = QtGui.QLabel(self.centralwidget)
        self.label_filter.setEnabled(True)
        self.label_filter.setMaximumSize(QtCore.QSize(16, 16))
        self.label_filter.setObjectName("label_filter")
        self.horizontalLayout_4.addWidget(self.label_filter)
        self.comboBox_a = QtGui.QComboBox(self.centralwidget)
        self.comboBox_a.setObjectName("comboBox_a")
        self.horizontalLayout_4.addWidget(self.comboBox_a)
        self.comboBox_b = QtGui.QComboBox(self.centralwidget)
        self.comboBox_b.setObjectName("comboBox_b")
        self.horizontalLayout_4.addWidget(self.comboBox_b)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(16, 16))
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.lineEdit_a = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_a.setObjectName("lineEdit_a")
        self.horizontalLayout_5.addWidget(self.lineEdit_a)
        self.lineEdit_b = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_b.setObjectName("lineEdit_b")
        self.horizontalLayout_5.addWidget(self.lineEdit_b)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.treeWidget_a = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget_a.setAlternatingRowColors(True)
        self.treeWidget_a.setObjectName("treeWidget_a")
        self.verticalLayout.addWidget(self.treeWidget_a)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelImage = QtGui.QLabel(self.centralwidget)
        self.labelImage.setMinimumSize ( QtCore.QSize ( 300, 300 ) )
        self.labelImage.setObjectName ( "labelImage" )
        self.verticalLayout_2.addWidget(self.labelImage)
        self.plainTextEdit_description = QtGui.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_description.setObjectName("plainTextEdit_description")
        self.verticalLayout_2.addWidget(self.plainTextEdit_description)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_main.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.verticalLayout_main.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_main)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
                    
        self.customUi ()
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def customUi ( self ):
        self.progressBar.setHidden(True)
        self.label_sys.setPixmap(os.path.join ( CC_PATH, "%s.png" % self.launcher ))
        self.label.setPixmap ( os.path.join ( CC_PATH, "search.png" ) )
        self.label_proj.setText("""<html><head/><body><p><span style=\" font-size:12pt;
                                    font-weight:600;\">Asset Manager </span><span style=\" font-size:12pt;
                                    \"/><span style=\" font-size:12pt;font-weight:600;
                                    \">:</span><span style=\" font-size:12pt;
                                    \"> '%s'</span></p></body></html>""" % PROJECT )
        self.label_filter.setPixmap( os.path.join ( CC_PATH, "filter.png" ) )
        empty = os.path.join( CC_PATH, "hk_title_medium.png" )
        self.labelImage.setPixmap( empty )
        self.treeWidget_a.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        self.treeWidget_a.headerItem().setText ( 0, "asset" )
        self.plainTextEdit_description.setReadOnly(True)
        self.createWidget ()
        self.signalConnect ()


class UiAssetManager(UiMainManager):
    
    
    pushls = ("texture",
              "render",
              "compout")
    
    effect_task = {
                   "particle" : "pcl",
                   "fluid" : "fld",
                   "dynamic" : "dyn"
                   }
    
    material_task = {
                     "shader" : "shd",
                     "override" : "ovr"
                     }
        
    shot_task =   {
                   "layout" : "lay",
                   "lighting" : "lit",
                   "render" : "rdr",
                   "compositing" : "cmp",
                   "compout" : "out",
                   "matte-paint" : "dmp",
                   "camera" : "cam",
                   "effect" : "vfx"
                   }
    
    sequence_task = shot_task
        
    asset_task = {
                  "surface" : "sur",
                  "model" : "mod",
                  "texture" : "tex",
                  "rig" : "rig",
                  "sculpt" : "sct",
                  "retopo" : "rtp"
                  }
    
    typ_dict = {
                "character": ( "chr", asset_task ),
                "vehicle": ( "vcl", asset_task ),
                "prop": ( "prp", asset_task ),
                "environment": ( "env", asset_task ),
                "effect" : ( "vfx", effect_task ),
                "material" : ( "mtl", material_task ),
                "shot" : ( "shot", shot_task ),
                "sequence" : ( "seq", sequence_task )
                }
    
    icon_empty = os.path.join ( CC_PATH, "empty.png" )
    
    def createAsset ( self ) :
        
        self.createAssetWin = UiCreateAsset()
        nicename = self.comboBox_a.currentText()
        typ = self.typ_dict[nicename][0]
        self.createAssetWidget=QtGui.QWidget()
        self.createAssetWin.setupUi(self.createAssetWidget, (nicename, typ) )
        self.createAssetWidget.show()
        
    def createTask ( self ) :
        item = self.treeWidget_a.currentItem()
        doc_id = item.hkid
        nicename = doc_id
        
        self.createTaskWin = UiCreateTask()   
        self.createTaskWidget=QtGui.QWidget()
        self.createTaskWin.setupUi(self.createTaskWidget, (nicename, doc_id) )
        self.createTaskWidget.show()
        
    def pushVersion ( self ) :
        item = self.treeWidget_a.currentItem()
        task = item.parent().text(0) 
        doc_id = item.hkid
        
        if task in self.pushls:
            self.pushVersionWin = UiPushLs ()
        else:
            self.pushVersionWin = UiPush ()

        self.pushVersionWidget = QtGui.QWidget()
        self.pushVersionWin.setupUi ( self.pushVersionWidget, self.db, doc_id )
        self.pushVersionWidget.show ()
    
    def pullVersion ( self ) :
        self.progressBar.setHidden ( False )
        item = self.treeWidget_a.currentItem ()
        doc_id = item.parent().hkid
        ver = int ( item.text ( 0 ) )
        self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str(ver) ) )
        pull = core.pull (self.db, doc_id = doc_id, ver = ver ,
                                  progressbar = self.progressBar,
                                  msgbar = self.statusbar.showMessage)
        if pull :
            self.statusbar.showMessage("%s %s pulled" % ( doc_id, str(ver) ))
        
        self.progressBar.setHidden ( True )
    
    def createWorkspace ( self ) :
        item = self.treeWidget_a.currentItem()
        core.createWorkspace ( self.db, doc_id = item.hkid )

    def contextMenuAsset ( self, item ) :
        menu = QtGui.QMenu ()
        icon_new = QtGui.QIcon ( os.path.join ( CC_PATH, "add.png" ) )
        icon_refresh = QtGui.QIcon ( os.path.join ( CC_PATH, "refresh.png" ) ) 
        action = menu.addAction ( icon_new, 'Create new %s' % self.comboBox_a.currentText() )
        action.triggered.connect (  self.createAsset )       
        refresh = menu.addAction ( icon_refresh, 'Refresh' )
        refresh.triggered.connect ( self.refreshBranch )
        menu.exec_( QtGui.QCursor.pos() )
         
    def contextMenuTask ( self, item ) :
        menu = QtGui.QMenu ()
        icon_new = QtGui.QIcon ( os.path.join ( CC_PATH, "add.png" ) )
        icon_refresh = QtGui.QIcon ( os.path.join ( CC_PATH, "refresh.png" ) ) 
        action = menu.addAction ( icon_new, 'New %s %s fork' % 
                                ( item.parent().text(0), item.text(0) ) )
        action.triggered.connect ( self.createTask )
        refresh = menu.addAction( icon_refresh, 'Refresh' )
        refresh.triggered.connect( self.refreshBranch )
        menu.exec_ ( QtGui.QCursor.pos () )
        
    def contextMenuFork ( self, item ) :
        item = self.treeWidget_a.currentItem ()       
        menu = QtGui.QMenu ()
        icon_new = QtGui.QIcon ( os.path.join ( CC_PATH, "add.png" ) )
        icon_push = QtGui.QIcon ( os.path.join ( CC_PATH, "push.png" ) )
        
        doc_id = item.hkid
        path = core.getWorkspaceFromId ( doc_id = doc_id )
        
        if os.path.exists ( path ) :
            action = menu.addAction ( icon_push, 'Push a new %s %s %s version' % 
                                      ( item.parent().parent().text(0),
                                        item.parent().text(0), item.text(0)) )
            action.triggered.connect ( self.pushVersion )
        else:
            action = menu.addAction ( icon_new, 'Create workspace' )
            action.triggered.connect ( self.createWorkspace )
                    
        menu.exec_ ( QtGui.QCursor.pos () )
        
    def contextMenuVersion ( self, item ) :
        menu = QtGui.QMenu ()
        icon_pull = QtGui.QIcon ( os.path.join ( CC_PATH, "pull.png" ) )
        action = menu.addAction ( icon_pull, 'Pull version %s' % item.text (0) )
        action.triggered.connect ( self.pullVersion )
        menu.exec_( QtGui.QCursor.pos () )
        
    def contextMenuEvent(self):
        item = self.treeWidget_a.currentItem ()
        if not item:
            self.contextMenuAsset ( item )
            
        else :
            item_type = item.hktype
            
            if item_type == "sequence" :
                print "ma bite"
                
            if item_type == "asset" :
                self.contextMenuAsset ( item )
                
            elif item_type == "task" :
                self.contextMenuTask ( item )
                
            elif item_type == "fork" :
                self.contextMenuFork ( item )
                
            elif item_type == "version" :
                self.contextMenuVersion ( item )
                
            elif item_type == "None" :
                pass
            
    def refreshBranch ( self ):
        item = self.treeWidget_a.currentItem ()
        item.takeChildren()
        icon_empty = os.path.join ( CC_PATH, "hk_title.png" )
        item_none = QtGui.QTreeWidgetItem( item )
        item_none.hktype = "none"
        item_none.setText ( 0, "Empty" )
        item_none.setIcon ( 0, QtGui.QIcon(icon_empty ) )
        self.itemExpanded(item)
            
    def itemExpandedSequence ( self, item ) :
        itChildCount = item.childCount ()
        if not (itChildCount > 1) :
            icon_empty = os.path.join ( CC_PATH, "empty.png" )
            startkey = item.hkid.replace("seq","shot")
            shot_ls = utils.lsDb ( self.db, "shot", startkey )

            if len(shot_ls)>0:
                item.removeChild(item.child(0))
             
            for shot in shot_ls:
                itemChild = QtGui.QTreeWidgetItem ( item )
                itemChild.setFont(0,item.font(0))
                itemChild.setText (0, shot.split("_")[1])
                icon=os.path.join ( CC_PATH,"shot.png" )
                itemChild.setIcon ( 0, QtGui.QIcon ( icon ) )
                itemChild.hktype = "asset"
                itemChild.hkbranch = shot
                itemChild.hkid = ( "%s_%s" ) % ( PROJECT, shot )
                 
                item_none = QtGui.QTreeWidgetItem( itemChild )
                item_none.hktype = "none"
                item_none.hkbranch = shot
                item_none.setText ( 0, "Empty" )
                item_none.setIcon ( 0, QtGui.QIcon(icon_empty ) )
                 
            order=QtCore.Qt.AscendingOrder    
            item.sortChildren ( 0, order )
            
            if ( item.childCount () > 1 ) and ( item.child(0).hktype == "none" ) :
                item.removeChild ( item.child(0) )
        self.filterTree ()       
            
    def itemExpandedAsset ( self, item ) :
         
        if item.child(0).hktype == "none" :
            icon_empty = os.path.join ( CC_PATH, "empty.png" )
            task_dict = self.typ_dict [ self.comboBox_a.currentText () ][1]
            font = item.font(0)
            font.setPointSize ( 9.5 ) 
            if len ( task_dict ) > 0 :
                brush = QtGui.QBrush( QtGui.QColor ( 150, 150, 150 ) )
                item.removeChild ( item.child (0) )
            
            for task in task_dict :
                itemChild = QtGui.QTreeWidgetItem ( item )
                itemChild.setForeground(0,brush)
                itemChild.setText (0, task)
                itemChild.setFont( 0, font)
                icon=os.path.join ( CC_PATH,task + ".png" )
                itemChild.setIcon ( 0, QtGui.QIcon ( icon ) )
                itemChild.hktype = "task"
                itemChild.hkbranch = task
                itemChild.hkid = ( "%s_%s" ) % ( item.hkid, task_dict[task] )
                
                item_none = QtGui.QTreeWidgetItem( itemChild )
                item_none.hktype = "none"
                item_none.hkbranch = task
                item_none.setText ( 0, "Empty" )
                item_none.setIcon ( 0, QtGui.QIcon(icon_empty ) )
                
            order=QtCore.Qt.AscendingOrder    
            item.sortChildren(0, order)
            
        self.filterTree()
            
    def itemExpandedTask ( self, item ) :
        if item.child(0).hktype == "none" :
            task_dict = self.typ_dict [ self.comboBox_a.currentText () ][1]
            task = task_dict [ item.text (0) ]
            parentId = item.parent().hkid
            startkey = "%s_%s" % ( parentId, task )
            itNameLs = utils.lsDb ( self.db, "asset_task", startkey )
            icon_empty = os.path.join ( CC_PATH, "empty.png" )
            
            if len ( itNameLs ) > 0 :
                item.removeChild ( item.child (0) )         
            
            for itName in itNameLs:
                itemChild = QtGui.QTreeWidgetItem ( item )
                itemChild.setText(0,itName.split ( "_" ) [-1] )
                itemChild.hktype = "fork"
                itemChild.hkbranch = item.hkbranch
                icon = os.path.join ( CC_PATH, "fork.png" )
                itemChild.setIcon ( 0, QtGui.QIcon ( icon ) )
                itemChild.versions = dict ()
                itemChild.hkid = "%s_%s" % ( PROJECT, itName )
                itemChild.dbdoc = self.db [ itemChild.hkid ]
                
                item_none = QtGui.QTreeWidgetItem ( itemChild )
                item_none.hktype = "none"
                item_none.hkbranch = "empty"
                item_none.setText ( 0, "Empty" )
                item_none.setIcon ( 0, QtGui.QIcon ( icon_empty ) )
                item_none.setText ( 0, "Empty" )
                item_none.setHidden = True

            order = QtCore.Qt.AscendingOrder    
            item.sortChildren ( 0, order )
        
    def itemExpandedFork ( self, item ) :
        
        if item.child(0).hktype == "none" :
            font = QtGui.QFont ()
            font.setItalic ( True )
#             font.setPointSize(8.7)
#             font.setBold(True)
            if item.versions == dict ():
                item.versions = item.dbdoc [ "versions" ]
                if len ( item.versions ) > 0:
                    brush = QtGui.QBrush ( QtGui.QColor ( 128, 128, 128 ) )
                    
                    for ver in item.versions :
                        itemChild = QtGui.QTreeWidgetItem ( item )
                        itemChild.setFont ( 0, font )
                        itemChild.setForeground ( 0, brush )
                        icon = os.path.join ( CC_PATH, "file.png" )
                        itemChild.setIcon ( 0, QtGui.QIcon ( icon ) )
                        itemChild.setText ( 0, "%03d" % float ( ver ) )
                        itemChild.hkbranch = item.hkbranch
                        itemChild.hktype = "version"
                        itemChild.info = item.versions [ ver ]
                        
                    order = QtCore.Qt.DescendingOrder
                    item.sortChildren ( 0, order )
                    item.removeChild ( item.child ( 0 ) )
        
    def itemExpanded ( self, item ) :
        
        if item.hktype == "sequence" :
            self.itemExpandedSequence ( item )
            
        elif item.hktype == "asset":
            self.itemExpandedAsset ( item )
            
        elif item.hktype == "task" :
            self.itemExpandedTask ( item )
            
        elif item.hktype == "fork" :
            self.itemExpandedFork ( item )
                            
    def itemClickedVersion( self, item ):
                
        """Set the data to the plain text"""
        creator  = "Creator:\t%s\n" % item.info [ 'creator' ]
        created  = "\nCreated:\t%s\n" % item.info [ 'created' ]
        description = "\nDescription:\n\t%s\n" % item.info [ 'description' ]
        
        path = os.path.expandvars( item.info["path"] )
        pathinfo = "\nPath:\n\t%s\n" % os.path.expandvars( item.info [ "path" ] )
        
        files ="\n\t".join ( map ( str, item.info [ "files" ] ) )
        files = "\nFiles:\n\t%s\n" % files
         
        infos = creator + created + description + pathinfo + files
        self.plainTextEdit_description.setPlainText ( infos )
        
        """Set the screenshot"""
        screenshot = "%s.jpg" % item.parent().hkid
        screenshot = os.path.join( path, screenshot )
        
        if not os.path.exists ( screenshot ) :
            screenshot = os.path.join( CC_PATH, "hk_title_medium.png" )
            
        self.labelImage.setPixmap( screenshot )
            
    def itemClickedFork( self, item ):
                
        """Set the data to the plain text"""
        creator  = "Creator:\t%s\n" % item.dbdoc [ 'creator' ]
        created  = "\nCreated:\t%s\n" % item.dbdoc [ 'created' ]
        state = "\nState:\t%s\n" % item.dbdoc [ 'state' ]
        description = "\nDescription:\n\t%s\n" % item.dbdoc [ 'description' ]
          
        infos = creator + created + state + description
        self.plainTextEdit_description.setPlainText ( infos )  
        
    def itemClicked(self, item):
       
        if item.hktype == "fork":
            self.itemClickedFork ( item )
            
        elif item.hktype == "version" :
            self.itemClickedVersion ( item )
            
        else:
            self.plainTextEdit_description.setPlainText ( "" )
            
        if hasattr(item, "hkid") :
            self.statusbar.showMessage(item.hkid)
        else:
            self.statusbar.showMessage("")
            
    def setComboTask ( self, task_dict ) :
        self.comboBox_b.clear ()
        icon = os.path.join ( CC_PATH, "cross.png" )
        self.comboBox_b.addItem ( QtGui.QIcon ( icon ), "No filter" )
        
        for key in task_dict :
            icon = os.path.join ( CC_PATH, key + ".png" )
            self.comboBox_b.addItem ( QtGui.QIcon ( icon ), key )
        
    def filterTree ( self ):
        currFilter = self.comboBox_b.currentText ()            
        it = QtGui.QTreeWidgetItemIterator ( self.treeWidget_a )
        while it.value () :
            item = it.value ()                
            if not item.hkbranch == "root":
                if item.parent ().hktype == "asset":
                    if item.parent ().isExpanded ():
                        if ( item.hkbranch == currFilter ) or ( currFilter == "No filter" ) :
                            item.setHidden ( False )
                        else:
                            item.setHidden(True)
            it.next()
            
    def comboTypeChange(self):                    
        currtext = self.comboBox_a.currentText ()
        finded = self.comboBox_a.findText ( "Please select ..." )
        
        if finded >= 0 : 
            self.comboBox_a.removeItem ( finded )
            
        self.typ = self.typ_dict [ currtext ] [0]
        self.setComboTask ( self.typ_dict [ currtext ] [1] )
        hktype = "sequence"
        
        startkey = "%s" % ( PROJECT )
        if self.typ != "seq" : 
            startkey = startkey + "_" + self.typ
            hktype = "asset"
            
        obj_ls = utils.lsDb ( self.db, self.typ, startkey )
        icon_empty = os.path.join ( CC_PATH, "empty.png" )             
        self.treeWidget_a.clear ()
                
        font = QtGui.QFont ()
        font.setPointSize ( 10 )
        font.setWeight ( 75 )
        font.setItalic ( False )
        font.setBold ( True )
                 
        for asset in obj_ls :
            item_asset = QtGui.QTreeWidgetItem ( self.treeWidget_a )
            item_asset.setFont ( 0, font )
            item_asset.setText ( 0, "%s" % asset.split ( "_" ) [-1] )
            icon = os.path.join ( CC_PATH, currtext + ".png" )
            item_asset.setIcon ( 0, QtGui.QIcon ( icon ) )
            item_asset.hktype = hktype
            item_asset.hkid = "%s_%s" % ( PROJECT, asset )
            item_asset.hkbranch = "root"
            
            item_none = QtGui.QTreeWidgetItem ( item_asset )
            item_none.setIcon ( 0, QtGui.QIcon ( icon_empty ))
            item_none.setText ( 0, "Empty" )
            item_none.hktype = "none"
            item_none.hkbranch = "empty"

            
        self.filterTree ()
                
    def comboTaskChange ( self ) :
        self.filterTree ()
        
    def createWidget ( self ) :
        """Create the type combobox"""
        icon = os.path.join ( CC_PATH, "combobox.png" )
        self.comboBox_a.addItem ( QtGui.QIcon ( icon ), "Please select ..." )
        
        for key in self.typ_dict :
            icon = os.path.join ( CC_PATH, key + ".png" )
            self.comboBox_a.addItem ( QtGui.QIcon ( icon ), key )
                
def systemAM():
    # Create a Qt application
    app = QtGui.QApplication ( sys.argv )    
    main = UiAssetManager()
    main.show()
    app.exec_()
    sys.exit()
    
# systemAM()