import sys, os

from PySide import QtCore, QtGui
import badass.utils as utils
import badass.core as core

# try :
#     CC_PATH = utils.getCCPath()
# except:
#     CC_PATH = "/tmp"
#     print "assetManager module: Can't set CC_PATH \n set CC_PATH > /tmp"
#
# try :
#     PROJECT = utils.getProjectName()
# except:
#     PROJECT = "temp"
#     print "assetManager module: Can't set PROJECT \n set PROJECT > tmp"

# TODO: Add image reference task
# TODO: create ui for shot creation
# TODO: preview obj with meshlab

class UiPush ( QtGui.QWidget ) :

    pushTask = { "texture": core.texturePush }

    def searchLineChanged ( self, lineEdit, listWidget ) :
        filtr = lineEdit.text()
        if filtr != "" :

            for i in range( 0, listWidget.count() ):
                text = listWidget.item( i ).text()
                item = listWidget.item( i )

                if text.find( filtr ) >= 0 :
                    item.setHidden ( False )

                else:
                    item.setHidden ( True )

        else:

            for i in range( 0, listWidget.count() ):
                item = listWidget.item( i )
                item.setHidden( False )

    def fileLineChanged ( self ) :
        self.searchLineChanged( self.lineEdit_file, self.listWidget_file )

    def createWidgetList( self ):
        self.workspace = core.getPathFromId ( self.doc_id, True )
        lsdir = os.listdir ( self.workspace )
        dictpath = dict()

        for fil in lsdir :
            path = os.path.join ( self.workspace, fil )

            if os.path.isfile ( path ) :
                dictpath [ fil] = path

        self.dictpath = dictpath
        lspath = list()

        for key in self.dictpath:
            lspath.append( key )

        self.listWidget_file.addItems( lspath )
        self.listWidget_file.setSortingEnabled( True )

    def liswidget_clicked( self ):
        pass

    def pushClicked( self ):

        item = self.listWidget_file.currentItem ()

        if type ( item ) == type ( None ) :
            self.labelStatus.setText ( "Please select an item to publish" )

        else:
            lspush = list ()
            self.progressBar.setHidden ( False )
            self.progressBar.setValue ( 0 )
            lspush.append ( self.dictpath[ item.text () ] )
            description = self.plainTextEdit_description.toPlainText ()

            if self.task in self.pushTask :
                push = self.pushTask [ self.task ]
            else:
                push = core.push

            push( self.db, self.doc_id, lspush, description, self.progressBar,
                  self.labelStatus.setText )

            self.progressBar.setHidden ( True )
            self.labelStatus.setText ( "Done" )
            self.close()

    def descriptionChanged( self ):
        description = self.plainTextEdit_description.toPlainText ()

        if description == "" :
            self.pushButton.setEnabled ( False )

        else :
            self.pushButton.setEnabled ( True )

    def checkBoxClicked ( self ):
        print "checked"

    def signalConnect( self ):
        """ Connect the UI to the Ui_AssetWindow methods """
        self.pushButton.clicked.connect ( self.pushClicked )
        self.lineEdit_file.textChanged.connect ( self.fileLineChanged )
        self.plainTextEdit_description.textChanged.connect ( self.descriptionChanged )
        self.listWidget_file.clicked.connect ( self.liswidget_clicked )
        self.checkBox.clicked.connect ( self.checkBoxClicked )

    def __init__( self, parent = None, db = None, item = "" ):
        super ( UiPush, self ).__init__( parent )

        self.setObjectName ( "Form" )
        self.resize ( 600, 600 )
        self.verticalLayout_2 = QtGui.QVBoxLayout ( self )
        self.verticalLayout_2.setObjectName( "verticalLayout_2" )
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName( "verticalLayout_main" )
        self.horizontalLayout_center = QtGui.QHBoxLayout()
        self.horizontalLayout_center.setObjectName( "horizontalLayout_center" )
        self.verticalLayout_file = QtGui.QVBoxLayout()
        self.verticalLayout_file.setObjectName( "verticalLayout_file" )
        self.label_proj = QtGui.QLabel( self )
        self.label_proj.setObjectName( "label_proj" )
        self.verticalLayout_file.addWidget( self.label_proj )
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName( "horizontalLayout" )
        self.checkBox = QtGui.QCheckBox( self )
        self.checkBox.setObjectName( "checkBox" )
        self.horizontalLayout.addWidget( self.checkBox )
        self.label_search = QtGui.QLabel( self )
        self.label_search.setMaximumSize( QtCore.QSize( 16, 16 ) )
        self.label_search.setObjectName( "label_search" )
        self.horizontalLayout.addWidget( self.label_search )
        self.lineEdit_file = QtGui.QLineEdit( self )
        self.lineEdit_file.setObjectName( "lineEdit_file" )
        self.horizontalLayout.addWidget( self.lineEdit_file )
        self.verticalLayout_file.addLayout( self.horizontalLayout )
        self.listWidget_file = QtGui.QListWidget( self )
        self.listWidget_file.setMinimumSize( QtCore.QSize( 300, 0 ) )
        self.listWidget_file.setObjectName( "listWidget_file" )
        self.verticalLayout_file.addWidget( self.listWidget_file )
        self.horizontalLayout_center.addLayout( self.verticalLayout_file )
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName( "verticalLayout" )
        self.label_description = QtGui.QLabel( self )
        self.label_description.setAlignment( QtCore.Qt.AlignCenter )
        self.label_description.setObjectName( "label_description" )
        self.verticalLayout.addWidget( self.label_description )
        self.plainTextEdit_description = QtGui.QPlainTextEdit( self )
        self.plainTextEdit_description.setMinimumSize ( QtCore.QSize ( 300, 300 ) )
        self.plainTextEdit_description.setObjectName( "plainTextEdit_description" )
        self.verticalLayout.addWidget( self.plainTextEdit_description )
        self.horizontalLayout_center.addLayout( self.verticalLayout )
        self.verticalLayout_main.addLayout( self.horizontalLayout_center )
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName( "horizontalLayout_bottom" )
        self.progressBar = QtGui.QProgressBar( self )
        self.progressBar.setMinimumSize( QtCore.QSize( 550, 0 ) )
        self.progressBar.setProperty( "value", 0 )
        self.progressBar.setTextVisible( True )
        self.progressBar.setInvertedAppearance( False )
        self.progressBar.setTextDirection( QtGui.QProgressBar.TopToBottom )
        self.progressBar.setObjectName( "progressBar" )
        self.horizontalLayout_bottom.addWidget( self.progressBar )
        spacerItem = QtGui.QSpacerItem ( 40, 20, QtGui.QSizePolicy.Expanding,
                                         QtGui.QSizePolicy.Minimum )
        self.horizontalLayout_bottom.addItem( spacerItem )
        self.pushButton = QtGui.QPushButton( self )
        self.pushButton.setMaximumSize( QtCore.QSize( 60, 16777215 ) )
        self.pushButton.setObjectName( "pushButton" )
        self.horizontalLayout_bottom.addWidget( self.pushButton )
        self.verticalLayout_main.addLayout( self.horizontalLayout_bottom )
        self.labelStatus = QtGui.QLabel( self )
        self.labelStatus.setText( "" )
        self.labelStatus.setObjectName( "labelStatus" )
        self.verticalLayout_main.addWidget( self.labelStatus )
        self.verticalLayout_2.addLayout( self.verticalLayout_main )

        # Default setup
        self.item = item
        self.task = item.parent().text( 0 )
        self.doc_id = item.hkid
        self.db = db
        self.setWindowTitle ( "Asset Pusher" )

        self.label_proj.setText ( """<html><head/><body><p><span style=\" 
                                font-size:12pt; font-weight:600;\">Asset Push :
                                </span><span style=\" font-size:12pt;
                                \"> '%s'</span></p></body></html>""" % self.doc_id )

        self.label_description.setText ( """<html><head/><body><p><span style=
                                    \" font-weight:600;\">Description</span>
                                    </p></body></html>""" )

        self.listWidget_file.setSortingEnabled ( True )
        self.checkBox.setIcon( QtGui.QIcon( utils.getIconPath( "all" ) ) )
        self.checkBox.setVisible( False )
        self.progressBar.setHidden( True )
        self.label_search.setPixmap( utils.getIconPath( "search" ) )
        self.pushButton.setText( "Push" )
        self.pushButton.setDisabled( True )
        icon_push = QtGui.QIcon( utils.getIconPath( "push" ) )
        self.pushButton.setIcon( icon_push )
        self.createWidgetList()
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName( self )

class UiPushLs ( UiPush ) :

    def checkBoxClicked ( self ):
        checkState = self.checkBox.checkState ()
        for i in range( 0, self.listWidget_file.count () ):
            self.listWidget_file.item( i ).setCheckState( checkState )

    def createWidgetList( self ):
        self.checkBox.setVisible ( True )
        self.workspace = core.getPathFromId ( self.doc_id, True )
        self.dictpath = utils.lsSeq ( self.workspace )

        lspath = list ()
        for key in self.dictpath:
            lspath.append( key )

        self.listWidget_file.addItems( lspath )

        font = QtGui.QFont ()
        font.setPointSize ( 9 )
        font.setWeight ( 75 )
        font.setBold ( True )

        for i in range( 0, self.listWidget_file.count() ):
            item = self.listWidget_file.item( i )
            item.setCheckState( QtCore.Qt.Unchecked )
            if item.text().find( os.sep ) > -1:
                item.setFont( font )

    def pushClicked( self ):
        lspush = list ()
        self.progressBar.setHidden ( False )
        self.progressBar.setValue ( 0 )

        for i in range( 0, self.listWidget_file.count() ):
            item = self.listWidget_file.item ( i )

            if item.checkState() == QtCore.Qt.CheckState.Checked :
                lspush.extend ( self.dictpath [ item.text () ] )

        description = self.plainTextEdit_description.toPlainText ()

        if self.task in self.pushTask :
            push = self.pushTask[self.task]
        else:
            push = core.push

        push ( self.db, self.doc_id, lspush, description, self.progressBar,
               self.labelStatus.setText, rename = False )

        self.progressBar.setHidden ( True )
        self.labelStatus.setText ( "Done" )
        self.close ()

class UiPush3dPack ( QtGui.QWidget ) :


    screenshot = utils.getIconPath( "hk_title_medium" )

    def __init__( self, parent = None, db = None, doc_id = "", item = "" ):
        super ( UiPush3dPack, self ).__init__( parent )

        self.setObjectName( "Form" )
        self.resize( 394, 666 )
        self.verticalLayout_2 = QtGui.QVBoxLayout( self )
        self.verticalLayout_2.setObjectName( "verticalLayout_2" )
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName( "verticalLayout_main" )
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName( "verticalLayout_3" )
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName( "horizontalLayout_2" )
        self.label_launcher = QtGui.QLabel( self )
        self.label_launcher.setMaximumSize( QtCore.QSize( 21, 21 ) )
        self.label_launcher.setText( "" )
        self.label_launcher.setObjectName( "label_launcher" )
        self.horizontalLayout_2.addWidget( self.label_launcher )
        self.label_proj = QtGui.QLabel( self )
        self.label_proj.setObjectName( "label_proj" )
        self.horizontalLayout_2.addWidget( self.label_proj )
        self.verticalLayout_3.addLayout( self.horizontalLayout_2 )
        self.labelImage = QtGui.QLabel ( self )
        self.labelImage.setText ( "" )
        self.labelImage.setObjectName ( "labelImage" )
        self.verticalLayout_3.addWidget ( self.labelImage )
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName( "horizontalLayout" )
        spacerItem = QtGui.QSpacerItem( 40, 20, QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Minimum )
        self.horizontalLayout.addItem( spacerItem )
        self.screenshotButton = QtGui.QPushButton( self )
        self.screenshotButton.setObjectName( "screenshotButton" )
        self.horizontalLayout.addWidget( self.screenshotButton )
        self.verticalLayout_3.addLayout( self.horizontalLayout )
        self.label_comments = QtGui.QLabel( self )
        self.label_comments.setAlignment( QtCore.Qt.AlignCenter )
        self.label_comments.setObjectName( "label_comments" )
        self.verticalLayout_3.addWidget( self.label_comments )
        self.plainTextEdit_comments = QtGui.QPlainTextEdit( self )
        self.plainTextEdit_comments.setMinimumSize( QtCore.QSize( 300, 0 ) )
        self.plainTextEdit_comments.setObjectName( "plainTextEdit_comments" )
        self.verticalLayout_3.addWidget( self.plainTextEdit_comments )
        self.verticalLayout_main.addLayout( self.verticalLayout_3 )
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName( "horizontalLayout_bottom" )
        self.progressBar = QtGui.QProgressBar( self )
        self.progressBar.setMinimumSize( QtCore.QSize( 300, 0 ) )
        self.progressBar.setProperty( "value", 0 )
        self.progressBar.setTextVisible( True )
        self.progressBar.setInvertedAppearance( False )
        self.progressBar.setTextDirection( QtGui.QProgressBar.TopToBottom )
        self.progressBar.setObjectName( "progressBar" )
        self.horizontalLayout_bottom.addWidget( self.progressBar )
        spacerItem1 = QtGui.QSpacerItem ( 40, 20, QtGui.QSizePolicy.Expanding,
                                          QtGui.QSizePolicy.Minimum )
        self.horizontalLayout_bottom.addItem( spacerItem1 )
        self.pushButton = QtGui.QPushButton( self )
        self.pushButton.setMaximumSize( QtCore.QSize( 60, 16777215 ) )
        self.pushButton.setObjectName( "pushButton" )
        self.horizontalLayout_bottom.addWidget( self.pushButton )
        self.verticalLayout_main.addLayout( self.horizontalLayout_bottom )
        self.labelStatus = QtGui.QLabel( self )
        self.labelStatus.setText( "" )
        self.labelStatus.setObjectName( "labelStatus" )
        self.verticalLayout_main.addWidget( self.labelStatus )
        self.verticalLayout_2.addLayout( self.verticalLayout_main )

        self.item = item
        self.db = db
        self.doc_id = doc_id
        self.setupUi()
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName( self )

    def setupUi( self ):
        self.setWindowTitle( "Asset Push" )

        self.label_proj.setText( """<html><head/><body><p><span style=\" font-size:12pt;
                                font-weight:600;\">Push Asset :</span><span style=\"
                                font-size:12pt;\"> '%s'</span></p></body></html>""" % self.doc_id )

        self.label_comments.setText( """<html><head/><body><p><span style=\" font-weight:600;
                                    \">User comments</span></p></body></html>""" )

        self.progressBar.setHidden ( True )

        self.label_launcher.setPixmap( utils.getIconPath( self.launcher ) )
        self.pushButton.setText ( "Push" )
        icon_push = QtGui.QIcon ( utils.getIconPath( "push" ) )
        self.pushButton.setIcon ( icon_push )
        self.pushButton.setDisabled ( True )

        self.screenshotButton.setText( "Screenshot" )
        icon_push_2 = QtGui.QIcon ( utils.getIconPath( "screenshot" ) )
        self.screenshotButton.setIcon ( icon_push_2 )

        self.labelImage.setPixmap ( self.screenshot )

    def signalConnect( self ):
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


    def pushButtonClicked( self ):
        print "push button clicked"
        self.close ()

    def plainTextEditChanged( self ):
        descriptions = self.plainTextEdit.toPlainText()
        if descriptions == "" :
            self.pushButton.setEnabled( False )
        else :
            self.pushButton.setEnabled( True )

    def signalConnect( self ):
        self.pushButton.clicked.connect ( self.pushButtonClicked )
        self.plainTextEdit.textChanged.connect ( self.plainTextEditChanged )


    def __init__( self, parent = None, typ = ( "Type", "typ" ) ):
        super( UiCreateOnDb, self ).__init__( parent )

        self.typ = typ
        self.setObjectName( "Form" )
        self.resize( 486, 429 )
        self.setWindowTitle( "Create on database" )
        self.verticalLayout_2 = QtGui.QVBoxLayout( self )
        self.verticalLayout_2.setObjectName( "verticalLayout_2" )
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName( "verticalLayout" )
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName( "horizontalLayout" )
        self.label_lineedit = QtGui.QLabel( self )
        self.label_lineedit.setObjectName( "label_lineedit" )
        self.label_lineedit.setText( "Create new %s" % self.typ[0] )
        self.horizontalLayout.addWidget( self.label_lineedit )
        self.lineEdit = QtGui.QLineEdit( self )
        self.lineEdit.setObjectName( "lineEdit" )
        self.horizontalLayout.addWidget( self.lineEdit )
        self.pushButton = QtGui.QPushButton( self )
        self.pushButton.setObjectName( "pushButton" )
        self.pushButton.setText( "create" )
        self.pushButton.setToolTip( "Make sure to create a description" )
        self.pushButton.setEnabled( False )
        self.horizontalLayout.addWidget( self.pushButton )
        self.verticalLayout.addLayout( self.horizontalLayout )
        self.label_description = QtGui.QLabel( self )
        self.label_description.setObjectName( "label_description" )
        self.label_description.setText( "Description:" )
        self.verticalLayout.addWidget( self.label_description )
        self.plainTextEdit = QtGui.QPlainTextEdit( self )
        self.plainTextEdit.setObjectName( "plainTextEdit" )
        self.verticalLayout.addWidget( self.plainTextEdit )
        self.label_status = QtGui.QLabel( self )
        self.label_status.setObjectName( "label_status" )
        self.label_status.setText( "" )
        self.verticalLayout.addWidget( self.label_status )
        self.verticalLayout_2.addLayout( self.verticalLayout )
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName( self )


class UiCreateAsset ( UiCreateOnDb ):

    def pushButtonClicked( self ):
        self.label_status.setText ( "" )
        dbtyp = self.typ [1]
        name = self.lineEdit.text()

        if name == "":
            msg = "Can't create asset '%s' no characters in name"
            self.label_status.setText( msg % name )
            return

        if name.find( "_" ) >= 0:
            msg = "Can't create asset '%s' name shouldn't contain underscore"
            self.label_status.setText( msg % name )
            return

        if name.find( " " ) >= 0:
            msg = "Can't create asset '%s' name shouldn't contain space"
            self.label_status.setText( msg % name )
            return

        description = self.plainTextEdit.toPlainText()
        doc_id = "%s_%s_%s" % ( utils.getProjectName(), dbtyp, name )
        doc = core.createAsset ( doc_id = doc_id, description = description )

        if doc :
            self.lineEdit.setText( "" )
            self.label_status.setText( "%s created" % doc_id )

        self.close ()


class UiCreateTask ( QtGui.QWidget ) :


    def pushButtonClicked ( self ) :

        tasks = utils.getAssetTasks ()
        dbtyp = self.typ[1]
        fork = self.lineEdit_fork.text()
        description = self.plainTextEdit_comments.toPlainText()

        if fork != "" :

            for i in range ( 0, self.listWidget_task.count() ):
                item = self.listWidget_task.item ( i )

                if item.checkState () == QtCore.Qt.CheckState.Checked :
                    task = tasks [ item.text () ]
                    doc_id = "%s_%s_%s" % ( dbtyp, task, fork )
                    doc = core.createTask ( doc_id = doc_id, description = description )

                    if doc :
                        self.labelStatus.setText ( "%s created" % doc_id )

            self.close ()

        else :
            self.labelStatus.setText ( "Please provide a Fork name" )

    def createListWidget ( self ) :
        """Clear previous task list"""
        self.listWidget_task.clear ()

        """Get fork lineEdit """
        fork = self.lineEdit_fork.text()

        """Get asset id"""
        asset_id = self.typ[1].replace ( os.getenv ( "HK_PROJECT" ) + "_", "" )

        """Get Description test"""
        textdoc = self.plainTextEdit_comments.document ()
        description = textdoc.toPlainText ()

        if fork != "" :

            """Check if description is not empty to enable it"""
            if description != "":
                self.pushButton.setEnabled ( True )

            else:
                self.pushButton.setEnabled ( False )

            """Create task items"""
            for i in self.taskTypes :
                self.listWidget_task.addItem ( i )

            """Set task status"""
            for i in range ( 0, self.listWidget_task.count () ) :
                """get items task"""
                item = self.listWidget_task.item ( i )

                """get item name"""
                itemText = item.text ()

                """create task id from asset id, item text and fork line """
                itemId = self.taskTypes [ itemText ]
                task = "%s_%s_%s" % ( asset_id, itemId, fork, )
                icon = utils.getIconPath( itemId )
                item.setIcon ( QtGui.QIcon ( icon ) )

                """if task exist change bg color"""
                if not ( task in self.tasks ) :
                    item.setCheckState ( QtCore.Qt.Unchecked )
                else:
                    item.setBackground ( QtGui.QColor ( 128, 255, 128 ) )

        else :
            """Set create button false if fork is empty"""
            self.pushButton.setEnabled ( False )



    def signalConnect ( self ) :
        self.pushButton.clicked.connect ( self.pushButtonClicked )
        self.lineEdit_fork.textChanged.connect ( self.createListWidget )
        self.plainTextEdit_comments.textChanged.connect ( self.commentsChanged )

    def commentsChanged ( self ) :

        textdoc = self.plainTextEdit_comments.document ()
        fork = self.lineEdit_fork.text ()
        description = textdoc.toPlainText ()

        if description == "" or fork == "":
            self.pushButton.setEnabled ( False )

        else :
            self.pushButton.setEnabled ( True )

    def __init__( self, parent = None, db = None, typ = ( "Type", "typ" ) ):
        super ( UiCreateTask, self ).__init__( parent )

        self.db = db
        self.typ = typ
        self.tasks = utils.lsDb ( self.db, "task", self.typ[1] )
        self.taskTypes = utils.getAssetTasks ()

        self.setWindowTitle ( "Create Task" )
        self.setObjectName ( "Form" )
        self.resize ( 803, 593 )
        self.verticalLayout_2 = QtGui.QVBoxLayout( self )
        self.verticalLayout_2.setObjectName( "verticalLayout_2" )
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName( "verticalLayout_main" )
        self.horizontalLayout_center = QtGui.QHBoxLayout()
        self.horizontalLayout_center.setObjectName( "horizontalLayout_center" )
        self.verticalLayout_file = QtGui.QVBoxLayout()
        self.verticalLayout_file.setObjectName( "verticalLayout_file" )
        self.label_proj = QtGui.QLabel( self )
        self.label_proj.setObjectName( "label_proj" )
        self.verticalLayout_file.addWidget( self.label_proj )
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName( "horizontalLayout" )
        self.label_fork = QtGui.QLabel( self )
        self.label_fork.setMinimumSize( QtCore.QSize( 30, 0 ) )
        self.label_fork.setMaximumSize( QtCore.QSize( 16, 16 ) )
        self.label_fork.setObjectName( "label_fork" )
        self.horizontalLayout.addWidget( self.label_fork )
        self.lineEdit_fork = QtGui.QLineEdit( self )
        self.lineEdit_fork.setObjectName( "lineEdit_fork" )
        self.horizontalLayout.addWidget( self.lineEdit_fork )
        self.verticalLayout_file.addLayout( self.horizontalLayout )
        self.listWidget_task = QtGui.QListWidget( self )
        self.listWidget_task.setMinimumSize( QtCore.QSize( 300, 0 ) )
        self.listWidget_task.setObjectName( "listWidget_task" )
        self.listWidget_task.setAlternatingRowColors( True )
        self.verticalLayout_file.addWidget( self.listWidget_task )
        self.horizontalLayout_center.addLayout( self.verticalLayout_file )
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName( "verticalLayout" )
        self.label_comments = QtGui.QLabel( self )
        self.label_comments.setAlignment( QtCore.Qt.AlignCenter )
        self.label_comments.setObjectName( "label_comments" )
        self.verticalLayout.addWidget( self.label_comments )
        self.plainTextEdit_comments = QtGui.QPlainTextEdit( self )
        self.plainTextEdit_comments.setMinimumSize( QtCore.QSize( 300, 0 ) )
        self.plainTextEdit_comments.setObjectName( "plainTextEdit_comments" )
        self.verticalLayout.addWidget( self.plainTextEdit_comments )
        self.horizontalLayout_center.addLayout( self.verticalLayout )
        self.verticalLayout_main.addLayout( self.horizontalLayout_center )
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName( "horizontalLayout_bottom" )
        spacerItem = QtGui.QSpacerItem( 40, 20, QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Minimum )
        self.horizontalLayout_bottom.addItem( spacerItem )
        self.pushButton = QtGui.QPushButton( self )
        self.pushButton.setMaximumSize( QtCore.QSize( 60, 16777215 ) )
        self.pushButton.setObjectName( "pushButton" )
        self.pushButton.setEnabled ( False )
        self.horizontalLayout_bottom.addWidget( self.pushButton )
        self.verticalLayout_main.addLayout( self.horizontalLayout_bottom )
        self.labelStatus = QtGui.QLabel( self )
        self.labelStatus.setText( "" )
        self.labelStatus.setObjectName( "labelStatus" )
        self.verticalLayout_main.addWidget( self.labelStatus )
        self.verticalLayout_2.addLayout( self.verticalLayout_main )

        self.createListWidget()
        self.signalConnect()
        self.retranslateUi( self )

        QtCore.QMetaObject.connectSlotsByName( self )

    def retranslateUi( self, Form ):
        Form.setWindowTitle( QtGui.QApplication.translate( "Form", "Asset Push", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.label_proj.setText( QtGui.QApplication.translate( "Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Create Task :</span><span style=\" font-size:12pt;\"> %s </span></p></body></html>" % self.typ[1], None, QtGui.QApplication.UnicodeUTF8 ) )
        self.label_fork.setText( QtGui.QApplication.translate( "Form", "Fork", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.label_comments.setText( QtGui.QApplication.translate( "Form", "<html><head/><body><p><span style=\" font-weight:600;\">Description</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8 ) )
        self.pushButton.setText( QtGui.QApplication.translate( "Form", "create", None, QtGui.QApplication.UnicodeUTF8 ) )


class UiMainManager( QtGui.QMainWindow ):

    db = None
    launcher = "terminal"

    def init ( self ) :
        pass

    def searchLine_a_Changed ( self, lineEdit, treeWidget ) :
        it = QtGui.QTreeWidgetItemIterator( treeWidget )
        text = self.lineEdit_a.text()

        while it.value () :
            item = it.value()

            if not item.parent() :

                if filter != "" :
                    itemtext = item.text( 0 )

                    if itemtext.find( text ) >= 0:
                        item.setHidden ( False )

                    else :
                        item.setHidden ( True )

                else :
                    item.setHidden ( False )

            it.next ()

    def searchLine_b_Changed ( self, lineEdit, treeWidget ) :
        it = QtGui.QTreeWidgetItemIterator( treeWidget )
        text = self.lineEdit_b.text()

        while it.value () :
            item = it.value()
            if item.hktype == "fork" :
                if filter != "" :
                    itemtext = item.text( 0 )
                    if itemtext.find( text ) >= 0 :
                        item.setHidden ( False )
                    else :
                        item.setHidden ( True )
                else :
                    item.setHidden ( False )
            it.next()

    def searchLine_a ( self ) :
        self.searchLine_a_Changed( self.lineEdit_a, self.treeWidget_a )

    def searchLine_b ( self ) :
        self.searchLine_b_Changed( self.lineEdit_b, self.treeWidget_a )

    def itemExpanded( self, item ):
        print item.text( 0 )

    def createWidget( self ):
        pass

    def comboTaskChange( self ):
        pass

    def comboTypeChange( self ):
        print self.comboBox_a.currentText()

    def itemClicked( self, item ):
        print "item clicked"

    def contextMenuEvent( self ):
        menu = QtGui.QMenu()
        menu.addAction( 'Add' )
        menu.addAction( 'Delete' )
        menu.exec_( QtGui.QCursor.pos() )

    def signalConnect( self ):
        self.comboBox_a.currentIndexChanged.connect( self.comboTypeChange )
        self.comboBox_b.currentIndexChanged.connect( self.comboTaskChange )
        self.lineEdit_a.textChanged.connect( self.searchLine_a )
        self.lineEdit_b.textChanged.connect( self.searchLine_b )
        self.treeWidget_a.itemExpanded.connect( self.itemExpanded )
        self.treeWidget_a.itemClicked.connect( self.itemClicked )
        self.treeWidget_a.customContextMenuRequested.connect( self.contextMenuEvent )

    def __init__( self, parent = None ):
        super( UiMainManager, self ).__init__( parent )
        self.db = utils.getDb ()
        self.setObjectName( "MainWindow" )
        self.setWindowTitle( "asset manager" )
        self.resize( 600, 700 )

        self.centralwidget = QtGui.QWidget( self )
        self.centralwidget.setObjectName( "centralwidget" )
        self.horizontalLayout_2 = QtGui.QHBoxLayout( self.centralwidget )
        self.horizontalLayout_2.setObjectName( "horizontalLayout_2" )
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName( "verticalLayout_main" )
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName( "horizontalLayout" )
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint( QtGui.QLayout.SetDefaultConstraint )
        self.verticalLayout.setObjectName( "verticalLayout" )
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName( "horizontalLayout_6" )
        self.label_sys = QtGui.QLabel( self.centralwidget )
        self.label_sys.setMaximumSize( QtCore.QSize( 21, 21 ) )
        self.label_sys.setObjectName( "label_sys" )
        self.horizontalLayout_6.addWidget( self.label_sys )
        self.label_proj = QtGui.QLabel( self.centralwidget )
        self.label_proj.setObjectName( "label_proj" )
        self.horizontalLayout_6.addWidget( self.label_proj )
        self.verticalLayout.addLayout( self.horizontalLayout_6 )
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName( "horizontalLayout_4" )
        self.label_filter = QtGui.QLabel( self.centralwidget )
        self.label_filter.setEnabled( True )
        self.label_filter.setMaximumSize( QtCore.QSize( 16, 16 ) )
        self.label_filter.setObjectName( "label_filter" )
        self.horizontalLayout_4.addWidget( self.label_filter )
        self.comboBox_a = QtGui.QComboBox( self.centralwidget )
        self.comboBox_a.setObjectName( "comboBox_a" )
        self.horizontalLayout_4.addWidget( self.comboBox_a )
        self.comboBox_b = QtGui.QComboBox( self.centralwidget )
        self.comboBox_b.setObjectName( "comboBox_b" )
        self.horizontalLayout_4.addWidget( self.comboBox_b )
        self.verticalLayout.addLayout( self.horizontalLayout_4 )
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName( "horizontalLayout_5" )
        self.label = QtGui.QLabel( self.centralwidget )
        self.label.setMaximumSize( QtCore.QSize( 16, 16 ) )
        self.label.setObjectName( "label" )
        self.horizontalLayout_5.addWidget( self.label )
        self.lineEdit_a = QtGui.QLineEdit( self.centralwidget )
        self.lineEdit_a.setObjectName( "lineEdit_a" )
        self.horizontalLayout_5.addWidget( self.lineEdit_a )
        self.lineEdit_b = QtGui.QLineEdit( self.centralwidget )
        self.lineEdit_b.setObjectName( "lineEdit_b" )
        self.horizontalLayout_5.addWidget( self.lineEdit_b )
        self.verticalLayout.addLayout( self.horizontalLayout_5 )
        self.treeWidget_a = QtGui.QTreeWidget( self.centralwidget )
        self.treeWidget_a.setAlternatingRowColors( True )
        self.treeWidget_a.setObjectName( "treeWidget_a" )
        self.verticalLayout.addWidget( self.treeWidget_a )
        self.horizontalLayout.addLayout( self.verticalLayout )
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName( "verticalLayout_2" )
        self.labelImage = QtGui.QLabel( self.centralwidget )
        self.labelImage.setMinimumSize ( QtCore.QSize ( 300, 300 ) )
        self.labelImage.setMaximumSize ( QtCore.QSize ( 960, 540 ) )
        self.labelImage.setScaledContents ( True )
        self.labelImage.setObjectName ( "labelImage" )
        self.verticalLayout_2.addWidget( self.labelImage )
        self.plainTextEdit_description = QtGui.QPlainTextEdit( self.centralwidget )
        self.plainTextEdit_description.setObjectName( "plainTextEdit_description" )
        self.plainTextEdit_description.setMinimumSize ( QtCore.QSize ( 300, 300 ) )
        self.verticalLayout_2.addWidget( self.plainTextEdit_description )
        self.horizontalLayout.addLayout( self.verticalLayout_2 )
        self.verticalLayout_main.addLayout( self.horizontalLayout )
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName( "horizontalLayout_3" )
        self.progressBar = QtGui.QProgressBar( self.centralwidget )
        self.progressBar.setEnabled( True )
        self.progressBar.setProperty( "value", 0 )
        self.progressBar.setObjectName( "progressBar" )
        self.horizontalLayout_3.addWidget( self.progressBar )
        self.verticalLayout_main.addLayout( self.horizontalLayout_3 )
        self.horizontalLayout_2.addLayout( self.verticalLayout_main )
        self.setCentralWidget( self.centralwidget )
        self.statusbar = QtGui.QStatusBar( self )
        self.statusbar.setObjectName( "statusbar" )
        self.setStatusBar( self.statusbar )

        self.customUi ()
        QtCore.QMetaObject.connectSlotsByName( self )
        self.init()

    def customUi ( self ):
        self.progressBar.setHidden( True )
        self.label_proj.setText( """<html><head/><body><p><span style=\" font-size:12pt;
                                    font-weight:600;\">Asset Manager </span><span style=\" font-size:12pt;
                                    \"/><span style=\" font-size:12pt;font-weight:600;
                                    \">:</span><span style=\" font-size:12pt;
                                    \"> '%s'</span></p></body></html>""" % utils.getProjectName() )

        self.labelImage.setPixmap( utils.getIconPath( "hk_title_medium" ) )
        self.label_sys.setPixmap ( utils.getIconPath( self.launcher ) )
        self.label.setPixmap ( utils.getIconPath( "search.png" ) )
        self.label_filter.setPixmap( utils.getIconPath( "filter.png" ) )

        self.treeWidget_a.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        self.treeWidget_a.headerItem().setText ( 0, "asset" )
        self.plainTextEdit_description.setReadOnly( True )
        self.createWidget ()
        self.signalConnect ()


class UiAssetManager ( UiMainManager ):

    fileFilters = "Maya (*.ma *.mb);;Wavefront (*.obj *.Obj *.OBJ)"
    defaultsuffix = "obj"

    # TODO: add push dir ui for texture grooming render etc
    pushls = ( "texture",
               "render",
               "compout" )

    assettype = utils.getAssetTypes ()

    icon_empty = utils.getIconPath( "empty" )

    def createAsset ( self ) :
        nicename = self.comboBox_a.currentText()
        typ = self.assettype [ nicename ]
        self.createAssetWidget = UiCreateAsset ( typ = ( nicename, typ ) )
        self.createAssetWidget.show()

    def createTask ( self ) :
        item = self.treeWidget_a.currentItem ()
        doc_id = item.hkid
        nicename = doc_id

        self.createTaskWidget = UiCreateTask ( db = self.db, typ = ( nicename, doc_id ) )
        self.createTaskWidget.show()

    def pushVersion ( self ) :
        item = self.treeWidget_a.currentItem()
        task = item.parent().text( 0 )

        if task in self.pushls:
            self.pushVersionWin = UiPushLs ( db = self.db, item = item )

        else:
            self.pushVersionWin = UiPush ( db = self.db, item = item )

        self.pushVersionWin.show ()

    def pullVersion ( self ) :
        self.progressBar.setHidden ( False )
        item = self.treeWidget_a.currentItem ()

        """get asset id and version"""
        doc_id = item.parent().hkid
        ver = int ( item.text ( 0 ) )
        self.statusbar.showMessage ( "Pulling %s %s" % ( doc_id, str( ver ) ) )

        """Pull asset"""
        pull = core.pull ( db = self.db, doc_id = doc_id, version = ver,
                           progressbar = self.progressBar, msgbar = self.statusbar.showMessage )

        if pull :
            self.statusbar.showMessage( "%s %s pulled" % ( doc_id, str( ver ) ) )

        self.progressBar.setHidden ( True )

    def importVersion ( self ) :
        print "importVersion()"

    def openFileDialog ( self ) :
        item = self.treeWidget_a.currentItem()
        hkid = item.hkid
        path = hkid.replace( "_", os.sep )
        path = os.path.join ( os.getenv( "HK_USER_REPO" ), path )
        fdialog = QtGui.QFileDialog ()
        fdialog.setDefaultSuffix ( self.defaultsuffix )
        fname = fdialog.getOpenFileName ( self, caption = 'Open file from workspace',
                                          dir = path, filter = self.fileFilters )
        self.openFile ( fname[0] )

    def openFile( self, fname ):
        print fname

    def saveFileDialog ( self ) :
        item = self.treeWidget_a.currentItem()
        hkid = item.hkid
        path = hkid.replace( "_", os.sep )
        path = os.path.join ( os.getenv( "HK_USER_REPO" ), path )
        fdialog = QtGui.QFileDialog()
        fdialog.setDefaultSuffix ( self.defaultsuffix )
        fdialog.setConfirmOverwrite ( True )
        fname = fdialog.getSaveFileName ( self, caption = 'Save file to workspace',
                                        dir = path, filter = self.fileFilters )
        self.saveFile ( fname[0] )

    def saveFile( self, fname ):
        print fname

    def createWorkspace ( self ) :
        item = self.treeWidget_a.currentItem()
        core.createWorkspace ( item.hkid )

    def contextMenuAsset ( self, item ) :
        menu = QtGui.QMenu ()
        curtext = self.comboBox_a.currentText()
        icon_new = QtGui.QIcon ( utils.getIconPath( "add" ) )

        """Do not allow to create asset from asset or task"""
        if not ( curtext in ( "asset", "task" ) ):
            """Create new asset"""
            newAsset = menu.addAction ( icon_new, 'Add %s' % curtext )
            newAsset.triggered.connect ( self.createAsset )

        """Create new task"""
        newTask = menu.addAction ( icon_new, 'Add task' )
        newTask.triggered.connect ( self.createTask )

        """Refresh option """
        icon_refresh = QtGui.QIcon ( utils.getIconPath( "refresh" ) )
        refresh = menu.addAction ( icon_refresh, 'Refresh' )
        refresh.triggered.connect ( self.refreshBranch )

        """Execute menu"""
        menu.exec_( QtGui.QCursor.pos() )

    def contextMenuTask ( self, item ) :
        item = self.treeWidget_a.currentItem ()
        menu = QtGui.QMenu ()

        """Get workspace"""
        doc_id = item.hkid
        path = core.getPathFromId ( doc_id, True )

        if os.path.exists ( path ) :
            """Check if workspace exists"""
            icon_push = QtGui.QIcon ( utils.getIconPath( "push" ) )
            push = menu.addAction ( icon_push, 'Push a new %s version' % doc_id )
            push.triggered.connect ( self.pushVersion )

        else:
            """If not existing create action createWorkspace """
            icon_new = QtGui.QIcon ( utils.getIconPath( "add" ) )
            createWorkspace = menu.addAction ( icon_new, 'Create workspace' )
            createWorkspace.triggered.connect ( self.createWorkspace )

        menu.exec_ ( QtGui.QCursor.pos () )

    def contextMenuVersion ( self, item ) :
        menu = QtGui.QMenu ()
        icon_pull = QtGui.QIcon ( utils.getIconPath( "pull" ) )
        action_pull = menu.addAction ( icon_pull, 'Pull version %s' % item.text ( 0 ) )
        action_pull.triggered.connect ( self.pullVersion )

        menu.exec_( QtGui.QCursor.pos () )

    def contextMenuEvent ( self ) :
        item = self.treeWidget_a.currentItem ()
        if not item:
            self.contextMenuAsset ( item )

        else :
            item_type = item.hktype

            if item_type == "sequence" :
                print "contextMenuEvent(): sequence"

            if item_type == "asset" :
                self.contextMenuAsset ( item )

            elif item_type == "task" :
                self.contextMenuTask ( item )

            elif item_type == "version" :
                self.contextMenuVersion ( item )

            elif item_type == "None" :
                pass

    def refreshBranch ( self ):
        item = self.treeWidget_a.currentItem ()
        if item :
            item.takeChildren()
            icon_empty = utils.getIconPath( "hk_title" )
            item_none = QtGui.QTreeWidgetItem ( item )
            item_none.hktype = "none"
            item_none.setText ( 0, "Empty" )
            item_none.setIcon ( 0, QtGui.QIcon( icon_empty ) )
            self.itemExpanded ( item )

    def itemExpandedSequence ( self, item ) :
        itChildCount = item.childCount ()
        if not ( itChildCount > 1 ) :
            icon_empty = utils.getIconPath( "empty" )
            startkey = item.hkid.replace( "seq", "shot" )
            shot_ls = utils.lsDb ( self.db, "shot", startkey )

            if len ( shot_ls ) > 0 :
                item.removeChild( item.child( 0 ) )

            for shot in shot_ls :
                itemChild = QtGui.QTreeWidgetItem ( item )
                itemChild.setFont( 0, item.font( 0 ) )
                itemChild.setText ( 0, shot.split( "_" )[1] )
                icon = utils.getIconPath( "shot" )
                itemChild.setIcon ( 0, QtGui.QIcon ( icon ) )
                itemChild.hktype = "asset"
                itemChild.hkbranch = shot
                itemChild.hkid = ( "%s_%s" ) % ( utils.getProjectName(), shot )

                item_none = QtGui.QTreeWidgetItem( itemChild )
                item_none.hktype = "none"
                item_none.hkbranch = shot
                item_none.setText ( 0, "Empty" )
                item_none.setIcon ( 0, QtGui.QIcon( icon_empty ) )

            order = QtCore.Qt.AscendingOrder
            item.sortChildren ( 0, order )

            if ( item.childCount () > 1 ) and ( item.child( 0 ).hktype == "none" ) :
                item.removeChild ( item.child( 0 ) )
        self.filterTree ()

    def itemExpandedAsset ( self, item ) :

        if item.child ( 0 ).hktype == "none" :
            icon_empty = utils.getIconPath( "empty" )
            doc_id = item.hkid
            tasks = utils.lsDb ( self.db, "task", doc_id )
            font = item.font( 0 )
            font.setPointSize ( 9.5 )

            if len ( tasks ) > 0 :
                brush = QtGui.QBrush( QtGui.QColor ( 150, 150, 150 ) )
                item.removeChild ( item.child ( 0 ) )

            for task in tasks :
                itemChild = QtGui.QTreeWidgetItem ( item )
                itemChild.setForeground( 0, brush )
                itemChild.setText ( 0, task )
                itemChild.setFont( 0, font )
                itemChild.hktype = "task"
                itemChild.hkbranch = task.split( "_" )[2]
                itemChild.hkid = "%s_%s" % ( utils.getProjectName(), task )
                itemChild.versions = dict ()
                itemChild.dbdoc = self.db [ "%s_%s" % ( utils.getProjectName(), task ) ]
                icon = utils.getIconPath( itemChild.hkbranch )
                itemChild.setIcon ( 0, QtGui.QIcon ( icon ) )

                item_none = QtGui.QTreeWidgetItem( itemChild )
                item_none.hktype = "none"
                item_none.hkbranch = task.split( "_" )[2]
                item_none.setText ( 0, "Empty" )
                item_none.setIcon ( 0, QtGui.QIcon( icon_empty ) )

            order = QtCore.Qt.AscendingOrder
            item.sortChildren( 0, order )

        self.filterTree()

    def itemExpandedTask ( self, item ) :

        if item.child( 0 ).hktype == "none" :
            font = QtGui.QFont ()
            font.setItalic ( True )

            if item.versions == dict ():
                item.versions = item.dbdoc [ "review" ]

                if len ( item.versions ) > 0:
                    brush = QtGui.QBrush ( QtGui.QColor ( 128, 128, 128 ) )

                    for ver in item.versions :
                        itemChild = QtGui.QTreeWidgetItem ( item )
                        itemChild.setFont ( 0, font )
                        itemChild.setForeground ( 0, brush )
                        icon = utils.getIconPath( "file" )
                        itemChild.setIcon ( 0, QtGui.QIcon ( icon ) )
                        itemChild.setText ( 0, "%03d" % float ( ver ) )
                        itemChild.hkbranch = item.hkbranch
                        itemChild.hktype = "version"
                        itemChild.info = item.versions [ ver ]

                    order = QtCore.Qt.DescendingOrder
                    item.sortChildren ( 0, order )
                    item.removeChild ( item.child ( 0 ) )

    def itemExpanded ( self, item ) :

        if item.hktype == "asset":
            self.itemExpandedAsset ( item )

        elif item.hktype == "task" :
            self.itemExpandedTask ( item )

        elif item.hktype == "sequence" :
            self.itemExpandedSequence ( item )

    def itemClickedTask( self, item ) :

        """Set the data to the plain text"""
        creator = "Creator:\t%s\n" % item.dbdoc [ 'creator' ]
        created = "\nCreated:\t%s\n" % item.dbdoc [ 'created' ]
        status = "\nStatus:\t%s\n" % item.dbdoc [ 'status' ]
        description = "\nDescription:\n\t%s\n" % item.dbdoc [ 'description' ]

        infos = creator + created + status + description
        self.plainTextEdit_description.setPlainText ( infos )

    def itemClickedVersion( self, item ) :

        # Set the data to the plain text
        creator = "Creator:\t%s\n" % item.info [ 'creator' ]
        created = "\nCreated:\t%s\n" % item.info [ 'created' ]
        description = "\nDescription:\n\t%s\n" % item.info [ 'description' ]

        path = os.path.expandvars( item.info [ "path" ] )
        pathinfo = "\nPath:\n\t%s\n" % os.path.expandvars( item.info [ "path" ] )

        files = "\n\t".join ( map ( str, item.info [ "files" ] ) )
        files = "\nFiles:\n\t%s\n" % files

        infos = creator + created + description + pathinfo + files
        self.plainTextEdit_description.setPlainText ( infos )

        # Set the screenshot
        screenshot = ""
        for ext in ( "jpg", "jpeg", "png" ) :
            screenshot = "%s.%s" % ( item.parent().hkid, ext )
            screenshot = os.path.join ( path, screenshot )

            if os.path.exists ( screenshot ):
                break

        if not os.path.exists ( screenshot ) :
            screenshot = utils.getIconPath( "hk_title_medium" )

        self.labelImage.setPixmap ( screenshot )
#         self.labelImage.setFixedSize ( QtCore.QSize ( 640, 480 ) )

    def itemClicked ( self, item ) :

        if item.hktype == "task" :
            self.itemClickedTask ( item )

        elif item.hktype == "version" :
            self.itemClickedVersion ( item )

        else:
            self.plainTextEdit_description.setPlainText ( "" )

        if hasattr( item, "hkid" ) :
            self.statusbar.showMessage( item.hkid )

        else:
            self.statusbar.showMessage( "" )

    def setComboTask ( self ) :
        task_dict = utils.getAssetTasks ()
        self.comboBox_b.clear ()
        icon = utils.getIconPath( "cross" )
        self.comboBox_b.addItem ( QtGui.QIcon ( icon ), "No filter" )

        for key in task_dict :
            icon = utils.getIconPath( task_dict [ key ] )
            self.comboBox_b.addItem ( QtGui.QIcon ( icon ), key )

    def filterTree ( self ) :
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
                            item.setHidden( True )
            it.next()

    def comboTypeChange ( self ) :
        currtext = self.comboBox_a.currentText ()
        assettype = self.assettype
        assettype [ "asset" ] = "asset"
        assettype [ "task" ] = "task"
        self.typ = assettype [ currtext ]
        startkey = utils.getProjectName()
        hktype = "asset"

        """Check if current filter is asset or task"""
        if not ( self.typ in ( "asset", "task" ) ):
            """If current filter is asset or task then create a proper view"""
            startkey = "%s_%s" % ( startkey, self.typ )

        """List assets"""
        asset_ls = utils.lsDb ( self.db, self.typ, startkey )

        """Clear the tree"""
        icon_empty = utils.getIconPath( "empty" )
        self.treeWidget_a.clear ()

        """Setup the items fonts"""
        font = QtGui.QFont ()
        font.setPointSize ( 10 )
        font.setWeight ( 75 )
        font.setItalic ( False )
        font.setBold ( True )

        """Create the items"""
        for asset in asset_ls:
            """Set the item attributes"""
            item_asset = QtGui.QTreeWidgetItem ( self.treeWidget_a )
            assplit = asset.split ( "_" )
            typ, name = assplit[0], assplit[1]

            if self.typ == "task" :
                item_asset.versions = dict ()
                item_asset.dbdoc = self.db [ "%s_%s" % ( utils.getProjectName(), asset ) ]
                hktype = "task"
                name = asset

            item_asset.hkid = "%s_%s" % ( utils.getProjectName(), asset )
            item_asset.hkbranch = "root"
            item_asset.hktype = hktype

            """UI look"""
            item_asset.setFont ( 0, font )
            item_asset.setText ( 0, name )
            icon = utils.getIconPath( typ )
            item_asset.setIcon ( 0, QtGui.QIcon( icon ) )

            """Children"""
            item_none = QtGui.QTreeWidgetItem( item_asset )
            item_none.setIcon ( 0, QtGui.QIcon( icon_empty ) )
            item_none.setText ( 0, "Empty" )
            item_none.hktype = "none"
            item_none.hkbranch = "empty"

        self.filterTree ()

    def comboTaskChange ( self ) :
        self.filterTree ()

    def createWidget ( self ) :
        """Create the type combobox"""
        assettype = self.assettype
        assettype ["asset"] = "asset"
        assettype ["task"] = "task"

        item = list ( ( "asset", "task" ) )
        tmp = list ()

        for key in assettype :
            if not ( key in item ):
                tmp.append ( key )

        tmp.sort ()
        item = item + tmp

        for key in item :
            icon = utils.getIconPath( assettype [ key ] )
            self.comboBox_a.addItem ( QtGui.QIcon ( icon ), key )

        self.comboTypeChange ()
        self.setComboTask ()

def systemAM () :
    app = QtGui.QApplication ( sys.argv )
    main = UiAssetManager()
    main.show()
    app.exec_()
    sys.exit()

if __name__ == '__main__':
    systemAM ()
