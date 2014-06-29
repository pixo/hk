'''
Created on Jun 17, 2014

@author: pixo
'''
import sys, re
from PySide import QtCore, QtGui
import badass.utils as utils
import badass.core as core


class UiCreateAsset(QtGui.QWidget):

    def createFilterTypes(self):
        """Create the type comboBox"""
        items = self.assetTypes
        items = sorted([(key, value) for (key, value) in items.items()])

        # Set the types items
        for couple in items :
            icon = utils.getIconPath(couple[0])
            self.comboBoxAssetTypeFilter.addItem(QtGui.QIcon(icon), couple[0])

    def pushButtonClicked(self):
        self.label_status.setText ("")
        currentType = self.comboBoxAssetTypeFilter.currentText()
        currentType = self.assetTypes[currentType]
        name = self.lineEdit.text()

        if name == "":
            msg = "Can't create asset '%s' no characters in name"
            self.label_status.setText(msg % name)
            return

        if name.find("_") >= 0:
            msg = "Can't create asset '%s' name shouldn't contain underscore"
            self.label_status.setText(msg % name)
            return

        if name.find(" ") >= 0:
            msg = "Can't create asset '%s' name shouldn't contain space"
            self.label_status.setText(msg % name)
            return

        description = self.plainTextEdit.toPlainText()
        doc_id = "%s_%s_%s" % (utils.getProjectName(), currentType, name)

        doc = core.createAsset (doc_id = doc_id, description = description)
        if doc :
            self.lineEdit.setText("")
            self.label_status.setText("%s created" % doc_id)

        if self.assetManager:
            self.assetManager.refreshTree()

        self.close ()

    def plainTextEditChanged(self):
        descriptions = self.plainTextEdit.toPlainText()
        if descriptions == "" :
            self.pushButton.setEnabled(False)
        else :
            self.pushButton.setEnabled(True)

    def signalConnect(self):
        self.pushButton.clicked.connect (self.pushButtonClicked)
        self.plainTextEdit.textChanged.connect (self.plainTextEditChanged)


    def __init__(self, parent = None, assetManager = None):
        super(UiCreateAsset, self).__init__(parent)

        self.assetManager = assetManager
        self.setObjectName("Form")
        self.resize(486, 429)
        self.setWindowTitle("create Asset")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayoutTitle = QtGui.QHBoxLayout()
        self.horizontalLayoutTitle.setContentsMargins(3, -1, 3, -1)
        self.horizontalLayoutTitle.setObjectName("horizontalLayoutTitle")
        self.labelSystemTitle = QtGui.QLabel(self)
        self.labelSystemTitle.setMaximumSize(QtCore.QSize(21, 16777215))
        self.labelSystemTitle.setObjectName("labelSystemTitle")
        self.horizontalLayoutTitle.addWidget(self.labelSystemTitle)
        self.labelProjectTitle = QtGui.QLabel(self)
        self.labelProjectTitle.setObjectName("labelProjectTitle")
        self.horizontalLayoutTitle.addWidget(self.labelProjectTitle)
        self.verticalLayout.addLayout(self.horizontalLayoutTitle)

        self.line1Main = QtGui.QFrame(self)
        self.line1Main.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1Main.setLineWidth(2)
        self.line1Main.setFrameShape(QtGui.QFrame.HLine)
        self.line1Main.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1Main.setObjectName("line1Main")
        self.verticalLayout.addWidget(self.line1Main)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxAssetTypeFilter = QtGui.QComboBox(self)
        self.comboBoxAssetTypeFilter.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBoxAssetTypeFilter.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBoxAssetTypeFilter.setAccessibleName("")
        self.comboBoxAssetTypeFilter.setObjectName("comboBoxAssetTypeFilter")
        self.horizontalLayout.addWidget(self.comboBoxAssetTypeFilter)

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

        self.assetTypes = utils.getAssetTypes()

        self.setUi()
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setUi(self):
        # Title
        self.labelSystemTitle.setPixmap(utils.getIconPath("addasset"))
        self.labelProjectTitle.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">%s</span><span style=\" font-size:12pt;\"/></body></html>" % ("Create Asset"), None, QtGui.QApplication.UnicodeUTF8))
        self.createFilterTypes()


class UiCreateTask (QtGui.QWidget) :

    def pushButtonClicked (self) :

        tasks = utils.getAssetTasks ()
        assetId = self.item.id
        fork = self.lineEditFork.text()
        description = self.plainTextEditComments.toPlainText()

        if fork != "" :
            for i in range (0, self.listWidgetTask.count()):
                item = self.listWidgetTask.item (i)

                if item.checkState() == QtCore.Qt.CheckState.Checked :
                    task = tasks [ item.text () ]
                    doc_id = "%s_%s_%s" % (assetId, task, fork)
                    doc = core.createTask (doc_id = doc_id, description = description)

                    if doc :
                        self.labelStatus.setText ("%s created" % doc_id)

            self.assetManager.refreshTree()
            self.close ()

        else :
            self.labelStatus.setText ("Please provide a Fork name")

    def createComboxBoxFork(self):
        ""
        forks = list()

        for task in self.tasks:
            value = self.tasks[task]
            fork = value["fork"]

            if not (fork in forks):
                forks.append(fork)

        forks.append("New fork ...")
        self.comboBoxFork.addItems(forks)

    def createListWidget(self) :
        """Clear previous task list"""
        self.listWidgetTask.clear ()

        """Get fork lineEdit """
        fork = self.lineEditFork.text()

        """Get Description test"""
        textdoc = self.plainTextEditComments.document ()
        description = textdoc.toPlainText ()

        if fork != "" :
            """Check if description is not empty to enable it"""
            if description != "":
                self.pushButton.setEnabled (True)

            else:
                self.pushButton.setEnabled (False)

            """Create task items"""
            for i in self.taskTypes :
                self.listWidgetTask.addItem (i)

            """Set task status"""
            for i in range (0, self.listWidgetTask.count ()) :
                """get items task"""
                item = self.listWidgetTask.item (i)

                """get item name"""
                itemText = item.text ()

                """create task id from asset id, item text and fork line """
                itemId = self.taskTypes [ itemText ]
                task = "%s_%s_%s" % (self.item.id, itemId, fork)
                icon = utils.getIconPath(itemText)
                item.setIcon (QtGui.QIcon (icon))

                """if task exist change bg color"""
                if not (task in self.tasks) :
                    item.setCheckState (QtCore.Qt.Unchecked)
                else:
                    item.setBackground(QtGui.QColor (128, 255, 128))

        else :
            """Set create button false if fork is empty"""
            self.pushButton.setEnabled (False)

    def comboBoxForkChanged(self):
        text = self.comboBoxFork.currentText()
        if text == "New fork ...":
            self.lineEditFork.setDisabled(False)
            self.lineEditFork.setText("")
        else:
            self.lineEditFork.setDisabled(True)
            self.lineEditFork.setText(text)

    def commentsChanged (self) :
        textdoc = self.plainTextEditComments.document ()
        fork = self.lineEditFork.text ()
        description = textdoc.toPlainText ()

        if description == "" or fork == "":
            self.pushButton.setEnabled (False)

        else :
            self.pushButton.setEnabled (True)

    def signalConnect (self) :
        self.pushButton.clicked.connect (self.pushButtonClicked)
        self.lineEditFork.textChanged.connect (self.createListWidget)
        self.plainTextEditComments.textChanged.connect (self.commentsChanged)
        self.comboBoxFork.currentIndexChanged.connect(self.comboBoxForkChanged)

    def __init__(self, parent = None, db = None, item = None, assetManager = None):
        super (UiCreateTask, self).__init__(parent)

        if not item:
            self.close()

        self.db = db
        self.assetManager = assetManager
        self.item = item
        self.tasks = utils.lsDb (self.db, "task", self.item.id)
        self.taskTypes = utils.getAssetTasks ()

        self.setWindowTitle ("Add Task(s)")
        self.setObjectName ("Form")
        self.resize (803, 593)

        self.verticalLayoutMain = QtGui.QVBoxLayout(self)
        self.verticalLayoutMain.setObjectName("verticalLayoutMain")

        self.horizontalLayoutTitle = QtGui.QHBoxLayout()
        self.horizontalLayoutTitle.setContentsMargins(3, -1, 3, -1)
        self.horizontalLayoutTitle.setObjectName("horizontalLayoutTitle")
        self.labelSystemTitle = QtGui.QLabel(self)
        self.labelSystemTitle.setMaximumSize(QtCore.QSize(21, 16777215))
        self.labelSystemTitle.setObjectName("labelSystemTitle")
        self.horizontalLayoutTitle.addWidget(self.labelSystemTitle)
        self.labelProjectTitle = QtGui.QLabel(self)
        self.labelProjectTitle.setObjectName("labelProjectTitle")
        self.horizontalLayoutTitle.addWidget(self.labelProjectTitle)
        self.verticalLayoutMain.addLayout(self.horizontalLayoutTitle)

        self.line1Main = QtGui.QFrame(self)
        self.line1Main.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1Main.setLineWidth(2)
        self.line1Main.setFrameShape(QtGui.QFrame.HLine)
        self.line1Main.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1Main.setObjectName("line1Main")
        self.verticalLayoutMain.addWidget(self.line1Main)

        self.horizontalLayoutCenter = QtGui.QHBoxLayout()
        self.horizontalLayoutCenter.setObjectName("horizontalLayoutCenter")
        self.verticalLayout_file = QtGui.QVBoxLayout()
        self.verticalLayout_file.setObjectName("verticalLayout_file")

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelFork = QtGui.QLabel(self)
        self.labelFork.setMinimumSize(QtCore.QSize(16, 16))
        self.labelFork.setMaximumSize(QtCore.QSize(16, 16))
        self.labelFork.setObjectName("labelFork")
        self.horizontalLayout.addWidget(self.labelFork)

        self.comboBoxFork = QtGui.QComboBox()
        self.comboBoxFork.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBoxFork.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBoxFork.setAccessibleName("")
        self.comboBoxFork.setObjectName("comboBoxFork")
        self.horizontalLayout.addWidget(self.comboBoxFork)

        self.lineEditFork = QtGui.QLineEdit(self)
        self.lineEditFork.setObjectName("lineEditFork")
        self.horizontalLayout.addWidget(self.lineEditFork)

        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setEnabled (False)
        self.horizontalLayout.addWidget(self.pushButton)

        self.verticalLayout_file.addLayout(self.horizontalLayout)

        self.listWidgetTask = QtGui.QListWidget(self)
        self.listWidgetTask.setMinimumSize(QtCore.QSize(300, 0))
        self.listWidgetTask.setObjectName("listWidgetTask")
        self.listWidgetTask.setAlternatingRowColors(True)
        self.listWidgetTask.setSortingEnabled(True)
        self.verticalLayout_file.addWidget(self.listWidgetTask)
        self.horizontalLayoutCenter.addLayout(self.verticalLayout_file)

        self.lineCore = QtGui.QFrame(self)
        self.lineCore.setLineWidth(2)
        self.lineCore.setMidLineWidth(0)
        self.lineCore.setFrameShape(QtGui.QFrame.VLine)
        self.lineCore.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineCore.setObjectName("lineCore")
        self.horizontalLayoutCenter.addWidget(self.lineCore)

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelComments = QtGui.QLabel(self)
        self.labelComments.setAlignment(QtCore.Qt.AlignCenter)
        self.labelComments.setObjectName("labelComments")
        self.verticalLayout.addWidget(self.labelComments)
        self.plainTextEditComments = QtGui.QPlainTextEdit(self)
        self.plainTextEditComments.setMinimumSize(QtCore.QSize(300, 0))
        self.plainTextEditComments.setObjectName("plainTextEditComments")
        self.verticalLayout.addWidget(self.plainTextEditComments)
        self.horizontalLayoutCenter.addLayout(self.verticalLayout)
        self.verticalLayoutMain.addLayout(self.horizontalLayoutCenter)

        self.lineBottom = QtGui.QFrame(self)
        self.lineBottom.setLineWidth(2)
        self.lineBottom.setMidLineWidth(0)
        self.lineBottom.setFrameShape(QtGui.QFrame.HLine)
        self.lineBottom.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineBottom.setObjectName("lineBottom")
        self.verticalLayoutMain.addWidget(self.lineBottom)

        self.labelStatus = QtGui.QLabel(self)
        self.labelStatus.setText("")
        self.labelStatus.setObjectName("labelStatus")
        self.verticalLayoutMain.addWidget(self.labelStatus)

        self.setUi(self)
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "create task(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFork.setPixmap(utils.getIconPath("fork"))
        self.labelFork.setToolTip("Select the fork or create a new one.")
        self.labelComments.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Description</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "create", None, QtGui.QApplication.UnicodeUTF8))

        # Title
        self.labelSystemTitle.setPixmap(utils.getIconPath("addtask"))
        self.labelProjectTitle.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">%s</span><span style=\" font-size:12pt;\"/><span style=\" font-size:12pt; font-weight:600;\">:</span><span style=\" font-size:12pt;\"> %s %s</span></p></body></html>" % ("Adding Task(s)", self.item.type, self.item.slug), None, QtGui.QApplication.UnicodeUTF8))

        self.createComboxBoxFork()
        self.comboBoxForkChanged()
        self.createListWidget()

class UiAssetManager(QtGui.QMainWindow):

    launcher = "terminal"

    def __init__(self, parent = None):
        super(UiAssetManager, self).__init__(parent)

        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayoutMain = QtGui.QVBoxLayout()
        self.verticalLayoutMain.setObjectName("verticalLayoutMain")
        self.horizontalLayoutTitle = QtGui.QHBoxLayout()
        self.horizontalLayoutTitle.setContentsMargins(3, -1, 3, -1)
        self.horizontalLayoutTitle.setObjectName("horizontalLayoutTitle")
        self.labelSystemTitle = QtGui.QLabel(self.centralwidget)
        self.labelSystemTitle.setMaximumSize(QtCore.QSize(21, 16777215))
        self.labelSystemTitle.setObjectName("labelSystemTitle")
        self.horizontalLayoutTitle.addWidget(self.labelSystemTitle)
        self.labelProjectTitle = QtGui.QLabel(self.centralwidget)
        self.labelProjectTitle.setObjectName("labelProjectTitle")
        self.horizontalLayoutTitle.addWidget(self.labelProjectTitle)
        self.verticalLayoutMain.addLayout(self.horizontalLayoutTitle)
        self.line1Main = QtGui.QFrame(self.centralwidget)
        self.line1Main.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1Main.setLineWidth(2)
        self.line1Main.setFrameShape(QtGui.QFrame.HLine)
        self.line1Main.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1Main.setObjectName("line1Main")
        self.verticalLayoutMain.addWidget(self.line1Main)
        self.horizontalLayoutCore = QtGui.QHBoxLayout()
        self.horizontalLayoutCore.setObjectName("horizontalLayoutCore")
        self.verticalLayoutLeft = QtGui.QVBoxLayout()
        self.verticalLayoutLeft.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayoutLeft.setObjectName("verticalLayoutLeft")
        self.horizontalLayoutFilter = QtGui.QHBoxLayout()
        self.horizontalLayoutFilter.setContentsMargins(3, -1, 3, -1)
        self.horizontalLayoutFilter.setObjectName("horizontalLayoutFilter")
        self.labelFilter = QtGui.QLabel(self.centralwidget)
        self.labelFilter.setEnabled(True)
        self.labelFilter.setMaximumSize(QtCore.QSize(16, 16))
        self.labelFilter.setObjectName("labelFilter")
        self.horizontalLayoutFilter.addWidget(self.labelFilter)

        self.comboBoxAssetTypeFilter = QtGui.QComboBox(self.centralwidget)
        self.comboBoxAssetTypeFilter.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBoxAssetTypeFilter.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBoxAssetTypeFilter.setAccessibleName("")
        self.comboBoxAssetTypeFilter.setObjectName("comboBoxAssetTypeFilter")
        self.horizontalLayoutFilter.addWidget(self.comboBoxAssetTypeFilter)

        self.comboBoxAssetTaskFilter = QtGui.QComboBox(self.centralwidget)
        self.comboBoxAssetTaskFilter.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBoxAssetTaskFilter.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBoxAssetTaskFilter.setAccessibleName("")
        self.comboBoxAssetTaskFilter.setObjectName("comboBoxAssetTaskFilter")
        self.horizontalLayoutFilter.addWidget(self.comboBoxAssetTaskFilter)

        self.comboBoxAssetForkFilter = QtGui.QComboBox(self.centralwidget)
        self.comboBoxAssetForkFilter.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBoxAssetForkFilter.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBoxAssetForkFilter.setAccessibleName("")
        self.comboBoxAssetForkFilter.setObjectName("comboBoxAssetForkFilter")
        self.horizontalLayoutFilter.addWidget(self.comboBoxAssetForkFilter)

        self.verticalLayoutLeft.addLayout(self.horizontalLayoutFilter)
        self.horizontalLayoutSearch = QtGui.QHBoxLayout()
        self.horizontalLayoutSearch.setContentsMargins(3, -1, 3, -1)
        self.horizontalLayoutSearch.setObjectName("horizontalLayoutSearch")
        self.labelSearch = QtGui.QLabel(self.centralwidget)
        self.labelSearch.setMaximumSize(QtCore.QSize(16, 16))
        self.labelSearch.setObjectName("labelSearch")
        self.horizontalLayoutSearch.addWidget(self.labelSearch)
        self.lineEditSearch = QtGui.QLineEdit(self.centralwidget)
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.horizontalLayoutSearch.addWidget(self.lineEditSearch)
        self.verticalLayoutLeft.addLayout(self.horizontalLayoutSearch)
        self.horizontalLayoutExplorer = QtGui.QHBoxLayout()
        self.horizontalLayoutExplorer.setObjectName("horizontalLayoutExplorer")
        self.verticalLayoutToolBar = QtGui.QVBoxLayout()
        self.verticalLayoutToolBar.setObjectName("verticalLayoutToolBar")

        # Workspace button
        self.buttonCreateWorkspaceToolBar = QtGui.QPushButton(self.centralwidget)
        self.buttonCreateWorkspaceToolBar.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonCreateWorkspaceToolBar.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonCreateWorkspaceToolBar.setObjectName("buttonPullToolBar")
        self.verticalLayoutToolBar.addWidget(self.buttonCreateWorkspaceToolBar)

        # Pull button
        self.buttonPullToolBar = QtGui.QPushButton(self.centralwidget)
        self.buttonPullToolBar.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonPullToolBar.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonPullToolBar.setObjectName("buttonPullToolBar")
        self.verticalLayoutToolBar.addWidget(self.buttonPullToolBar)

        # Push button
        self.buttonPushToolBar = QtGui.QPushButton(self.centralwidget)
        self.buttonPushToolBar.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonPushToolBar.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonPushToolBar.setObjectName("buttonPushToolBar")
        self.verticalLayoutToolBar.addWidget(self.buttonPushToolBar)

        # Set status button
        self.buttonSetStatusToolBar = QtGui.QPushButton(self.centralwidget)
        self.buttonSetStatusToolBar.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonSetStatusToolBar.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonSetStatusToolBar.setObjectName("buttonSetStatusToolBar")
        self.verticalLayoutToolBar.addWidget(self.buttonSetStatusToolBar)

        # CreateAsset button
        self.buttonCreateAssetToolBar = QtGui.QPushButton(self.centralwidget)
        self.buttonCreateAssetToolBar.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonCreateAssetToolBar.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonCreateAssetToolBar.setToolTip("")
        self.buttonCreateAssetToolBar.setObjectName("buttonCreateAssetToolBar")
        self.verticalLayoutToolBar.addWidget(self.buttonCreateAssetToolBar)

        # CreateTask button
        self.buttonCreateTaskToolBar = QtGui.QPushButton(self.centralwidget)
        self.buttonCreateTaskToolBar.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonCreateTaskToolBar.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonCreateTaskToolBar.setToolTip("")
        self.buttonCreateTaskToolBar.setObjectName("buttonCreateTaskToolBar")
        self.verticalLayoutToolBar.addWidget(self.buttonCreateTaskToolBar)

        # Delete asset
        self.buttonDeleteAssetToolBar = QtGui.QPushButton(self.centralwidget)
        self.buttonDeleteAssetToolBar.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonDeleteAssetToolBar.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonDeleteAssetToolBar.setObjectName("buttonDeleteAssetToolBar")
        self.verticalLayoutToolBar.addWidget(self.buttonDeleteAssetToolBar)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayoutToolBar.addItem(spacerItem)

        self.horizontalLayoutExplorer.addLayout(self.verticalLayoutToolBar)
        self.verticalLayoutTree = QtGui.QVBoxLayout()
        self.verticalLayoutTree.setObjectName("verticalLayoutTree")
        self.horizontalLayoutVersions = QtGui.QHBoxLayout()
        self.horizontalLayoutVersions.setObjectName("horizontalLayoutVersions")

        # VersionType comboBox
        self.comboBoxVersionType = QtGui.QComboBox(self.centralwidget)
        self.comboBoxVersionType.setMaximumSize(QtCore.QSize(90, 16777215))
        self.comboBoxVersionType.setAccessibleName("")
        self.comboBoxVersionType.setObjectName("comboBoxVersionType")
        self.horizontalLayoutVersions.addWidget(self.comboBoxVersionType)

        # Versions comboBox
        self.comboBoxVersions = QtGui.QComboBox(self.centralwidget)
        self.comboBoxVersions.setMaximumSize(QtCore.QSize(70, 16777215))
        self.comboBoxVersions.setAccessibleName("")
        self.comboBoxVersions.setObjectName("comboBoxVersions")
        self.horizontalLayoutVersions.addWidget(self.comboBoxVersions)

        # ActiveOnly CheckBox
        self.checkBoxActive = QtGui.QCheckBox(self.centralwidget)
        self.checkBoxActive.setEnabled(True)
        self.checkBoxActive.setChecked(True)
        self.checkBoxActive.setTristate(False)
        self.checkBoxActive.setObjectName("checkBoxActive")
        self.horizontalLayoutVersions.addWidget(self.checkBoxActive)

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayoutVersions.addItem(spacerItem1)

        # Refresh button
        self.buttonRefresh = QtGui.QPushButton(self.centralwidget)
        self.buttonRefresh.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonRefresh.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonRefresh.setObjectName("buttonRefresh")
        self.horizontalLayoutVersions.addWidget(self.buttonRefresh)

        self.verticalLayoutTree.addLayout(self.horizontalLayoutVersions)
        self.treeWidgetMain = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidgetMain.setAlternatingRowColors(True)
        self.treeWidgetMain.setRootIsDecorated(True)
        self.treeWidgetMain.setAnimated(True)
        self.treeWidgetMain.setWordWrap(False)
        self.treeWidgetMain.setObjectName("treeWidgetMain")
        self.treeWidgetMain.header().setVisible(False)
        self.verticalLayoutTree.addWidget(self.treeWidgetMain)
        self.horizontalLayoutExplorer.addLayout(self.verticalLayoutTree)
        self.verticalLayoutLeft.addLayout(self.horizontalLayoutExplorer)
        self.horizontalLayoutCore.addLayout(self.verticalLayoutLeft)
        self.lineCore = QtGui.QFrame(self.centralwidget)
        self.lineCore.setLineWidth(2)
        self.lineCore.setMidLineWidth(0)
        self.lineCore.setFrameShape(QtGui.QFrame.VLine)
        self.lineCore.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineCore.setObjectName("lineCore")
        self.horizontalLayoutCore.addWidget(self.lineCore)
        self.verticalLayoutInfos = QtGui.QVBoxLayout()
        self.verticalLayoutInfos.setObjectName("verticalLayoutInfos")
        self.labelImageInfos = QtGui.QLabel(self.centralwidget)
        self.labelImageInfos.setMinimumSize(QtCore.QSize(300, 300))
        self.labelImageInfos.setText("")
        self.labelImageInfos.setObjectName("labelImageInfos")
        self.verticalLayoutInfos.addWidget(self.labelImageInfos)
        self.lineInfos = QtGui.QFrame(self.centralwidget)
        self.lineInfos.setFrameShape(QtGui.QFrame.HLine)
        self.lineInfos.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineInfos.setObjectName("lineInfos")
        self.verticalLayoutInfos.addWidget(self.lineInfos)
        self.plainTextEditInfos = QtGui.QPlainTextEdit(self.centralwidget)
        self.plainTextEditInfos.setEnabled(False)
        self.plainTextEditInfos.setPlainText("")
        self.plainTextEditInfos.setObjectName("plainTextEditInfos")
        self.verticalLayoutInfos.addWidget(self.plainTextEditInfos)
        self.horizontalLayoutCore.addLayout(self.verticalLayoutInfos)
        self.verticalLayoutMain.addLayout(self.horizontalLayoutCore)
        self.line2Main = QtGui.QFrame(self.centralwidget)
        self.line2Main.setFrameShape(QtGui.QFrame.HLine)
        self.line2Main.setFrameShadow(QtGui.QFrame.Sunken)
        self.line2Main.setObjectName("line2Main")
        self.verticalLayoutMain.addWidget(self.line2Main)
        self.horizontalLayoutStatus = QtGui.QHBoxLayout()
        self.horizontalLayoutStatus.setObjectName("horizontalLayoutStatus")
        self.progressBarStatus = QtGui.QProgressBar(self.centralwidget)
        self.progressBarStatus.setEnabled(True)
        self.progressBarStatus.setProperty("value", 0)
        self.progressBarStatus.setObjectName("progressBarStatus")
        self.progressBarStatus.setVisible(False)
        self.horizontalLayoutStatus.addWidget(self.progressBarStatus)
        self.verticalLayoutMain.addLayout(self.horizontalLayoutStatus)
        self.horizontalLayout_2.addLayout(self.verticalLayoutMain)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # TODO:Clean it
        self.db = utils.getDb()
        self.user = utils.getCurrentUser()
        self.users = core.getProjectUsers (self.db)
        self.userStatus = self.users[self.user]
        self.project = utils.getProjectName()
        self.assetTypes = utils.getAssetTypes()
        self.assetTypes = dict({"No filter":"asset"}.items() + self.assetTypes.items())
        self.assetTypesSwap = dict((value, key) for key, value in self.assetTypes.iteritems())
        self.assetTasks = utils.getAssetTasks()
        self.assetTasks = dict({"No filter":"task"}.items() + self.assetTasks.items())
        self.assetTasksSwap = dict((value, key) for key, value in self.assetTasks.iteritems())
        self.allTasks = dict()
        self.versionTypes = ("review", "release")

        self.setUi()
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName(self)


    def createFilterTypes(self):
        """Create the type comboBox"""
        items = self.assetTypes
        items = sorted([(key, value) for (key, value) in items.items()])
        items.remove(("No filter", "asset"))
        items = [("No filter", "asset")] + items

        # Set the types items
        for couple in items :
            icon = utils.getIconPath("asset" if couple[0] == "No filter" else couple[0])
            self.comboBoxAssetTypeFilter.addItem(QtGui.QIcon(icon), couple[0])


    def createFilterTasks(self):
        """Create the tasks comboBox"""
        items = self.assetTasks
        items = sorted([(key, value) for (key, value) in items.items()])
        items.remove(("No filter", "task"))
        items = [("No filter", "task")] + items

        # Set the tasks items
        for couple in items :
            icon = utils.getIconPath("task" if couple[0] == "No filter" else couple[0])
            self.comboBoxAssetTaskFilter.addItem(QtGui.QIcon(icon), couple[0])

    def createFilterForks(self):
        """Create the tasks comboBox"""
        self.comboBoxAssetForkFilter.clear()
        items = self.allTasks
        forks = list()

        # Set the tasks items
        icon = utils.getIconPath("fork")
        self.comboBoxAssetForkFilter.addItem(QtGui.QIcon(icon), "No filter")
        for item in items :
            value = items[item]
            fork = value["fork"]
            if not (fork in forks):
                forks.append(fork)

        forks.sort()
        self.comboBoxAssetForkFilter.addItems(forks)

    def createVersions(self):
        """Create the versionType comboBox"""
        items = ("None")
        self.comboBoxVersions.addItems(items)

    def createVersionType(self):
        """Create the versiontype comboBox"""
        items = self.versionTypes
        # Create the version types
        for item in items :
            icon = utils.getIconPath(item)
            self.comboBoxVersionType.addItem(QtGui.QIcon(icon), item)

    def getTasksByAsset(self):
        tasks = dict()
        for task in self.allTasks:
            slug = self.allTasks[task]["name"]
            if not (slug in tasks) :
                tasks[slug] = list()
            tasks[slug].append(self.allTasks[task])
        return tasks

    def getStatusColor(self, status):
        color = QtCore.Qt.darkGray
        stat = "ns"
        if status == {"tec":"ns", "art":"ns"}:
            color = QtCore.Qt.darkGray
        elif status == {"tec":"app", "art":"app"}:
            color = QtCore.Qt.darkGreen
            stat = "app"
        else:
            color = QtCore.Qt.darkRed
            stat = "wip"
        return (color, stat)

    def getGlobalStatusColor(self, status):
        ns = list()
        app = list()

        color = QtCore.Qt.darkRed
        for i in status:
            if i == "ns" :
                ns.append(i)
            elif i == "app" :
                app.append(i)

        if len(ns) == len(status):
            color = QtCore.Qt.darkGray
        elif len(app) == len(status):
            color = QtCore.Qt.darkGreen

        return color

    def createTree(self):
        self.tasksByAsset = self.getTasksByAsset()
        self.treeWidgetMain.clear()

        # Set the asset items fonts
        assetFont = QtGui.QFont ()
        assetFont.setPointSize (10)
        assetFont.setWeight (75)
        assetFont.setItalic (False)
        assetFont.setBold (True)

        # Set the task items fonts
        taskFont = QtGui.QFont ()
        taskFont.setBold (True)

        # Inactive color
        redbrush = QtGui.QBrush()
        redbrush.setColor(QtGui.QColor(1, 0.5, 0.5))

        # Create the items
        for asset in self.allAssets :
            values = self.allAssets[asset]
            slug = values["name"]
            assetType = values["type"]

            # Create Asset items
            assetItem = QtGui.QTreeWidgetItem (self.treeWidgetMain)
            assetItem.typeNiceName = self.assetTypesSwap[assetType]
            assetItem.setFont(0, assetFont)
            assetItem.setText(0, slug)
            assetItem.type = assetType
            assetItem.task = False
            assetItem.id = values["_id"]
            assetItem.inactive = values["inactive"]
            assetItem.slug = slug
            assetIcon = utils.getIconPath(assetItem.typeNiceName)
            assetIcon = QtGui.QIcon(assetIcon)
            assetItem.setIcon(0, assetIcon)

            if values["inactive"]:
                assetItem.setBackground(0, QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.Dense4Pattern))

            # Create Task items
            globStat = list()
            if slug in self.tasksByAsset:
                for task in self.tasksByAsset[slug]:
                    assetTask = task["task"]
                    taskItem = QtGui.QTreeWidgetItem(assetItem)
                    taskItem.type = assetType
                    taskItem.task = assetTask
                    taskItem.taskNiceName = self.assetTasksSwap[assetTask]
                    taskItem.id = task["_id"]
                    taskItem.fork = task["fork"]
                    taskItem.slug = slug
                    taskItem.inactive = values["inactive"]
                    taskItem.setText(0, "%s %s" % (taskItem.taskNiceName, taskItem.fork))
                    taskItem.setFont(0, taskFont)
                    taskIcon = utils.getIconPath(taskItem.taskNiceName)
                    taskIcon = QtGui.QIcon(taskIcon)
                    taskItem.setIcon(0, taskIcon)
                    stat = self.getStatusColor(task["status"])
                    taskColor = stat[0]
                    globStat.append(stat[1])
                    taskItem.setForeground(0, QtGui.QBrush(taskColor))
                    if values["inactive"]:
                        taskItem.setBackground(0, QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.Dense6Pattern))

            assetColor = self.getGlobalStatusColor(globStat)
            assetItem.setForeground(0, QtGui.QBrush(assetColor))

        self.filterTree()

    def filterTree(self):
        it = QtGui.QTreeWidgetItemIterator(self.treeWidgetMain)
        text = self.lineEditSearch.text()
        currentType = self.comboBoxAssetTypeFilter.currentText()
        currentType = "asset" if currentType == "No filter" else currentType
        currentTask = self.comboBoxAssetTaskFilter.currentText()
        currentTask = "task" if currentTask == "No filter" else currentTask
        currentFork = self.comboBoxAssetForkFilter.currentText()
        currentFork = False if currentFork == "No filter" else currentFork
        activeOnly = self.checkBoxActive.isChecked()

        while it.value () :
            item = it.value()
            item.setHidden(False)
            slug = item.text(0)

            if not item.task :
                if activeOnly :
                    item.setHidden(item.inactive)

                if not (currentType in ("asset", item.typeNiceName)):
                    item.setHidden(True)

                try :
                    reg = (re.findall(text, slug) == [])
                except:
                    reg = False

                if not (text in ("", "\\")) and reg :
                    item.setHidden(True)
            else :
                if not (currentTask in ("task", item.taskNiceName)):
                    item.setHidden(True)

                if currentFork and item.fork != currentFork:
                    item.setHidden(True)

            it.next()

    def refreshTree(self):
        self.allAssets = utils.lsDb(self.db, "asset", self.project)
        self.allTasks = utils.lsDb(self.db, "task", self.project)
        self.createFilterForks()
        self.createTree()
        self.treeClicked()
        self.statusbar.showMessage("Welcome '%s' you are logged as '%s'.This project contain %d assets and %d tasks." % (self.user, self.userStatus, len(self.allAssets), len(self.allTasks)))

    def createAsset(self):
        self.createAssetWidget = UiCreateAsset(assetManager = self)
        self.createAssetWidget.show()

    def createTask(self):
        item = self.treeWidgetMain.currentItem ()
        if not item :
            print "not item selected"
            return

        self.createTaskWidget = UiCreateTask (db = self.db, item = item, assetManager = self)
        self.createTaskWidget.show()

    def deactivateAsset(self):
        "Delete Asset"
        item = self.treeWidgetMain.currentItem()
        slug = item.slug
        msg = "active" if item.inactive else "deactive"
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Do you want to %s '%s' ?" % (msg, slug))
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Save)
        ret = msgBox.exec_()

        if ret == QtGui.QMessageBox.Ok:
            # Save was clicked
            core.setAssetAttr(db = self.db, docId = item.id, attr = "inactive", value = not(item.inactive))
            item.inactive = not(item.inactive)
            self.refreshTree()
        else:
            print "Aborted"


    def workspace(self):
        item = self.treeWidgetMain.currentItem()
        core.createWorkspace(item.id, "review")

    def push(self):
        print ("push")

    def pull(self):
        print ("pull")

    def setStatus(self):
        print ("setStatus")

    def treeClicked(self):
        item = self.treeWidgetMain.currentItem()
        versionType = self.comboBoxVersionType.currentText()

        stat = False if item else True
        self.buttonSetStatusToolBar.setDisabled(stat)
        self.buttonCreateTaskToolBar.setDisabled(stat)
        self.buttonDeleteAssetToolBar.setDisabled(stat)

        stat = False if (item and item.task) else True
        self.buttonCreateWorkspaceToolBar.setDisabled(stat)
        self.buttonCreateTaskToolBar.setDisabled(not stat)
        self.buttonCreateTaskToolBar.setDisabled(not stat)
        self.buttonPullToolBar.setDisabled(stat)
        self.buttonPushToolBar.setDisabled(stat)

        value = self.allTasks[item.id] if not stat else False
        versions = value[versionType] if value else list()
        versions = list(versions)
        versions.sort(reverse = True)

        stat = False if len(versions) > 0 else True
        self.comboBoxVersions.setDisabled(stat)
        self.comboBoxVersions.clear()
        for version in versions:
            self.comboBoxVersions.addItem("%03d" % int(version))

        icon = "connect" if (item and item.inactive) else "disconnect"
        self.buttonDeleteAssetToolBar.setIcon(QtGui.QIcon(utils.getIconPath(icon)))

    def signalConnect(self):
        self.comboBoxAssetTypeFilter.currentIndexChanged.connect(self.filterTree)
        self.comboBoxAssetTaskFilter.currentIndexChanged.connect(self.filterTree)
        self.comboBoxAssetForkFilter.currentIndexChanged.connect(self.filterTree)
        self.lineEditSearch.textChanged.connect(self.filterTree)
        self.checkBoxActive.released.connect(self.refreshTree)
        self.buttonCreateWorkspaceToolBar.clicked.connect(self.workspace)
        self.buttonPullToolBar.clicked.connect(self.pull)
        self.buttonPushToolBar.clicked.connect(self.push)
        self.buttonSetStatusToolBar.clicked.connect(self.setStatus)
        self.buttonCreateAssetToolBar.clicked.connect(self.createAsset)
        self.buttonCreateTaskToolBar.clicked.connect(self.createTask)
        self.buttonDeleteAssetToolBar.clicked.connect(self.deactivateAsset)
        self.buttonRefresh.clicked.connect(self.refreshTree)
        self.treeWidgetMain.clicked.connect(self.treeClicked)

    def setUi(self):
        # Filter
        self.labelFilter.setPixmap(utils.getIconPath("filter"))
        self.labelFilter.setToolTip("Filter elements by asset <b>types and tasks</b>.")

        # Search
        self.labelSearch.setPixmap(utils.getIconPath("search"))
        self.labelSearch.setToolTip("Search elements with <b>part of name</b>.")

        # ComboBox asset type
        self.createFilterTypes()

        # ComboBox asset task
        self.createFilterTasks()

        # ComboBox asset fork
        self.createFilterForks()

        # ComboBox versions type
        self.createVersionType()

        # ComboBox versions
        self.comboBoxVersions.setDisabled(True)
        self.createVersions()

        # Create Workspace button
        self.buttonCreateWorkspaceToolBar.setIcon(QtGui.QIcon(utils.getIconPath("workspace")))
        self.buttonCreateWorkspaceToolBar.setToolTip("Create <b>Workspace</b>.")

        # Create Asset button
        self.buttonCreateAssetToolBar.setIcon(QtGui.QIcon(utils.getIconPath("addasset")))
        self.buttonCreateAssetToolBar.setToolTip("Create a new <b>Asset</b>.")

        # Create Task button
        self.buttonCreateTaskToolBar.setDisabled(True)
        self.buttonCreateTaskToolBar.setIcon(QtGui.QIcon(utils.getIconPath("addtask")))
        self.buttonCreateTaskToolBar.setToolTip("Add <b>Task(s)</b> to selected Asset.")

        # Push button
        self.buttonPushToolBar.setIcon(QtGui.QIcon(utils.getIconPath("push")))
        self.buttonPushToolBar.setToolTip("<b>Push</b> a task to the repository.")

        # Pull button
        self.buttonPullToolBar.setIcon(QtGui.QIcon(utils.getIconPath("pull")))
        self.buttonPullToolBar.setToolTip("<b>Pull</b> a task from the repository.")

        # Set status button
        self.buttonSetStatusToolBar.setIcon(QtGui.QIcon(utils.getIconPath("statuses")))
        self.buttonSetStatusToolBar.setToolTip("Set <b>Status</b>.")

        # Set delete/inactive button
        self.buttonDeleteAssetToolBar.setIcon(QtGui.QIcon(utils.getIconPath("disconnect")))
        self.buttonDeleteAssetToolBar.setToolTip("<b>Delete/inactive</b> an asset.")

        # Set active only checkBox
        self.checkBoxActive.setText("active only")
        self.checkBoxActive.setToolTip("Show only <b>active assets<\b>.")

        # Set tree
        self.treeWidgetMain.setSortingEnabled(True)
        self.treeWidgetMain.sortItems(0, QtCore.Qt.AscendingOrder)
        self.refreshTree()

        # Set refresh button
        self.buttonRefresh.setIcon(QtGui.QIcon(utils.getIconPath("refresh")))
        self.buttonRefresh.setToolTip("Refresh the tree with last elements from the DataBase.")

        # Title
        self.setWindowTitle(QtGui.QApplication.translate("Asset Manager", "Asset Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSystemTitle.setPixmap(utils.getIconPath(self.launcher))
        self.labelProjectTitle.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Project</span><span style=\" font-size:12pt;\"/><span style=\" font-size:12pt; font-weight:600;\">:</span><span style=\" font-size:12pt;\"> %s</span></p></body></html>" % (self.project), None, QtGui.QApplication.UnicodeUTF8))

def systemAM () :
    app = QtGui.QApplication (sys.argv)
    main = UiAssetManager()
    main.show()
    app.exec_()
    sys.exit()

if __name__ == '__main__':
    systemAM()
