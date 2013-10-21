'''
Created on Oct 19, 2013

@author: pixo
'''
import sys, os
import pipeline.core as core
import pipeline.utils as utils
from PySide import QtCore, QtGui

class UiProjectCloner ( QtGui.QWidget ):
    
    def refreshClicked (self):
        serveradress = self.lineEdit.text ()
        """Refresh projects, icons"""
        self.refreshAdress ( serveradress )
        self.refreshProject ( serveradress )
        
        if self.server and self.projects and len ( self.projects ) > 0 :
            self.pushButton.setEnabled ( True )
            
        else:
            self.pushButton.setEnabled ( False )
        
    def projectChanged (self):
        if not self.server:
            self.plainTextEdit.setPlainText ( "" )
            return
        
        current = self.comboBox.currentText ()
        root = "/homeworks"
        
        """"Project Descriptions"""
        description = ""
        
        """"Check description for initialiation or none available project"""
        if not ( current in [ "", "No project available" ] ) :
            description = self.server[current][current]["description"]
            root = self.server[current][current]["root"]
                
        self.lineEdit_2.setText ( root )
        self.plainTextEdit.setPlainText ( description )
        
    def synchonizeClicked (self):
        ""
        project = self.comboBox.currentText ()
        db_adress = self.lineEdit.text ()
        db = self.server [ project ][ project ]
        host = db [ "host" ]
        local = db [ "root" ]
        
        source = os.path.join ( host, "projects", project )
        destination = os.path.join ( local, "projects" )
        utils.rsync ( source, destination )
#         utils.rsync ( source, destination, ["sct","tex"] )
        core.createProjectCred ( project, db_adress, host )
        
        self.close ()
        
    def refreshAdress ( self, serveradress ):                
        """If server exist set 'ok' icon """
        icon = os.path.join ( utils.getCCPath (), "cross.png" )
        self.server = False
        
        if utils.serverExists ( serveradress ) :
            icon = os.path.join ( utils.getCCPath (), "ok.png" )
            self.server = utils.getServer ( serveradress )
            
#         self.labelpixmap.setPixmap ( icon )
        self.refresh.setIcon ( QtGui.QIcon ( icon ) )

    def refreshProject ( self, serveradress ):
        """Clear current combobox list"""
        self.comboBox.clear ()
        icon = os.path.join ( utils.getCCPath (), "cross.png" )
        self.projects = ["No project available"]
        
        if utils.serverExists ( serveradress ) :
            projects = core.lsServerProjects ( serveradress )
            
            if len ( projects ) > 0 :
                self.projects = projects
                icon = os.path.join ( utils.getCCPath (), "ok.png" )
            
        self.comboBox.addItems ( self.projects )
        self.labelpixmap_2.setPixmap ( icon )
                
    def __init__(self, parent=None):
        super ( UiProjectCloner, self ).__init__( parent )
        
        self.setObjectName ( "MainWindow" )
        self.setWindowTitle ( "Project Cloner" )
        self.resize ( 570, 470 )
        
        self.verticalLayout_2 = QtGui.QVBoxLayout ( self )
        self.verticalLayout_2.setObjectName ( "verticalLayout_2" )
        self.verticalLayout = QtGui.QVBoxLayout ()
        self.verticalLayout.setObjectName ( "verticalLayout" )
        
        self.horizontalLayout = QtGui.QHBoxLayout ()
        self.horizontalLayout.setObjectName ( "horizontalLayout" )
        self.label = QtGui.QLabel ( self )
        self.label.setObjectName ( "label" )
        self.label.setMinimumSize(QtCore.QSize(80, 0))
        self.horizontalLayout.addWidget ( self.label )
        self.refresh = QtGui.QPushButton(self)
        self.refresh.setObjectName("refresh")
        self.horizontalLayout.addWidget ( self.refresh )        
#         self.labelpixmap = QtGui.QLabel ( self )
#         self.labelpixmap.setObjectName ( "labelpixmap" )
#         self.horizontalLayout.addWidget ( self.labelpixmap )
        self.lineEdit = QtGui.QLineEdit ( self )
        self.lineEdit.setObjectName ( "lineEdit" )
        self.horizontalLayout.addWidget ( self.lineEdit )
        self.verticalLayout.addLayout ( self.horizontalLayout )
        
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel ( self )
        self.label_2.setObjectName ( "label_2" )
        self.label_2.setMinimumSize(QtCore.QSize(80, 0))
        self.horizontalLayout_2.addWidget ( self.label_2 )
        self.labelpixmap_2 = QtGui.QLabel ( self )
        self.labelpixmap_2.setObjectName ( "labelpixmap_2" )
        self.labelpixmap_2.setMinimumSize ( QtCore.QSize(30, 0) )
        self.horizontalLayout_2.addWidget ( self.labelpixmap_2 )
        self.comboBox = QtGui.QComboBox ( self )
        self.comboBox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setCursor(QtCore.Qt.ArrowCursor)
        self.comboBox.setAcceptDrops(False)
        self.comboBox.setAccessibleName("")
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setAutoFillBackground ( False )
        self.comboBox.setObjectName ( "comboBox" )
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        
        self.horizontalLayout_3 = QtGui.QHBoxLayout ()
        self.horizontalLayout_3.setObjectName ( "horizontalLayout_3" )
        self.label_3 = QtGui.QLabel ( self )
        self.label_3.setObjectName ( "label_3" )
        self.label_3.setMinimumSize(QtCore.QSize(105, 0))
        self.horizontalLayout_3.addWidget ( self.label_3 )
        self.labelpixmap_3 = QtGui.QLabel ( self )
        self.labelpixmap_3.setObjectName ( "labelpixmap_3" )
        self.horizontalLayout_3.addWidget ( self.labelpixmap_3 )
        self.lineEdit_2 = QtGui.QLineEdit ( self )
        self.lineEdit_2.setObjectName ( "lineEdit_2" )
        self.horizontalLayout_3.addWidget ( self.lineEdit_2 )
        self.verticalLayout.addLayout ( self.horizontalLayout_3 )
        
        self.horizontalLayout_4 = QtGui.QHBoxLayout ()
        self.horizontalLayout_4.setObjectName ( "horizontalLayout_4" )
        self.label_4 = QtGui.QLabel ( self )
        self.label_4.setObjectName ( "label_4" )
        self.label_4.setMinimumSize(QtCore.QSize(80, 0))
        self.horizontalLayout_4.addWidget ( self.label_4 )
        self.verticalLayout.addLayout ( self.horizontalLayout_4 )
        
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.plainTextEdit = QtGui.QPlainTextEdit(self)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout_5.addWidget(self.plainTextEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        
        self.setUi ()
#         self.lineEdit.textChanged.connect ( self.adressChanged )
        self.comboBox.currentIndexChanged.connect ( self.projectChanged )
        self.refresh.clicked.connect ( self.refreshClicked )
        self.pushButton.clicked.connect ( self.synchonizeClicked )

        QtCore.QMetaObject.connectSlotsByName ( self )


    def setUi ( self ):
        ccpath = utils.getCCPath()
        
        """DB adress"""
        adress = "admin:password@127.0.0.1:5984"
        self.label.setText ( "DB adress" )
        self.lineEdit.setText ( adress )
        
        """DB project"""
        self.label_2.setText ( "DB project" )

        """Homework root"""
        self.label_3.setText ( "Project root" )
        self.lineEdit_2.setText ( "/homeworks" )
        self.lineEdit_2.setReadOnly ( True )
        
        """Description"""
        self.label_4.setText ( "Description" )
        self.plainTextEdit.setPlainText ( "This is the project" )
        self.pushButton.setText ( "Synchronize" )
        self.pushButton.setIcon ( QtGui.QIcon ( os.path.join ( ccpath, "pull.png" ) ) )
        
        self.refreshClicked ()
        self.projectChanged()
        
        
if __name__ == '__main__':
    app = QtGui.QApplication ( sys.argv )    
    main = UiProjectCloner ()
    main.show()
    app.exec_()
    sys.exit()
