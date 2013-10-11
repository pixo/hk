'''
Created on Mar 5, 2013

@author: pixo
'''
import sys, re
import pipeline.core as core
from PySide import QtCore, QtGui

class UiProjectCreator ( QtGui.QMainWindow ):
            
    def pushButtonClicked(self):
        name = self.lineEdit.text()
        
        if name == "":
            msg = "Can't create asset '%s' no characters in name"
            self.statusbar.showMessage (msg % name)
            return
        
        if re.sub("[a-z]","", name) != "":
            msg = "Can't create Project '%s', invalid characters" % name
            self.statusbar.showMessage( msg )
            return
                    
        description = self.plainTextEdit.toPlainText()
        db_name = self.lineEdit_2.text()
        db_server = self.lineEdit_3.text()
                 
        doc = core.createProject ( name = name, description = description,
                                   db_server = db_server, db_name = db_name )
           
        if doc :
            msg = "'%s' added to db '%s'" % ( name, db_name )
            self.statusbar.showMessage ( msg )
            print msg
            self.close ()
    
    def descriptionChanged( self ):  
        description = self.plainTextEdit.toPlainText()
        if description == "" :
            self.pushButton.setEnabled ( False )
        else :
            self.pushButton.setEnabled ( True )
    
    def signalConnect(self):
        """ Connect the UI to the Ui_AssetWindow methods """
        self.pushButton.clicked.connect( self.pushButtonClicked )
        self.plainTextEdit.textChanged.connect( self.descriptionChanged )
    
    def __init__(self, parent=None):
        super(UiProjectCreator, self).__init__(parent)
        
        self.setObjectName("MainWindow")
        self.setWindowTitle("Project creator")
       
        self.resize(585, 482)
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(80, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setMinimumSize(QtCore.QSize(80, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QtCore.QSize(80, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        #self.lineEdit_3.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_5.addWidget(self.lineEdit_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)  
        
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.plainTextEdit = QtGui.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_4.addWidget(self.plainTextEdit)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.pushButton.setEnabled ( False )
        self.label_2.setText ( "Project slug" )
        self.lineEdit.setText ( "prj" )
        
        #Database attrs
        self.label_3.setText ( "DB name" )
        self.lineEdit_2.setText ( "projects" )
        self.label_4.setText ( "DB server" )
        self.lineEdit_3.setText ( "admin:password@127.0.0.1:5984" )
        self.label.setText( "Description" )
        self.pushButton.setText( "Create" )
        
        self.signalConnect()
        QtCore.QMetaObject.connectSlotsByName(self)
    
if __name__ == '__main__':
    app = QtGui.QApplication ( sys.argv )    
    main = UiProjectCreator()
    main.show()
    app.exec_()
    sys.exit()
