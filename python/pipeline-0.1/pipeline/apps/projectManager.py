'''
Created on Mar 5, 2013

@author: pixo
'''
import sys
import pipeline.core as core
from PySide import QtCore, QtGui

class UiProjectCreator ( QtGui.QMainWindow ):
            
    def pushButtonClicked(self):
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
        db_user = self.lineEdit_2.text()
        db_password = self.lineEdit_3.text()
        db_server = self.lineEdit_4.text()
        db_name = self.lineEdit_5.text()
        host_user = self.lineEdit_6.text()
        host_password = self.lineEdit_7.text()
        host_server = self.lineEdit_8.text()
                        
        doc = core.createProject ( name = name,
                                 description = description,
                                 db_user = db_user,
                                 db_password = db_password,
                                 db_server = db_server,
                                 dbname = db_name,
                                 host_user = host_user,
                                 host_password = host_password,
                                 host_server = host_server )
         
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
        self.label_2.setMinimumSize(QtCore.QSize(60, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setMinimumSize(QtCore.QSize(60, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QtCore.QSize(60, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_3.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_5.addWidget(self.lineEdit_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setMinimumSize(QtCore.QSize(60, 0))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.lineEdit_4 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_6.addWidget(self.lineEdit_4)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setMinimumSize(QtCore.QSize(60, 0))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.lineEdit_5 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_7.addWidget(self.lineEdit_5)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setMinimumSize(QtCore.QSize(60, 0))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.lineEdit_6 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.horizontalLayout_8.addWidget(self.lineEdit_6)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setMinimumSize(QtCore.QSize(60, 0))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        self.lineEdit_7 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_7.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_9.addWidget(self.lineEdit_7)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setMinimumSize(QtCore.QSize(60, 0))
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_10.addWidget(self.label_9)
        self.lineEdit_8 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.horizontalLayout_10.addWidget(self.lineEdit_8)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        
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
        self.label_2.setText ( "Project" )
        self.lineEdit.setText ( "NewProject" )
        
        #Database attrs
        self.label_3.setText ( "DB User" )
        self.lineEdit_2.setText ( "admin" )
        self.label_4.setText ( "DB Password" )
        self.lineEdit_3.setText ( "admin" )
        self.label_5.setText ( "DB Server" )
        self.lineEdit_4.setText ( "127.0.0.1:5984" )
        self.label_6.setText ( "DB Name" )
        self.lineEdit_5.setText ( "projects" )
        
        #Host attrs
        self.label_7.setText ( "Host User" )
        self.lineEdit_6.setText ( "homeworks" )
        self.label_8.setText ( "Host Password" )
        self.lineEdit_7.setText ( "admin" )
        self.label_9.setText ( "Host Server" )
        self.lineEdit_8.setText ( "127.0.0.1" )
        
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
