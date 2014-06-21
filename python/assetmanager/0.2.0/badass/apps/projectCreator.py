'''
Created on Mar 5, 2013

@author: pixo
'''
import sys, re, os
import badass.core as core
import badass.utils as utils
from PySide import QtCore, QtGui

class UiProjectCreator ( QtGui.QMainWindow ):

    def pushButtonClicked( self ):
        name = self.lineEdit_project.text()

        if name == "":
            msg = "Can't create asset '%s' no characters in name"
            self.statusbar.showMessage ( msg % name )
            return

        if re.sub( "[a-z]", "", name ) != "":
            msg = "Can't create Project '%s', invalid characters" % name
            self.statusbar.showMessage( msg )
            return

        """Collect host data"""
        huser = self.lineEdit_husername.text()
        hadress = self.lineEdit_hadress.text()
        hroot = self.lineEdit_root.text()
        rootadress = "%s@%s:/%s" % ( huser, hadress, hroot )

        """Collect DB data"""
        user = self.lineEdit_username.text()
        password = self.lineEditPassword.text()
        adress = self.lineEdit_adress.text()
        serveradress = "%s:%s@%s" % ( user, password, adress )
        description = self.plainTextEdit_description.toPlainText()
        badassversion = self.comboBoxVersions.currentText()

        doc = core.createProject ( name = name, description = description,
                                   db_server = serveradress, host_root = rootadress,
                                   badassversion = badassversion )

        if doc :
            msg = "'%s' added to db '%s'" % ( name, name )
            self.statusbar.showMessage ( msg )
            print msg
            self.close ()

    def descriptionChanged( self ):
        description = self.plainTextEdit_description.toPlainText()

        if description == "" :
            self.pushButton_create.setEnabled ( False )
        else :
            self.pushButton_create.setEnabled ( True )

    def signalConnect( self ):
        """ Connect the UI to the Ui_AssetWindow methods """
        self.pushButton_create.clicked.connect( self.pushButtonClicked )
        self.plainTextEdit_description.textChanged.connect( self.descriptionChanged )

    def __init__( self, parent = None ):
        super( UiProjectCreator, self ).__init__( parent )

        self.setObjectName( "MainWindow" )
        self.setWindowTitle( "Project creator" )

        self.resize( 585, 482 )
        self.centralwidget = QtGui.QWidget( self )
        self.centralwidget.setObjectName( "centralwidget" )
        self.verticalLayout_2 = QtGui.QVBoxLayout( self.centralwidget )
        self.verticalLayout_2.setObjectName( "verticalLayout_2" )
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName( "verticalLayout" )

        # DB Adress
        self.horizontalLayout_adress = QtGui.QHBoxLayout ()
        self.horizontalLayout_adress.setObjectName ( "horizontalLayout_adress" )
        self.label_adress = QtGui.QLabel ( self )
        self.label_adress.setObjectName ( "label_adress" )
        self.label_adress.setMinimumSize ( QtCore.QSize ( 80, 0 ) )
        self.horizontalLayout_adress.addWidget ( self.label_adress )
        self.labelpixmap_adress = QtGui.QLabel ( self )
        self.labelpixmap_adress.setObjectName ( "labelpixmap_adress" )
        self.horizontalLayout_adress.addWidget ( self.labelpixmap_adress )
        self.lineEdit_adress = QtGui.QLineEdit ( self )
        self.lineEdit_adress.setObjectName ( "lineEdit_adress" )
        self.horizontalLayout_adress.addWidget ( self.lineEdit_adress )
        self.verticalLayout.addLayout ( self.horizontalLayout_adress )

        # username
        self.horizontalLayout_username = QtGui.QHBoxLayout ()
        self.horizontalLayout_username.setObjectName ( "horizontalLayout_username" )
        self.label_username = QtGui.QLabel ( self )
        self.label_username.setObjectName ( "label_username" )
        self.label_username.setMinimumSize ( QtCore.QSize ( 80, 0 ) )
        self.horizontalLayout_username.addWidget ( self.label_username )
        self.labelpixmap_username = QtGui.QLabel ( self )
        self.labelpixmap_username.setObjectName ( "labelpixmap_username" )
        self.horizontalLayout_username.addWidget ( self.labelpixmap_username )
        self.lineEdit_username = QtGui.QLineEdit ( self )
        self.lineEdit_username.setObjectName ( "lineEditPassword" )
        self.horizontalLayout_username.addWidget ( self.lineEdit_username )
        self.verticalLayout.addLayout ( self.horizontalLayout_username )

        # password
        self.horizontalLayoutPassword = QtGui.QHBoxLayout ()
        self.horizontalLayoutPassword.setObjectName ( "horizontalLayoutPassword" )
        self.labelPassword = QtGui.QLabel ( self )
        self.labelPassword.setObjectName ( "labelPassword" )
        self.labelPassword.setMinimumSize( QtCore.QSize( 80, 0 ) )
        self.horizontalLayoutPassword.addWidget ( self.labelPassword )
        self.labelPixmapPassword = QtGui.QLabel ( self )
        self.labelPixmapPassword.setObjectName ( "labelPixmapPassword" )
        self.horizontalLayoutPassword.addWidget ( self.labelPixmapPassword )
        self.lineEditPassword = QtGui.QLineEdit ( self )
        self.lineEditPassword.setEchoMode( QtGui.QLineEdit.Password )
        self.lineEditPassword.setObjectName ( "lineEditPassword" )
        self.horizontalLayoutPassword.addWidget ( self.lineEditPassword )
        self.verticalLayout.addLayout ( self.horizontalLayoutPassword )

        # host adress
        self.horizontalLayout_hadress = QtGui.QHBoxLayout ()
        self.horizontalLayout_hadress.setObjectName ( "horizontalLayout_hadress" )
        self.label_hadress = QtGui.QLabel ( self )
        self.label_hadress.setObjectName ( "label_hadress" )
        self.label_hadress.setMinimumSize ( QtCore.QSize ( 80, 0 ) )
        self.horizontalLayout_hadress.addWidget ( self.label_hadress )
        self.labelpixmap_hadress = QtGui.QLabel ( self )
        self.labelpixmap_hadress.setObjectName ( "labelpixmap_hadress" )
        self.horizontalLayout_hadress.addWidget ( self.labelpixmap_hadress )
        self.lineEdit_hadress = QtGui.QLineEdit ( self )
        self.lineEdit_hadress.setObjectName ( "lineEdit_hadress" )
        self.horizontalLayout_hadress.addWidget ( self.lineEdit_hadress )
        self.verticalLayout.addLayout ( self.horizontalLayout_hadress )

        # host username
        self.horizontalLayout_husername = QtGui.QHBoxLayout ()
        self.horizontalLayout_husername.setObjectName ( "horizontalLayout_husername" )
        self.label_husername = QtGui.QLabel ( self )
        self.label_husername.setObjectName ( "label_husername" )
        self.label_husername.setMinimumSize ( QtCore.QSize ( 80, 0 ) )
        self.horizontalLayout_husername.addWidget ( self.label_husername )
        self.labelpixmap_husername = QtGui.QLabel ( self )
        self.labelpixmap_husername.setObjectName ( "labelpixmap_username" )
        self.horizontalLayout_husername.addWidget ( self.labelpixmap_husername )
        self.lineEdit_husername = QtGui.QLineEdit ( self )
        self.lineEdit_husername.setObjectName ( "lineEditPassword" )
        self.horizontalLayout_husername.addWidget ( self.lineEdit_husername )
        self.verticalLayout.addLayout ( self.horizontalLayout_husername )

        # Host root
        self.horizontalLayout_root = QtGui.QHBoxLayout ()
        self.horizontalLayout_root.setObjectName ( "horizontalLayout_root" )
        self.label_root = QtGui.QLabel ( self.centralwidget )
        self.label_root.setMinimumSize ( QtCore.QSize ( 80, 0 ) )
        self.label_root.setObjectName ( "label_root" )
        self.horizontalLayout_root.addWidget ( self.label_root )
        self.labelpixmap_root = QtGui.QLabel ( self )
        self.labelpixmap_root.setObjectName ( "labelpixmap_root" )
        self.horizontalLayout_root.addWidget ( self.labelpixmap_root )
        self.lineEdit_root = QtGui.QLineEdit ( self.centralwidget )
        self.lineEdit_root.setObjectName  ( "lineEdit_root" )
        self.horizontalLayout_root.addWidget ( self.lineEdit_root )
        self.verticalLayout.addLayout ( self.horizontalLayout_root )
        self.label_root.setText ( "Host root" )

        # Project slug
        self.horizontalLayout_project = QtGui.QHBoxLayout ()
        self.horizontalLayout_project.setObjectName ( "horizontalLayout_project" )
        self.label_project = QtGui.QLabel ( self.centralwidget )
        self.label_project.setMinimumSize ( QtCore.QSize ( 80, 0 ) )
        self.label_project.setObjectName ( "label_project" )
        self.horizontalLayout_project.addWidget ( self.label_project )
        self.labelpixmap_project = QtGui.QLabel ( self )
        self.labelpixmap_project.setObjectName ( "labelpixmap_project" )
        self.horizontalLayout_project.addWidget ( self.labelpixmap_project )
        self.lineEdit_project = QtGui.QLineEdit ( self.centralwidget )
        self.lineEdit_project.setObjectName( "lineEdit_project" )
        self.horizontalLayout_project.addWidget( self.lineEdit_project )
        self.verticalLayout.addLayout( self.horizontalLayout_project )

        # Asset manager version
        self.horizontalLayoutVersions = QtGui.QHBoxLayout ()
        self.horizontalLayoutVersions.setObjectName ( "horizontalLayoutVersions" )
        self.label_version = QtGui.QLabel ( self.centralwidget )
        self.label_version.setMinimumSize ( QtCore.QSize ( 80, 0 ) )
        self.label_version.setObjectName ( "label_version" )
        self.horizontalLayoutVersions.addWidget ( self.label_version )
        self.labelpixmap_version = QtGui.QLabel ( self )
        self.labelpixmap_version.setObjectName ( "labelpixmap_version" )
        self.horizontalLayoutVersions.addWidget ( self.labelpixmap_version )
        self.comboBoxVersions = QtGui.QComboBox( self.centralwidget )
        self.comboBoxVersions.setAccessibleName( "" )
        self.comboBoxVersions.setObjectName( "comboBoxVersions" )
        self.horizontalLayoutVersions.addWidget( self.comboBoxVersions )
        self.verticalLayout.addLayout ( self.horizontalLayoutVersions )

        spacerItem1 = QtGui.QSpacerItem( 40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
        self.horizontalLayoutVersions.addItem( spacerItem1 )

        # Description
        self.verticalLayout_description = QtGui.QVBoxLayout()
        self.verticalLayout_description.setObjectName( "verticalLayout_description" )
        self.label_description = QtGui.QLabel ( self.centralwidget )
        self.label_description.setObjectName ( "label_description" )
        self.label_description.setText ( "Description" )
        self.verticalLayout_description.addWidget ( self.label_description )
        self.plainTextEdit_description = QtGui.QPlainTextEdit( self.centralwidget )
        self.plainTextEdit_description.setObjectName( "plainTextEdit_description" )
        self.verticalLayout_description.addWidget ( self.plainTextEdit_description )
        self.verticalLayout.addLayout( self.verticalLayout_description )

        # Push button create
        self.horizontalLayout_create = QtGui.QHBoxLayout()
        self.horizontalLayout_create.setObjectName( "horizontalLayout_create" )
        spacerItem = QtGui.QSpacerItem ( 40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
        self.horizontalLayout_create.addItem ( spacerItem )
        self.pushButton_create = QtGui.QPushButton ( self.centralwidget )
        self.pushButton_create.setObjectName ( "pushButton_create" )
        self.pushButton_create.setText ( "Create" )
        self.horizontalLayout_create.addWidget ( self.pushButton_create )
        self.verticalLayout.addLayout ( self.horizontalLayout_create )

        # Main vertical
        self.verticalLayout_2.addLayout( self.verticalLayout )

        # Status bar
        self.setCentralWidget( self.centralwidget )
        self.statusbar = QtGui.QStatusBar( self )
        self.statusbar.setObjectName( "statusbar" )
        self.setStatusBar( self.statusbar )

        self.setUi ()

        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName( self )


    def setUi ( self ):
        ccpath = utils.getCCPath()

        """Username"""
        username = "admin"
        icon = os.path.join ( utils.getCCPath (), "admin.png" )
        self.label_username.setText ( "DB user" )
        self.labelpixmap_username.setPixmap ( icon )
        self.lineEdit_username.setText ( username )

        """Password"""
        password = "admin"
        icon = os.path.join ( utils.getCCPath (), "password.png" )
        self.labelPassword.setText ( "DB password" )
        self.labelPixmapPassword.setPixmap ( icon )
        self.lineEditPassword.setText ( password )

        """DB adress"""
        adress = "127.0.0.1:5984"
        icon = os.path.join ( utils.getCCPath (), "adress.png" )
        self.label_adress.setText ( "DB adress" )
        self.labelpixmap_adress.setPixmap ( icon )
        self.lineEdit_adress.setText ( adress )

        """host Username"""
        username = "admin"
        icon = os.path.join ( utils.getCCPath (), "admin.png" )
        self.label_husername.setText ( "Host user" )
        self.labelpixmap_husername.setPixmap ( icon )
        self.lineEdit_husername.setText ( username )

        """host adress"""
        hadress = "127.0.0.1"
        icon = os.path.join ( utils.getCCPath (), "adress.png" )
        self.label_hadress.setText ( "Host adress" )
        self.labelpixmap_hadress.setPixmap ( icon )
        self.lineEdit_hadress.setText ( hadress )

        """Homework root"""
        root = "homeworks"
        icon = os.path.join ( utils.getCCPath (), "hierarchy.png" )
        self.label_root.setText ( "Host root" )
        self.lineEdit_root.setText ( root )
        self.labelpixmap_root.setPixmap ( icon )

        """project"""
        project = "prj"
        icon = os.path.join( utils.getCCPath (), "project.png" )
        self.label_project.setText( "Project slug" )
        self.labelpixmap_project.setPixmap( icon )
        self.lineEdit_project.setText( project )

        """Version"""
        icon = os.path.join ( utils.getCCPath (), "hktitle16x16.png" )
        self.label_version.setText ( "Badass" )
        self.labelpixmap_version.setPixmap ( icon )
        self.comboBoxVersions.addItems( utils.getBadassVersions() )

        """Create"""
        self.pushButton_create.setEnabled ( False )
        self.pushButton_create.setIcon ( QtGui.QIcon ( os.path.join ( ccpath, "add.png" ) ) )


if __name__ == '__main__':
    app = QtGui.QApplication ( sys.argv )
    main = UiProjectCreator()
    main.show()
    app.exec_()
    sys.exit()
