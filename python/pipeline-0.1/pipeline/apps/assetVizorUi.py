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

class UiCreateOnDb(object):
    
    
    def pushButtonClicked(self):
        print "push button clicked"
        
    def plainTextEditChanged( self ):        
        comments = self.plainTextEdit.toPlainText()
        
        if comments == "" :
            self.pushButton.setEnabled(False)
        else :
            self.pushButton.setEnabled(True) 
    
    def signalConnect(self):
        self.pushButton.clicked.connect ( self.pushButtonClicked )
        self.plainTextEdit.textChanged.connect ( self.plainTextEditChanged )
                
    def setupUi(self, Form, typ = ("Type","typ")):
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
        project = utils.system.getProjectName()
        dbtyp = self.typ[1]
        name = self.lineEdit.text()
        description = self.plainTextEdit.toPlainText()    
        asset_id = "%s_%s_%s" % ( project, dbtyp, name )
        core.hkasset.createAsset(doc_id = asset_id, description = description)
        self.label_status.setText("%s created" % asset_id)
        
class UiCreateTask(UiCreateOnDb):
        
    def pushButtonClicked(self):       
        project = utils.system.getProjectName()
        dbtyp = self.typ[1]
        name = self.lineEdit.text()
        description = self.plainTextEdit.toPlainText()    
        doc_id = "%s_%s_%s" % ( project, dbtyp, name )
        core.hktask.createAssetTask(doc_id = doc_id, description = description)
        self.label_status.setText("%s created" % doc_id)
    
    
class UiMainVizor(object):
    #TODO:add another combo box to filter tasks
    #TODO:remove create button and the lineedit
    #TODO:create a progress bar to link to push/pull
        
    db = utils.dataBase.getDataBase()
    ccpath = os.path.join(os.getenv( "HK_PIPELINE"), "pipeline","creative")
    project = os.getenv ( "HK_PROJECT" )
        
    def searchLineChanged(self, lineEdit, treeWidget):
        it = QtGui.QTreeWidgetItemIterator(treeWidget)
        text = self.lineEdit_a.text()
        
        while it.value():
            item = it.value()
            if not item.parent():
                if filter != "" :
                    itemtext = item.text(0)
                    if itemtext.find(text)>=0:
                        item.setHidden (False)
                    else:
                        item.setHidden (True)
                else:
                    item.setHidden (False)       
            it.next()
                
    def searchLine(self):
        self.searchLineChanged(self.lineEdit_a, self.treeWidget_a)
                
    def itemExpanded(self,item):
        print item.text(0)
        
    def createWidget(self):
        pass
    
    def comboTypeChange(self):
        typ = self.comboBox_a.currentText()
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
        self.lineEdit_a.textChanged.connect(self.searchLine)
        self.treeWidget_a.itemExpanded.connect(self.itemExpanded)
        self.treeWidget_a.itemClicked.connect(self.itemClicked)
        self.treeWidget_a.customContextMenuRequested.connect(self.contextMenuEvent)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(541, 595)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox_a = QtGui.QComboBox(self.centralwidget)
        self.comboBox_a.setObjectName("comboBox_a")
        self.verticalLayout.addWidget(self.comboBox_a)
        self.lineEdit_a = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_a.setObjectName("lineEdit_a")
        self.lineEdit_a.setText("type asset name")
        self.verticalLayout.addWidget(self.lineEdit_a)
        self.treeWidget_a = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget_a.setAlternatingRowColors(True)
        self.treeWidget_a.setObjectName("treeWidget_a")
        self.treeWidget_a.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.verticalLayout.addWidget(self.treeWidget_a)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelImage = QtGui.QLabel(self.centralwidget)
        self.labelImage.setMinimumSize(QtCore.QSize(300, 300))
        self.labelImage.setObjectName("labelImage")
        self.verticalLayout_2.addWidget(self.labelImage)
        self.plainTextEdit_comment = QtGui.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_comment.setReadOnly(True)
        self.plainTextEdit_comment.setPlainText("")
        self.plainTextEdit_comment.setObjectName("plainTextEdit_comment")
        self.verticalLayout_2.addWidget(self.plainTextEdit_comment)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_main.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.createButton = QtGui.QPushButton(self.centralwidget)
        self.createButton.setObjectName("createButton")
        self.horizontalLayout_3.addWidget(self.createButton)
        self.verticalLayout_main.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_main)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.createWidget()
        self.signalConnect()
#         self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_a.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "asset", None, QtGui.QApplication.UnicodeUTF8))
        self.createButton.setText(QtGui.QApplication.translate("MainWindow", "create", None, QtGui.QApplication.UnicodeUTF8))

class UiAssetVizor(UiMainVizor):
    #TODO:create list of tasks per asset
    #TODO:change fonts for asset
    #TODO:support sequence and shot
    
    pushls = ("texture",
              "render",
              "compout")
        
    asset_task={"surface":"sur",
                "model":"mod",
                "texture":"tex",
                "rig":"rig",
                "sculpt":"sct",
                "retopo":"rtp"}
    
    typ_dict = {"character":("chr",asset_task),
                "vehicle":("vcl",asset_task),
                "prop":("prp",asset_task),
                "environment":("env",asset_task),
                "effect":("vfx",asset_task),
                "material":("mtl",asset_task)}
    
    def createAsset(self):
        self.createAssetWin = UiCreateAsset()
        nicename = self.comboBox_a.currentText()
        typ = self.typ_dict[nicename][0]
        self.createAssetWidget=QtGui.QWidget()
        self.createAssetWin.setupUi(self.createAssetWidget, (nicename, typ) )
        self.createAssetWidget.show()
        
    def createTask(self):
        typ = self.comboBox_a.currentText()
        item = self.treeWidget_a.currentItem()
        item_parent = item.parent()
        asset = item_parent.text(0)
        task = self.typ_dict[typ][1][item.text(0)]
        doc_id = "%s_%s_%s" % (self.typ_dict[typ][0],asset,task)
        nicename = "%s %s %s fork" % (typ, asset, item.text(0))
        self.createTaskWin = UiCreateTask()   
        self.createTaskWidget=QtGui.QWidget()
        self.createTaskWin.setupUi(self.createTaskWidget, (nicename, doc_id) )
        self.createTaskWidget.show()
        
    def pushVersion(self):
        item = self.treeWidget_a.currentItem()
        task = item.parent().text(0) 
        doc_id = item.doc_id
        if task in self.pushls:
            self.pushVersionWin = UiPushLs()
        else:
            self.pushVersionWin = UiPush()

        self.pushVersionWidget=QtGui.QWidget()
        self.pushVersionWin.setupUi(self.pushVersionWidget, self.db, doc_id)
        self.pushVersionWidget.show()
    
    def pullVersion(self):
        #TODO:link the main progress bar
        item = self.treeWidget_a.currentItem()
        doc_id = item.parent().doc_id
        ver = int(item.text(0)) 
        hkrepository.pull(self.db, doc_id = doc_id, ver = ver ) #, progressbar)
    
    def createWorkspace(self):
        item = self.treeWidget_a.currentItem()
        hkrepository.createWorkspace ( doc_id = item.doc_id )

    def contextMenuAsset(self,item):
        menu = QtGui.QMenu()
        action = menu.addAction('Create new asset')
        action.triggered.connect(self.createAsset)
        menu.exec_(QtGui.QCursor.pos())
         
    def contextMenuTask(self,item):
        menu = QtGui.QMenu()
        action = menu.addAction('New %s %s fork' % 
                                ( item.parent().text(0), item.text(0) ) )
        action.triggered.connect( self.createTask )
        menu.exec_(QtGui.QCursor.pos())
        
    def contextMenuFork(self,item):
        menu = QtGui.QMenu()
        item = self.treeWidget_a.currentItem()
        path = core.hkrepository.getWorkspaceFromId(doc_id = item.doc_id)
        
        if os.path.exists(path):
            action = menu.addAction('Push a new version')
            action.triggered.connect( self.pushVersion )
        else:
            action = menu.addAction('Create workspace')
            action.triggered.connect( self.createWorkspace )
            
        menu.exec_(QtGui.QCursor.pos())
        
    def contextMenuVersion(self,item):
        print item.text(0)
        menu = QtGui.QMenu()
        action = menu.addAction ( 'Pull version %s' % item.text (0) )
        action.triggered.connect ( self.pullVersion )
        menu.exec_( QtGui.QCursor.pos () )
        
    def contextMenuEvent(self):
        item = self.treeWidget_a.currentItem()
        
        if not item:
            self.contextMenuAsset(item)
            
        else :
            item_type = item.hktype
            
            if item_type == "asset" :
                self.contextMenuAsset(item)
                
            elif item_type == "task" :
                self.contextMenuTask(item)
                
            elif item_type == "fork" :
                self.contextMenuFork(item)
                
            elif item_type == "version" :
                self.contextMenuVersion(item)
                
            elif item_type == "None" :
                pass
            
    def itemExpandedAsset(self,item):
        itChildCount = item.childCount ()       
         
        if not (itChildCount > 1) :
            item.removeChild ( item.child(0) )
            icon_empty = os.path.join ( self.ccpath, "empty.png" )
            task_dict = self.typ_dict [ self.comboBox_a.currentText() ][1]
            
            for task in task_dict:
                itemChild = QtGui.QTreeWidgetItem ( item )
                itemChild.setText (0, task)
                icon=os.path.join ( self.ccpath,task + ".png" )
                itemChild.setIcon ( 0, QtGui.QIcon ( icon ) )
                itemChild.hktype = "task"
                itemChild.hkid = ( "%s_%s" ) % ( item.hkid, task_dict[task] )
                item_none = QtGui.QTreeWidgetItem( itemChild )
                item_none.hktype = "none"
                item_none.setText ( 0, "Empty" )
                item_none.setIcon ( 0, QtGui.QIcon(icon_empty ) )
                item_none.setHidden = True
                
            order=QtCore.Qt.AscendingOrder    
            item.sortChildren(0, order)
            
    def itemExpandedTask(self,item):
        if item.child(0).hktype == "none" : 
            task_dict = self.typ_dict[self.comboBox_a.currentText()][1]   
            task = task_dict[item.text(0)]
            parentId = item.parent().hkid
            startkey = "%s_%s_%s" % (self.project, parentId, task)
            itNameLs = utils.dataBase.lsDb(self.db, "asset_task", startkey)
            icon_empty=os.path.join(self.ccpath,"empty.png")
            
            if len(itNameLs)>0:
                item.removeChild(item.child(0))           
            
            for itName in itNameLs:
                itemChild = QtGui.QTreeWidgetItem(item)
                itemChild.setText(0,itName.split("_")[-1])
                itemChild.hktype = "fork"
                icon = os.path.join(self.ccpath,"fork.png")
                itemChild.setIcon(0,QtGui.QIcon(icon))
                itemChild.versions = dict()
                itemChild.hkid = itName
                itemChild.doc_id = "%s_%s" % (self.project,itName)
                itemChild.dbdoc = self.db[itemChild.doc_id]
                item_none = QtGui.QTreeWidgetItem(itemChild)
                item_none.hktype = "none"
                item_none.setText(0,"Empty")
                item_none.setIcon(0,QtGui.QIcon(icon_empty))
                item_none.setText(0,"Empty")
                item_none.setHidden = True
                
            order=QtCore.Qt.AscendingOrder    
            item.sortChildren(0, order)
        
    def itemExpandedFork(self,item):
        if item.child(0).hktype == "none" :
            if item.versions == dict():
                item.versions = item.dbdoc["versions"]                
                if len(item.versions)>0:
                    for ver in item.versions:
                        itemChild = QtGui.QTreeWidgetItem(item)
                        icon = os.path.join(self.ccpath,"file.png")
                        itemChild.setIcon(0,QtGui.QIcon(icon))
                        itemChild.setText(0,"%03d"%float(ver))
                        itemChild.hktype = "version"
                        itemChild.info = item.versions[ver]
                        
                    order=QtCore.Qt.DescendingOrder
                    item.sortChildren(0, order)
                    item.removeChild(item.child(0))
        
    def itemExpanded(self,item):
        if item.hktype == "asset":
            self.itemExpandedAsset(item)
            
        elif item.hktype == "task" :
            self.itemExpandedTask(item)
            
        elif item.hktype == "fork" :
            self.itemExpandedFork(item)
                            
    def itemClickedVersion( self, item ):
                
        """Set the data to the plain text"""
        creator  = "Creator:\t%s\n" % item.info['creator']
        created  = "\nCreated:\t%s\n" % item.info['created']
        comments = "\nComments:\n\t%s\n" % item.info['comments']
        
        path = os.path.expandvars( item.info["path"] )
        pathinfo = "\nPath:\n\t%s\n" % os.path.expandvars(item.info["path"])
        
        files ="\n\t".join( map( str, item.info["files"] ) )
        files = "\nFiles:\n\t%s\n" % files
         
        infos=creator+created+comments+pathinfo+files
        self.plainTextEdit_comment.setPlainText(infos)
        """Set the screenshot"""
        screenshot = "%s_%s.jpg" % (self.project,item.parent().hkid)
        screenshot = os.path.join(path, screenshot)
        
        if not os.path.exists(screenshot):
            empty = os.path.join(os.getenv( "HK_PIPELINE"), "pipeline",
                                            "creative", "empty.gif" )
            self.labelImage.setPixmap( empty )

    def itemClickedFork( self, item ):
                
        """Set the data to the plain text"""
        creator  = "Creator:\t%s\n" % item.dbdoc['creator']
        created  = "\nCreated:\t%s\n" % item.dbdoc['created']
        state = "\nState:\t%s\n" % item.dbdoc['state']
        description = "\nDescription:\n\t%s\n" % item.dbdoc['description']
          
        infos = creator+created+state+description
        self.plainTextEdit_comment.setPlainText(infos)  
        
    def itemClicked(self, item):
       
        if item.hktype == "fork":
            self.itemClickedFork(item)
        elif item.hktype == "version":
            self.itemClickedVersion(item)
        else:
            self.plainTextEdit_comment.setPlainText("")
        
    def comboTypeChange(self):
        currtext = self.comboBox_a.currentText()      
        self.typ = self.typ_dict[currtext][0]
        startkey = "%s_%s" % (self.project,self.typ)
        asset_ls = utils.dataBase.lsDb(self.db, self.typ, startkey)
        icon_empty=os.path.join(self.ccpath,"empty.png")
        #TODO:Optimize instead of deleting items hide by type,                
        self.treeWidget_a.clear()
        
        for asset in asset_ls:
            item_asset = QtGui.QTreeWidgetItem(self.treeWidget_a)
            item_asset.setText(0,"%s" % asset.split("_")[-1])
            icon=os.path.join(self.ccpath,currtext+".png")
            item_asset.setIcon(0,QtGui.QIcon(icon))
            item_asset.hktype = "asset"
            item_asset.hkid = asset
            item_none = QtGui.QTreeWidgetItem(item_asset)
            item_none.setIcon(0,QtGui.QIcon(icon_empty))
            item_none.setText(0,"Empty")
            item_none.hktype = "none"
                
    def createWidget(self):
        typ_ls = list()
        for key in self.typ_dict:
            icon=os.path.join(self.ccpath,key+".png")
            self.comboBox_a.addItem(QtGui.QIcon(icon),key)
            typ_ls.append(key) 
    

# Create a Qt application
app = QtGui.QApplication(sys.argv)

main=QtGui.QMainWindow()
setupui=UiAssetVizor()
setupui.setupUi(main)
main.show()

# Enter Qt application main loop
app.exec_()
sys.exit()