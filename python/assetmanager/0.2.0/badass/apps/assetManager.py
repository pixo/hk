'''
Created on Jun 17, 2014

@author: pixo
'''
import sys, os
from PySide import QtCore, QtGui
import badass.utils as utils
import badass.core as core


class UiAssetManager( QtGui.QMainWindow ):

    iconsPath = None
    assetTypes = None
    launcher = "terminal"

    def __init__( self, parent = None ):
        super( UiAssetManager, self ).__init__( parent )

        self.setObjectName( "MainWindow" )
        self.resize( 1042, 878 )
        self.centralwidget = QtGui.QWidget( self )
        self.centralwidget.setObjectName( "centralwidget" )
        self.horizontalLayout_2 = QtGui.QHBoxLayout( self.centralwidget )
        self.horizontalLayout_2.setObjectName( "horizontalLayout_2" )
        self.verticalLayoutMain = QtGui.QVBoxLayout()
        self.verticalLayoutMain.setObjectName( "verticalLayoutMain" )
        self.horizontalLayoutTitle = QtGui.QHBoxLayout()
        self.horizontalLayoutTitle.setContentsMargins( 3, -1, 3, -1 )
        self.horizontalLayoutTitle.setObjectName( "horizontalLayoutTitle" )
        self.labelSystemTitle = QtGui.QLabel( self.centralwidget )
        self.labelSystemTitle.setMaximumSize( QtCore.QSize( 21, 16777215 ) )
        self.labelSystemTitle.setObjectName( "labelSystemTitle" )
        self.horizontalLayoutTitle.addWidget( self.labelSystemTitle )
        self.labelProjectTitle = QtGui.QLabel( self.centralwidget )
        self.labelProjectTitle.setObjectName( "labelProjectTitle" )
        self.horizontalLayoutTitle.addWidget( self.labelProjectTitle )
        self.verticalLayoutMain.addLayout( self.horizontalLayoutTitle )
        self.line1Main = QtGui.QFrame( self.centralwidget )
        self.line1Main.setFrameShadow( QtGui.QFrame.Sunken )
        self.line1Main.setLineWidth( 2 )
        self.line1Main.setFrameShape( QtGui.QFrame.HLine )
        self.line1Main.setFrameShadow( QtGui.QFrame.Sunken )
        self.line1Main.setObjectName( "line1Main" )
        self.verticalLayoutMain.addWidget( self.line1Main )
        self.horizontalLayoutCore = QtGui.QHBoxLayout()
        self.horizontalLayoutCore.setObjectName( "horizontalLayoutCore" )
        self.verticalLayoutLeft = QtGui.QVBoxLayout()
        self.verticalLayoutLeft.setSizeConstraint( QtGui.QLayout.SetDefaultConstraint )
        self.verticalLayoutLeft.setObjectName( "verticalLayoutLeft" )
        self.horizontalLayoutFilter = QtGui.QHBoxLayout()
        self.horizontalLayoutFilter.setContentsMargins( 3, -1, 3, -1 )
        self.horizontalLayoutFilter.setObjectName( "horizontalLayoutFilter" )
        self.labelFilter = QtGui.QLabel( self.centralwidget )
        self.labelFilter.setEnabled( True )
        self.labelFilter.setMaximumSize( QtCore.QSize( 16, 16 ) )
        self.labelFilter.setObjectName( "labelFilter" )
        self.horizontalLayoutFilter.addWidget( self.labelFilter )
        self.comboBoxAssetTypeFilter = QtGui.QComboBox( self.centralwidget )
        self.comboBoxAssetTypeFilter.setMinimumSize( QtCore.QSize( 100, 0 ) )
        self.comboBoxAssetTypeFilter.setMaximumSize( QtCore.QSize( 16777215, 16777215 ) )
        self.comboBoxAssetTypeFilter.setAccessibleName( "" )
        self.comboBoxAssetTypeFilter.setObjectName( "comboBoxAssetTypeFilter" )
        self.horizontalLayoutFilter.addWidget( self.comboBoxAssetTypeFilter )
        self.comboBoxAssetTaskFilter = QtGui.QComboBox( self.centralwidget )
        self.comboBoxAssetTaskFilter.setMinimumSize( QtCore.QSize( 100, 0 ) )
        self.comboBoxAssetTaskFilter.setMaximumSize( QtCore.QSize( 16777215, 16777215 ) )
        self.comboBoxAssetTaskFilter.setAccessibleName( "" )
        self.comboBoxAssetTaskFilter.setObjectName( "comboBoxAssetTaskFilter" )
        self.horizontalLayoutFilter.addWidget( self.comboBoxAssetTaskFilter )
        self.verticalLayoutLeft.addLayout( self.horizontalLayoutFilter )
        self.horizontalLayoutSearch = QtGui.QHBoxLayout()
        self.horizontalLayoutSearch.setContentsMargins( 3, -1, 3, -1 )
        self.horizontalLayoutSearch.setObjectName( "horizontalLayoutSearch" )
        self.labelSearch = QtGui.QLabel( self.centralwidget )
        self.labelSearch.setMaximumSize( QtCore.QSize( 16, 16 ) )
        self.labelSearch.setObjectName( "labelSearch" )
        self.horizontalLayoutSearch.addWidget( self.labelSearch )
        self.lineEditSearch = QtGui.QLineEdit( self.centralwidget )
        self.lineEditSearch.setObjectName( "lineEditSearch" )
        self.horizontalLayoutSearch.addWidget( self.lineEditSearch )
        self.verticalLayoutLeft.addLayout( self.horizontalLayoutSearch )
        self.horizontalLayoutExplorer = QtGui.QHBoxLayout()
        self.horizontalLayoutExplorer.setObjectName( "horizontalLayoutExplorer" )
        self.verticalLayoutToolBar = QtGui.QVBoxLayout()
        self.verticalLayoutToolBar.setObjectName( "verticalLayoutToolBar" )

        # Import button
        self.buttonImportToolBar = QtGui.QPushButton( self.centralwidget )
        self.buttonImportToolBar.setMinimumSize( QtCore.QSize( 24, 24 ) )
        self.buttonImportToolBar.setMaximumSize( QtCore.QSize( 24, 24 ) )
        self.buttonImportToolBar.setObjectName( "buttonImportToolBar" )
        self.verticalLayoutToolBar.addWidget( self.buttonImportToolBar )

        # Export button
        self.buttonExportToolBar = QtGui.QPushButton( self.centralwidget )
        self.buttonExportToolBar.setMinimumSize( QtCore.QSize( 24, 24 ) )
        self.buttonExportToolBar.setMaximumSize( QtCore.QSize( 24, 24 ) )
        self.buttonExportToolBar.setObjectName( "buttonExportToolBar" )
        self.verticalLayoutToolBar.addWidget( self.buttonExportToolBar )

        # Set status button
        self.buttonSetStatusToolBar = QtGui.QPushButton( self.centralwidget )
        self.buttonSetStatusToolBar.setMaximumSize( QtCore.QSize( 24, 24 ) )
        self.buttonSetStatusToolBar.setMaximumSize( QtCore.QSize( 24, 24 ) )
        self.buttonSetStatusToolBar.setObjectName( "buttonSetStatusToolBar" )
        self.verticalLayoutToolBar.addWidget( self.buttonSetStatusToolBar )

        # CreateAsset button
        self.buttonCreateAssetToolBar = QtGui.QPushButton( self.centralwidget )
        self.buttonCreateAssetToolBar.setMinimumSize( QtCore.QSize( 24, 24 ) )
        self.buttonCreateAssetToolBar.setMaximumSize( QtCore.QSize( 24, 24 ) )
        self.buttonCreateAssetToolBar.setToolTip( "" )
        self.buttonCreateAssetToolBar.setObjectName( "buttonCreateAssetToolBar" )
        self.verticalLayoutToolBar.addWidget( self.buttonCreateAssetToolBar )

        # CreateTask button
        self.buttonCreateTaskToolBar = QtGui.QPushButton( self.centralwidget )
        self.buttonCreateTaskToolBar.setMinimumSize( QtCore.QSize( 24, 24 ) )
        self.buttonCreateTaskToolBar.setMaximumSize( QtCore.QSize( 24, 24 ) )
        self.buttonCreateTaskToolBar.setToolTip( "" )
        self.buttonCreateTaskToolBar.setObjectName( "buttonCreateTaskToolBar" )
        self.verticalLayoutToolBar.addWidget( self.buttonCreateTaskToolBar )

        spacerItem = QtGui.QSpacerItem( 20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding )
        self.verticalLayoutToolBar.addItem( spacerItem )

        self.horizontalLayoutExplorer.addLayout( self.verticalLayoutToolBar )
        self.verticalLayoutTree = QtGui.QVBoxLayout()
        self.verticalLayoutTree.setObjectName( "verticalLayoutTree" )
        self.horizontalLayoutVersions = QtGui.QHBoxLayout()
        self.horizontalLayoutVersions.setObjectName( "horizontalLayoutVersions" )

        # VersionType comboBox
        self.comboBoxVersionType = QtGui.QComboBox( self.centralwidget )
        self.comboBoxVersionType.setMaximumSize( QtCore.QSize( 90, 16777215 ) )
        self.comboBoxVersionType.setAccessibleName( "" )
        self.comboBoxVersionType.setObjectName( "comboBoxVersionType" )
        self.horizontalLayoutVersions.addWidget( self.comboBoxVersionType )

        # Versions comboBox
        self.comboBoxVersions = QtGui.QComboBox( self.centralwidget )
        self.comboBoxVersions.setMaximumSize( QtCore.QSize( 70, 16777215 ) )
        self.comboBoxVersions.setAccessibleName( "" )
        self.comboBoxVersions.setObjectName( "comboBoxVersions" )
        self.horizontalLayoutVersions.addWidget( self.comboBoxVersions )

        # ActiveOnly CheckBox
        self.checkBoxActive = QtGui.QCheckBox( self.centralwidget )
        self.checkBoxActive.setEnabled( True )
        self.checkBoxActive.setChecked( True )
        self.checkBoxActive.setTristate( False )
        self.checkBoxActive.setObjectName( "checkBoxActive" )
        self.horizontalLayoutVersions.addWidget( self.checkBoxActive )

        spacerItem1 = QtGui.QSpacerItem( 40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
        self.horizontalLayoutVersions.addItem( spacerItem1 )

        # Refresh button
        self.buttonRefresh = QtGui.QPushButton( self.centralwidget )
        self.buttonRefresh.setMinimumSize( QtCore.QSize( 24, 24 ) )
        self.buttonRefresh.setMaximumSize( QtCore.QSize( 24, 24 ) )
        self.buttonRefresh.setObjectName( "buttonRefresh" )
        self.horizontalLayoutVersions.addWidget( self.buttonRefresh )

        self.verticalLayoutTree.addLayout( self.horizontalLayoutVersions )
        self.treeWidgetMain = QtGui.QTreeWidget( self.centralwidget )
        self.treeWidgetMain.setAlternatingRowColors( True )
        self.treeWidgetMain.setRootIsDecorated( True )
        self.treeWidgetMain.setAnimated( True )
        self.treeWidgetMain.setWordWrap( False )
        self.treeWidgetMain.setObjectName( "treeWidgetMain" )
        self.treeWidgetMain.header().setVisible( False )
        self.verticalLayoutTree.addWidget( self.treeWidgetMain )
        self.horizontalLayoutExplorer.addLayout( self.verticalLayoutTree )
        self.verticalLayoutLeft.addLayout( self.horizontalLayoutExplorer )
        self.horizontalLayoutCore.addLayout( self.verticalLayoutLeft )
        self.lineCore = QtGui.QFrame( self.centralwidget )
        self.lineCore.setLineWidth( 2 )
        self.lineCore.setMidLineWidth( 0 )
        self.lineCore.setFrameShape( QtGui.QFrame.VLine )
        self.lineCore.setFrameShadow( QtGui.QFrame.Sunken )
        self.lineCore.setObjectName( "lineCore" )
        self.horizontalLayoutCore.addWidget( self.lineCore )
        self.verticalLayoutInfos = QtGui.QVBoxLayout()
        self.verticalLayoutInfos.setObjectName( "verticalLayoutInfos" )
        self.labelImageInfos = QtGui.QLabel( self.centralwidget )
        self.labelImageInfos.setMinimumSize( QtCore.QSize( 300, 300 ) )
        self.labelImageInfos.setText( "" )
        self.labelImageInfos.setObjectName( "labelImageInfos" )
        self.verticalLayoutInfos.addWidget( self.labelImageInfos )
        self.lineInfos = QtGui.QFrame( self.centralwidget )
        self.lineInfos.setFrameShape( QtGui.QFrame.HLine )
        self.lineInfos.setFrameShadow( QtGui.QFrame.Sunken )
        self.lineInfos.setObjectName( "lineInfos" )
        self.verticalLayoutInfos.addWidget( self.lineInfos )
        self.plainTextEditInfos = QtGui.QPlainTextEdit( self.centralwidget )
        self.plainTextEditInfos.setEnabled( False )
        self.plainTextEditInfos.setPlainText( "" )
        self.plainTextEditInfos.setObjectName( "plainTextEditInfos" )
        self.verticalLayoutInfos.addWidget( self.plainTextEditInfos )
        self.horizontalLayoutCore.addLayout( self.verticalLayoutInfos )
        self.verticalLayoutMain.addLayout( self.horizontalLayoutCore )
        self.line2Main = QtGui.QFrame( self.centralwidget )
        self.line2Main.setFrameShape( QtGui.QFrame.HLine )
        self.line2Main.setFrameShadow( QtGui.QFrame.Sunken )
        self.line2Main.setObjectName( "line2Main" )
        self.verticalLayoutMain.addWidget( self.line2Main )
        self.horizontalLayoutStatus = QtGui.QHBoxLayout()
        self.horizontalLayoutStatus.setObjectName( "horizontalLayoutStatus" )
        self.progressBarStatus = QtGui.QProgressBar( self.centralwidget )
        self.progressBarStatus.setEnabled( True )
        self.progressBarStatus.setProperty( "value", 0 )
        self.progressBarStatus.setObjectName( "progressBarStatus" )
        self.progressBarStatus.setVisible( False )
        self.horizontalLayoutStatus.addWidget( self.progressBarStatus )
        self.verticalLayoutMain.addLayout( self.horizontalLayoutStatus )
        self.horizontalLayout_2.addLayout( self.verticalLayoutMain )
        self.setCentralWidget( self.centralwidget )
        self.statusbar = QtGui.QStatusBar( self )
        self.statusbar.setObjectName( "statusbar" )
        self.setStatusBar( self.statusbar )

        # TODO:Clean it
        self.db = utils.getDb()
        self.user = utils.getCurrentUser()
        self.dbUsers = core.getProjectUsers ( self.db )
        self.userStatus = self.dbUsers[self.user]
        self.project = utils.getProjectName()
        self.iconsPath = utils.getCCPath()
        self.assetTypes = utils.getAssetTypes()
        self.assetTasks = utils.getAssetTasks()
        self.versionTypes = ( "review", "release" )

        self.retranslateUi()
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName( self )


    def createFilterTypes( self ):
        """Create the type comboBox"""
        items = self.assetTypes
        items = sorted( [( key, value ) for ( key, value ) in items.items()] )
        items = [( "assets", "asset" )] + items

        # Set the types items
        for couple in items :
            icon = os.path.join( self.iconsPath, couple[1] + ".png" )
            self.comboBoxAssetTypeFilter.addItem( QtGui.QIcon( icon ), couple[0] )


    def createFilterTasks( self ):
        """Create the tasks comboBox"""
        items = self.assetTasks
        items = sorted( [( key, value ) for ( key, value ) in items.items()] )
        items = [( "tasks", "task" )] + items
        # Set the tasks items
        for couple in items :
            icon = os.path.join( self.iconsPath, couple[1] + ".png" )
            self.comboBoxAssetTaskFilter.addItem( QtGui.QIcon( icon ), couple[0] )

    def createVersionType( self ):
        """Create the versiontype comboBox"""
        items = self.versionTypes
        # Create the version types
        for item in items :
            icon = os.path.join( self.iconsPath, item + ".png" )
            self.comboBoxVersionType.addItem( QtGui.QIcon( icon ), item )

    def createVersions( self ):
        """Create the versiontype comboBox"""
        items = ( "001", "002" )
        self.comboBoxVersions.addItems( items )

    def getTasksByAsset( self ):
        tasks = dict()
        for task in self.allTasks:
            slug = self.allTasks[task]["name"]
            if not ( slug in tasks ) :
                tasks[slug] = list()
            tasks[slug].append( self.allTasks[task] )
        return tasks

    def getStatusColor( self, status ):
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
        return ( color, stat )

    def getGlobalStatusColor( self, status ):
        ns = list()
        app = list()

        color = QtCore.Qt.darkRed
        for i in status:
            if i == "ns" :
                ns.append( i )
            elif i == "app" :
                app.append( i )

        if len( ns ) == len( status ):
            color = QtCore.Qt.darkGray
        elif len( app ) == len( status ):
            color = QtCore.Qt.darkGreen

        return color

    def createTree( self ):
        assetTasks = dict( {"tasks":"task"}.items() + self.assetTasks.items() )
        assetTasksSwap = dict( ( value, key ) for key, value in assetTasks.iteritems() )
        self.tasksByAsset = self.getTasksByAsset()

        # Clear the tree
        self.treeWidgetMain.clear()

        # Set the asset items fonts
        assetFont = QtGui.QFont ()
        assetFont.setPointSize ( 10 )
        assetFont.setWeight ( 75 )
        assetFont.setItalic ( False )
        assetFont.setBold ( True )

        # Set the task items fonts
        taskFont = QtGui.QFont ()
        taskFont.setBold ( True )

        # Inactive color
        redbrush = QtGui.QBrush()
        redbrush.setColor( QtGui.QColor( 1, 0.5, 0.5 ) )

        # Create the items
        for asset in self.allAssets :
            values = self.allAssets[asset]
            slug = values["name"]
            assetType = values["type"]

            # Create Asset items
            assetIcon = os.path.join ( self.iconsPath, assetType + ".png" )
            assetIcon = QtGui.QIcon( assetIcon )
            assetItem = QtGui.QTreeWidgetItem ( self.treeWidgetMain )
            assetItem.setIcon( 0, assetIcon )
            assetItem.setFont( 0, assetFont )
            assetItem.setText( 0, slug )
            if values["inactive"]:
                assetItem.setBackground( 0, QtGui.QBrush( QtCore.Qt.red, QtCore.Qt.Dense4Pattern ) )
            assetItem.type = assetType
            assetItem.task = False
            assetItem.id = values["_id"]

            # Create Task items
            globStat = list()
            for task in self.tasksByAsset[slug]:
                assetTask = task["task"]
                taskIcon = os.path.join( self.iconsPath, assetTask + ".png" )
                taskIcon = QtGui.QIcon( taskIcon )
                taskItem = QtGui.QTreeWidgetItem( assetItem )
                taskItem.type = assetType
                taskItem.task = assetTask
                taskItem.id = task["_id"]
                taskItem.setIcon( 0, QtGui.QIcon( taskIcon ) )
                taskItem.setText( 0, assetTasksSwap[assetTask] )
                taskItem.setFont( 0, taskFont )
                stat = self.getStatusColor( task["status"] )
                taskColor = stat[0]
                globStat.append( stat[1] )
                taskItem.setForeground( 0, QtGui.QBrush( taskColor ) )
                if values["inactive"]:
                    taskItem.setBackground( 0, QtGui.QBrush( QtCore.Qt.red, QtCore.Qt.Dense6Pattern ) )

            assetColor = self.getGlobalStatusColor( globStat )
            assetItem.setForeground( 0, QtGui.QBrush( assetColor ) )

        self.filterTree()

    def filterTree( self ):
        it = QtGui.QTreeWidgetItemIterator( self.treeWidgetMain )
        text = self.lineEditSearch.text()
        assetTypes = dict( {"assets":"asset"}.items() + self.assetTypes.items() )
        currentType = self.comboBoxAssetTypeFilter.currentText()
        currentType = assetTypes[currentType]
        currentTask = self.comboBoxAssetTaskFilter.currentText()
        activeOnly = self.checkBoxActive.isChecked()

        while it.value () :
            item = it.value()
            item.setHidden( False )
            slug = item.text( 0 )

            if not item.task :
                if activeOnly :
                    values = self.allAssets[item.id]
                    item.setHidden( values["inactive"] )

                if not ( currentType in ( "asset", item.type ) ):
                    item.setHidden( True )

                if slug != "" and slug.find( text ) < 0:
                    item.setHidden( True )
            else :
                if not ( currentTask in ( "tasks", item.task ) ):
                    item.setHidden( True )

            it.next ()

    def refreshTree ( self ):
        self.allAssets = utils.lsDb( self.db, "asset", self.project )
        self.allTasks = utils.lsDb( self.db, "task", self.project )
        self.createTree()

    def signalConnect( self ):
        self.comboBoxAssetTypeFilter.currentIndexChanged.connect( self.filterTree )
        self.comboBoxAssetTaskFilter.currentIndexChanged.connect( self.filterTree )
        self.lineEditSearch.textChanged.connect( self.filterTree )
        self.buttonRefresh.clicked.connect( self.refreshTree )
        self.checkBoxActive.released.connect( self.refreshTree )

    def retranslateUi( self ):
        # Title
        self.setWindowTitle( QtGui.QApplication.translate( "MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.labelSystemTitle.setPixmap( os.path.join( self.iconsPath, self.launcher + ".png" ) )
        self.labelProjectTitle.setText( QtGui.QApplication.translate( "MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Project</span><span style=\" font-size:12pt;\"/><span style=\" font-size:12pt; font-weight:600;\">:</span><span style=\" font-size:12pt;\"> %s</span></p></body></html>" % self.project, None, QtGui.QApplication.UnicodeUTF8 ) )

        # Filter
        self.labelFilter.setPixmap( os.path.join ( self.iconsPath, "filter.png" ) )
        self.labelFilter.setToolTip( "Filter elements by asset <b>types and tasks</b>." )

        # Search
        self.labelSearch.setPixmap( os.path.join ( self.iconsPath, "search.png" ) )
        self.labelSearch.setToolTip( "Search elements with <b>part of name</b>." )

        # ComboBox asset type
        self.createFilterTypes()

        # ComboBox asset task
        self.createFilterTasks()

        # ComboBox versions type
        self.createVersionType()

        # ComboBox versions
        self.createVersions()

        # Create Asset button
        self.buttonCreateAssetToolBar.setIcon( QtGui.QIcon( os.path.join ( self.iconsPath, "addasset.png" ) ) )
        self.buttonCreateAssetToolBar.setToolTip( "Create a new <b>Asset</b>." )

        # Create Task button
        self.buttonCreateTaskToolBar.setIcon( QtGui.QIcon( os.path.join ( self.iconsPath, "addtask.png" ) ) )
        self.buttonCreateTaskToolBar.setToolTip( "Create new <b>Task(s)</b>." )

        # Export button
        self.buttonExportToolBar.setIcon( QtGui.QIcon( os.path.join ( self.iconsPath, "push.png" ) ) )
        self.buttonExportToolBar.setToolTip( "<b>Publish</b> a task." )

        # Import button
        self.buttonImportToolBar.setIcon( QtGui.QIcon( os.path.join ( self.iconsPath, "pull.png" ) ) )
        self.buttonImportToolBar.setToolTip( "<b>Import</b> a task." )

        # Set status button
        self.buttonSetStatusToolBar.setIcon( QtGui.QIcon( os.path.join ( self.iconsPath, "statuses.png" ) ) )
        self.buttonSetStatusToolBar.setToolTip( "Set <b>Status</b>." )

        # Set active only checkBox
        self.checkBoxActive.setText( "active only" )
        self.checkBoxActive.setToolTip( "Show only <b>active assets<\b>." )

        # Set tree
        self.refreshTree()

        # Set refresh button
        self.buttonRefresh.setIcon( QtGui.QIcon( os.path.join ( self.iconsPath, "refresh.png" ) ) )
        self.buttonRefresh.setToolTip( "Refresh the tree with last elements from the DataBase." )

        # Set status bar
        self.statusbar.showMessage( "Welcome '%s' you are logged as '%s'." % ( self.user, self.userStatus ) )

        self.treeWidgetMain.setSortingEnabled( True )
        self.treeWidgetMain.sortItems( 0, QtCore.Qt.AscendingOrder )


def systemAM () :
    app = QtGui.QApplication ( sys.argv )
    main = UiAssetManager()
    main.show()
    app.exec_()
    sys.exit()

if __name__ == '__main__':
    systemAM()
