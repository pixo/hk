'''
Created on Oct 19, 2013

@author: pixo
'''
import sys, os
import badass.core as core
import badass.utils as utils
from PySide import QtCore, QtGui

class UiProjectCloner ( QtGui.QWidget ):

    def refreshClicked ( self ):
        """Collect data"""
        user = self.lineEdit_username.text ()
        password = self.lineEdit_password.text ()
        adress = self.lineEdit_adress.text ()
        serveradress = "%s:%s@%s" % ( user, password, adress )

        """Refresh projects, icons"""
        self.refreshProject ( serveradress )

    def projectChanged ( self ):

        if not self.server:
            self.plainTextEdit.setPlainText ( "" )
            return

        current = self.comboBox_project.currentText ()
        root = "/homeworks"

        """"Project Descriptions"""
        description = ""

        """"Check description for initialiation or none available project"""
        if not ( current in [ "", "No project available" ] ) :
            description = self.server[current][current]["description"]
            root = self.server[current][current]["root"]

        self.lineEdit_root.setText ( root )
        self.plainTextEdit.setPlainText ( description )

        """Check if current project exist on the local drive"""
        if current in self.project_stat :
            self.pushButton.setEnabled ( self.project_stat [ current ] )


    def synchonizeClicked ( self ):
        ""
        project = self.comboBox_project.currentText ()
        user = self.lineEdit_username.text ()
        password = self.lineEdit_password.text ()
        adress = self.lineEdit_adress.text ()
        serveradress = "%s:%s@%s" % ( user, password, adress )


        db = self.server [ project ][ project ]
        host = db [ "host" ]
        local = db [ "root" ]

        source = os.path.join ( host, "projects", project )
        destination = os.path.join ( local, "projects" )
        utils.rsync ( source, destination )
#         utils.rsync ( source, destination, ["sct","tex"] )
        core.createProjectCred ( project, serveradress, host )

        self.close ()

    def refreshProject ( self, serveradress ):
        """If server exist set 'ok' icon """
        self.server = False
        if utils.serverExists ( serveradress ) :
            icon = utils.getIconPath( "ok" )
            self.server = utils.getServer ( serveradress )

        """Clear current comboBox_project list"""
        self.comboBox_project.clear ()
        icon = utils.getIconPath( "cross" )
        self.projects = ["No project available"]

        if utils.serverExists ( serveradress ) :
            projects = core.lsProjectServer ( serveradress )

            if len ( projects ) > 0 :
                self.projects = projects

        self.comboBox_project.addItems ( self.projects )
        root = self.lineEdit_root.text()
        root = os.path.join ( root, "projects" )

        for i in range ( 0, self.comboBox_project.count () ):
            proj = self.comboBox_project.itemText ( i )
            curroot = os.path.join ( root, proj )

            if proj == "No project available" or os.path.exists ( curroot ) :
                icon = utils.getIconPath( "cross" )
                self.project_stat [ proj ] = False
            else:
                icon = utils.getIconPath( "ok" )
                self.project_stat [ proj ] = True

            self.comboBox_project.setItemIcon ( i, QtGui.QIcon ( icon ) )

        self.pushButton.setEnabled ( self.project_stat [ self.comboBox_project.currentText () ] )



    def __init__( self, parent = None ):
        super ( UiProjectCloner, self ).__init__( parent )

        self.setObjectName ( "MainWindow" )
        self.setWindowTitle ( "Project Cloner" )
        self.resize ( 570, 470 )

        self.verticalLayout_2 = QtGui.QVBoxLayout ( self )
        self.verticalLayout_2.setObjectName ( "verticalLayout_2" )
        self.verticalLayout = QtGui.QVBoxLayout ()
        self.verticalLayout.setObjectName ( "verticalLayout" )

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
        self.lineEdit_username.setObjectName ( "lineEdit_password" )
        self.horizontalLayout_username.addWidget ( self.lineEdit_username )
        self.verticalLayout.addLayout ( self.horizontalLayout_username )

        # password
        self.horizontalLayout_password = QtGui.QHBoxLayout ()
        self.horizontalLayout_password.setObjectName ( "horizontalLayout_password" )
        self.label_password = QtGui.QLabel ( self )
        self.label_password.setObjectName ( "label_password" )
        self.label_password.setMinimumSize( QtCore.QSize( 80, 0 ) )
        self.horizontalLayout_password.addWidget ( self.label_password )
        self.labelpixmap_password = QtGui.QLabel ( self )
        self.labelpixmap_password.setObjectName ( "labelpixmap_password" )
        self.horizontalLayout_password.addWidget ( self.labelpixmap_password )
        self.lineEdit_password = QtGui.QLineEdit ( self )
        self.lineEdit_password.setEchoMode( QtGui.QLineEdit.Password )
        self.lineEdit_password.setObjectName ( "lineEdit_password" )
        self.horizontalLayout_password.addWidget ( self.lineEdit_password )
        self.verticalLayout.addLayout ( self.horizontalLayout_password )


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

        # DB project
        self.horizontalLayout_project = QtGui.QHBoxLayout()
        self.horizontalLayout_project.setObjectName( "horizontalLayout_project" )
        self.label_project = QtGui.QLabel ( self )
        self.label_project.setObjectName ( "label_project" )
        self.label_project.setMinimumSize ( QtCore.QSize ( 80, 0 ) )
        self.horizontalLayout_project.addWidget ( self.label_project )
        self.refresh = QtGui.QPushButton ( self )
        self.refresh.setObjectName ( "refresh" )
        self.refresh.setMaximumSize ( QtCore.QSize ( 16, 16 ) )
        self.horizontalLayout_project.addWidget ( self.refresh )
        self.comboBox_project = QtGui.QComboBox ( self )
        self.comboBox_project.setEnabled( True )
        sizePolicy = QtGui.QSizePolicy( QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed )
        sizePolicy.setHorizontalStretch( 1 )
        sizePolicy.setVerticalStretch( 0 )
        sizePolicy.setHeightForWidth( self.comboBox_project.sizePolicy().hasHeightForWidth() )
        self.comboBox_project.setSizePolicy( sizePolicy )
        self.comboBox_project.setCursor( QtCore.Qt.ArrowCursor )
        self.comboBox_project.setAcceptDrops( False )
        self.comboBox_project.setAccessibleName( "" )
        self.comboBox_project.setLayoutDirection( QtCore.Qt.LeftToRight )
        self.comboBox_project.setAutoFillBackground ( False )
        self.comboBox_project.setObjectName ( "comboBox_project" )
        self.horizontalLayout_project.addWidget( self.comboBox_project )
        self.verticalLayout.addLayout( self.horizontalLayout_project )

        # Homeworks root
        self.horizontalLayout_root = QtGui.QHBoxLayout ()
        self.horizontalLayout_root.setObjectName ( "horizontalLayout_root" )
        self.label_root = QtGui.QLabel ( self )
        self.label_root.setObjectName ( "label_root" )
        self.label_root.setMinimumSize ( QtCore.QSize ( 80, 0 ) )
        self.horizontalLayout_root.addWidget ( self.label_root )
        self.labelpixmap_root = QtGui.QLabel ( self )
        self.labelpixmap_root.setObjectName ( "labelpixmap_root" )
        self.horizontalLayout_root.addWidget ( self.labelpixmap_root )
        self.lineEdit_root = QtGui.QLineEdit ( self )
        self.lineEdit_root.setObjectName ( "lineEdit_root" )
        self.horizontalLayout_root.addWidget ( self.lineEdit_root )
        self.verticalLayout.addLayout ( self.horizontalLayout_root )

        # Description
        self.horizontalLayout_4 = QtGui.QHBoxLayout ()
        self.horizontalLayout_4.setObjectName ( "horizontalLayout_4" )
        self.label_4 = QtGui.QLabel ( self )
        self.label_4.setObjectName ( "label_4" )
        self.label_4.setMinimumSize( QtCore.QSize( 80, 0 ) )
        self.horizontalLayout_4.addWidget ( self.label_4 )
        self.verticalLayout.addLayout ( self.horizontalLayout_4 )
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName( "horizontalLayout_5" )
        self.plainTextEdit = QtGui.QPlainTextEdit( self )
        self.plainTextEdit.setReadOnly( True )
        self.plainTextEdit.setObjectName( "plainTextEdit" )
        self.horizontalLayout_5.addWidget( self.plainTextEdit )
        self.verticalLayout.addLayout( self.horizontalLayout_5 )

        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName( "horizontalLayout_6" )
        spacerItem = QtGui.QSpacerItem ( 40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
        self.horizontalLayout_6.addItem( spacerItem )
        self.pushButton = QtGui.QPushButton( self )
        self.pushButton.setObjectName( "pushButton" )
        self.horizontalLayout_6.addWidget( self.pushButton )
        self.verticalLayout.addLayout( self.horizontalLayout_6 )
        self.verticalLayout_2.addLayout( self.verticalLayout )

        self.setUi ()
        self.comboBox_project.currentIndexChanged.connect ( self.projectChanged )
        self.refresh.clicked.connect ( self.refreshClicked )
        self.pushButton.clicked.connect ( self.synchonizeClicked )

        QtCore.QMetaObject.connectSlotsByName ( self )


    def setUi ( self ):
        """Username"""
        username = "admin"
        icon = utils.getIconPath( "admin" )
        self.label_username.setText ( "DB user" )
        self.labelpixmap_username.setPixmap ( icon )
        self.lineEdit_username.setText ( username )

        """Password"""
        password = "admin"
        icon = utils.getIconPath( "password" )
        self.label_password.setText ( "DB password" )
        self.labelpixmap_password.setPixmap ( icon )
        self.lineEdit_password.setText ( password )

        """DB adress"""
        adress = "127.0.0.1:5984"
        icon = utils.getIconPath( "adress" )
        self.label_adress.setText ( "DB adress" )
        self.labelpixmap_adress.setPixmap ( icon )
        self.lineEdit_adress.setText ( adress )

        """DB project"""
        icon = utils.getIconPath( "refresh" )
        self.label_project.setText ( "DB project" )
        self.refresh.setIcon ( QtGui.QIcon ( icon ) )


        """Homework root"""
        root = "/homeworks"
        icon = utils.getIconPath( "hierarchy" )
        self.label_root.setText ( "Project root" )
        self.lineEdit_root.setText ( root )
        self.lineEdit_root.setReadOnly ( True )
        self.labelpixmap_root.setPixmap ( icon )

        """Description"""
        icon = utils.getIconPath( "pull" )
        self.label_4.setText ( "Description" )
        self.plainTextEdit.setPlainText ( "This is the project" )
        self.pushButton.setText ( "Synchronize" )
        self.pushButton.setIcon ( QtGui.QIcon ( icon ) )

        self.project_stat = dict ()
        self.project_stat [ "No project available" ] = False
        self.project_stat [ "" ] = False

        self.refreshClicked ()
        self.projectChanged()


if __name__ == '__main__':
    app = QtGui.QApplication ( sys.argv )
    main = UiProjectCloner ()
    main.show()
    app.exec_()
    sys.exit()
