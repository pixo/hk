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
from pipeline.core import hkrepository
from pushPullUi import UiPush,UiPushLs

#TODO:Ajout icon asset manager en face du nom de projet

class UiCreateOnDb(object):
    
    
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
                
    def setupUi(self, Form, typ = ( "Type", "typ" ) ):
        self.typ = typ
        Form.setObjectName("Form")
        Form.resize(486, 429)
        Form.setWindowTitle("Create on database")
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_lineedit = QtGui.QLabel(Form)
        self.label_lineedit.setObjectName("label_lineedit")
        self.label_lineedit.setText("Create new %s" % self.typ[0])
        self.horizontalLayout.addWidget(self.label_lineedit)
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("create")
        self.pushButton.setToolTip("Make sure to create a description")
        self.pushButton.setEnabled(False)
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_description = QtGui.QLabel(Form)
        self.label_description.setObjectName("label_description")
        self.label_description.setText("Description:")
        self.verticalLayout.addWidget(self.label_description)
        self.plainTextEdit = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.label_status = QtGui.QLabel(Form)
        self.label_status.setObjectName("label_status")
        self.label_status.setText("")
        self.verticalLayout.addWidget(self.label_status)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName(Form)


class UiCreateAsset(UiCreateOnDb):
        
    def pushButtonClicked(self):
        self.label_status.setText("")
        project = utils.system.getProjectName()
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
        doc_id = "%s_%s_%s" % ( project, dbtyp, name )
        doc = core.hkasset.createAsset ( doc_id = doc_id, description = description)
        if doc :
            self.label_status.setText("%s created" % doc_id)
        
class UiCreateTask(UiCreateOnDb):
        
    def pushButtonClicked(self):
        self.label_status.setText("")   
        dbtyp = self.typ[1]
        name = self.lineEdit.text()
        description = self.plainTextEdit.toPlainText()    
        doc_id = "%s_%s" % ( dbtyp, name )
        doc = core.hktask.createTask(doc_id = doc_id, description = description)
        if doc : 
            self.label_status.setText("%s created" % doc_id)
    
    
class UiMainVizor(object):
        
    db = utils.dataBase.getDataBase()
    ccpath = os.path.join(os.getenv( "HK_PIPELINE"), "pipeline","creative")
    project = os.getenv ( "HK_PROJECT" )
        
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
        print itCurr.text(0)
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
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("asset manager")
        MainWindow.resize(600, 700)
        
        self.centralwidget = QtGui.QWidget(MainWindow)
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
        self.labelImage.setMinimumSize(QtCore.QSize(300, 300))
        self.labelImage.setObjectName("labelImage")
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
                    
        self.customUi()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def customUi ( self ):
        
        self.progressBar.setHidden(True)
        self.label.setPixmap ( os.path.join ( self.ccpath, "search.png" ) )
        self.label_proj.setText("""<html><head/><body><p><span style=\" font-size:12pt;
                                    font-weight:600;\">Asset Manager </span><span style=\" font-size:12pt;
                                    \"/><span style=\" font-size:12pt;font-weight:600;
                                    \">:</span><span style=\" font-size:12pt;
                                    \"> '%s'</span></p></body></html>""" % self.project)
        self.label_filter.setPixmap( os.path.join ( self.ccpath, "filter.png" ) )
        empty = os.path.join( os.getenv ( "HK_PIPELINE" ), "pipeline",
                                        "creative", "hk_title_medium.png" )
        self.labelImage.setPixmap( empty )
        self.treeWidget_a.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        self.treeWidget_a.headerItem().setText ( 0, "asset" )
        self.plainTextEdit_description.setReadOnly(True)
        self.createWidget ()
        self.signalConnect ()


class UiAssetVizor(UiMainVizor):
    
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
    ccpath = os.path.join(os.getenv( "HK_PIPELINE"), "pipeline","creative")
    icon_empty = os.path.join ( ccpath, "empty.png" )
    
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
        self.progressBar.setHidden(False)
        item = self.treeWidget_a.currentItem()
        doc_id = item.parent().hkid
        ver = int ( item.text ( 0 ) )
        self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str(ver) ) )
        pull = hkrepository.pull (self.db, doc_id = doc_id, ver = ver ,
                                  progressbar = self.progressBar,
                                  msgbar = self.statusbar.showMessage)
        if pull :
            self.statusbar.showMessage("%s %s pulled" % ( doc_id, str(ver) ))
        
        self.progressBar.setHidden ( True )
    
    def createWorkspace ( self ) :
        item = self.treeWidget_a.currentItem()
        hkrepository.createWorkspace ( self.db, doc_id = item.hkid )

    def contextMenuAsset ( self, item ) :
        menu = QtGui.QMenu ()
        icon_new = QtGui.QIcon ( os.path.join ( self.ccpath, "add.png" ) )
        icon_refresh = QtGui.QIcon ( os.path.join ( self.ccpath, "refresh.png" ) ) 
        action = menu.addAction ( icon_new, 'Create new %s' % self.comboBox_a.currentText() )
        action.triggered.connect (  self.createAsset )       
        refresh = menu.addAction ( icon_refresh, 'Refresh' )
        refresh.triggered.connect ( self.refreshBranch )
        menu.exec_( QtGui.QCursor.pos() )
         
    def contextMenuTask ( self, item ) :
        menu = QtGui.QMenu ()
        icon_new = QtGui.QIcon ( os.path.join ( self.ccpath, "add.png" ) )
        icon_refresh = QtGui.QIcon ( os.path.join ( self.ccpath, "refresh.png" ) ) 
        action = menu.addAction ( icon_new, 'New %s %s fork' % 
                                ( item.parent().text(0), item.text(0) ) )
        action.triggered.connect ( self.createTask )
        refresh = menu.addAction( icon_refresh, 'Refresh' )
        refresh.triggered.connect( self.refreshBranch )
        menu.exec_ ( QtGui.QCursor.pos () )
        
    def contextMenuFork ( self, item ) :
        item = self.treeWidget_a.currentItem ()       
        menu = QtGui.QMenu ()
        icon_new = QtGui.QIcon ( os.path.join ( self.ccpath, "add.png" ) )
        icon_push = QtGui.QIcon ( os.path.join ( self.ccpath, "push.png" ) )
        
        doc_id = item.hkid
        path = core.hkrepository.getWorkspaceFromId ( doc_id = doc_id )
        
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
        icon_pull = QtGui.QIcon ( os.path.join ( self.ccpath, "pull.png" ) )
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
        icon_empty = os.path.join ( self.ccpath, "hk_title.png" )
        item_none = QtGui.QTreeWidgetItem( item )
        item_none.hktype = "none"
        item_none.setText ( 0, "Empty" )
        item_none.setIcon ( 0, QtGui.QIcon(icon_empty ) )
        self.itemExpanded(item)
            
    def itemExpandedSequence ( self, item ) :
        itChildCount = item.childCount ()
        if not (itChildCount > 1) :
            icon_empty = os.path.join ( self.ccpath, "empty.png" )
            startkey = item.hkid.replace("seq","shot")
            shot_ls = utils.dataBase.lsDb ( self.db, "shot", startkey )

            if len(shot_ls)>0:
                item.removeChild(item.child(0))
             
            for shot in shot_ls:
                itemChild = QtGui.QTreeWidgetItem ( item )
                itemChild.setFont(0,item.font(0))
                itemChild.setText (0, shot.split("_")[1])
                icon=os.path.join ( self.ccpath,"shot.png" )
                itemChild.setIcon ( 0, QtGui.QIcon ( icon ) )
                itemChild.hktype = "asset"
                itemChild.hkbranch = shot
                itemChild.hkid = ( "%s_%s" ) % ( self.project, shot )
                 
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
            icon_empty = os.path.join ( self.ccpath, "empty.png" )
            task_dict = self.typ_dict [ self.comboBox_a.currentText () ][1]
            font = item.font(0)
            font.setPointSize ( 9.5 ) 
            if len ( task_dict ) > 0 :
                brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
                item.removeChild ( item.child (0) )
            
            for task in task_dict :
                itemChild = QtGui.QTreeWidgetItem ( item )
                itemChild.setForeground(0,brush)
                itemChild.setText (0, task)
                itemChild.setFont( 0, font)
                icon=os.path.join ( self.ccpath,task + ".png" )
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
            itNameLs = utils.dataBase.lsDb ( self.db, "asset_task", startkey )
            icon_empty = os.path.join ( self.ccpath, "empty.png" )
            
            if len ( itNameLs ) > 0 :
                item.removeChild ( item.child (0) )         
            
            for itName in itNameLs:
                itemChild = QtGui.QTreeWidgetItem ( item )
                itemChild.setText(0,itName.split ( "_" ) [-1] )
                itemChild.hktype = "fork"
                itemChild.hkbranch = item.hkbranch
                icon = os.path.join ( self.ccpath, "fork.png" )
                itemChild.setIcon ( 0, QtGui.QIcon ( icon ) )
                itemChild.versions = dict ()
                itemChild.hkid = "%s_%s" % ( self.project, itName )
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
                    brush = QtGui.QBrush(QtGui.QColor(0, 45, 0))
                    
                    for ver in item.versions :
                        itemChild = QtGui.QTreeWidgetItem ( item )
                        itemChild.setFont ( 0, font )
                        itemChild.setForeground ( 0, brush )
                        icon = os.path.join ( self.ccpath, "file.png" )
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
        screenshot = "%s_%s.jpg" % ( self.project, item.parent().hkid )
        screenshot = os.path.join( path, screenshot )
        
        if not os.path.exists ( screenshot ) :
            empty = os.path.join( os.getenv ( "HK_PIPELINE" ), "pipeline",
                                            "creative", "hk_title_medium.png" )
            self.labelImage.setPixmap( empty )
            
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
        icon = os.path.join ( self.ccpath, "cross.png" )
        self.comboBox_b.addItem ( QtGui.QIcon ( icon ), "No filter" )
        
        for key in task_dict :
            icon = os.path.join ( self.ccpath, key + ".png" )
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
            item = self.comboBox_a.removeItem ( finded )
            
        self.typ = self.typ_dict [ currtext ] [0]
        self.setComboTask ( self.typ_dict [ currtext ] [1] )
        hktype = "sequence"
        
        startkey = "%s" % ( self.project )
        if self.typ != "seq" : 
            startkey = startkey + "_" + self.typ
            hktype = "asset"
            
        obj_ls = utils.dataBase.lsDb ( self.db, self.typ, startkey )
        icon_empty = os.path.join ( self.ccpath, "empty.png" )             
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
            icon = os.path.join ( self.ccpath, currtext + ".png" )
            item_asset.setIcon ( 0, QtGui.QIcon ( icon ) )
            item_asset.hktype = hktype
            item_asset.hkid = "%s_%s" % ( self.project, asset )
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
        icon = os.path.join ( self.ccpath, "combobox.png" )
        self.comboBox_a.addItem ( QtGui.QIcon ( icon ), "Please select ..." )
        for key in self.typ_dict :
            icon = os.path.join ( self.ccpath, key + ".png" )
            self.comboBox_a.addItem ( QtGui.QIcon ( icon ), key )

    

# Create a Qt application
app = QtGui.QApplication(sys.argv)
 
main=QtGui.QMainWindow()
setupui=UiAssetVizor()
setupui.setupUi(main)
main.show()
 
# Enter Qt application main loop
app.exec_()
sys.exit()