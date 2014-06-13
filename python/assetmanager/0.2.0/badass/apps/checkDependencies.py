'''
Created on Jul 31, 2013

@author: pixo
'''
from PySide import QtCore, QtGui
import badass.utils as utils
import badass.core as core
import sys, os

try :
    CC_PATH = utils.getCCPath()
except:
    CC_PATH = "/tmp"
    print "checkDependencies: Can't set CC_PATH \n set CC_PATH > /tmp"

#TODO make it works in maya and in cli

def getRefsFromFile ( fname ):
    """open file"""
    fil = open ( fname, "r" )
    lin = ""
    refs = list ()
    
    while lin.find ( "requires maya" ) < 0 :
        lin = fil.readline ()
        
        if lin.find ("//Name:") < 0 :
            for w in lin.split ( " " ): 
                
                if w.find (".mb") > 0 or w.find (".ma") > 0 :
                    for ch in ( '\n', '"', ';' ) : w = w.replace ( ch , "" )
                    
                    if not ( w in refs ) :
                        refs.append ( w )        
    fil.close()
    return refs

def setRefsToFile ( paths, fname ):
    """open file for reading"""
    fil = open ( fname, "r" )
    lines = fil.readlines() 
    maxline = len ( lines )
    
    for i in range ( 0, maxline ) :
        lin = lines [i] 
        
        if lin.find ( "requires maya" ) >= 0 :
            break
        
        if lin.find ("//Name:") < 0 :
            
            if lin.find (".mb") >= 0 or lin.find (".ma") >= 0 :
                
                for w in lin.split ( " " ):
                    
                    if w.find (".mb") > 0 or w.find (".ma") > 0 :
                        for ch in ( '\n', '"', ';' ) : w = w.replace ( ch , "" )
                
                        if w in paths :
                            lines [i] = lin.replace ( w, paths [ w ] )
                                                    
    fil.close()
    
    """open file for writing"""
    fil = open ( fname, "w" )
    fil.writelines ( lines )
    fil.close()
    
    return True

class UiCheckDependencies ( QtGui.QMainWindow ):
    
    launcher = "terminal"
            
    def getPaths (self):
        return getRefsFromFile ( self.fpath )
    
    def getVersionFromPath ( self, path ):
        repo = os.getenv ( "HK_REPO" )
        result = path.replace ( repo + os.sep, "" )
        version = result.split ( os.sep )[5] 
        return version 
    
    def getVersionsList ( self, doc_id = "" ):
        paths = core.getVersions ( db = self.db, doc_id = doc_id )
        versions = list ()
        
        for path in paths :
            versions.append ( os.path.basename ( path ) )
        
        return versions
    
    def getDocIdFromPath ( self, path ):
        fname = os.path.basename ( path )
        doc_id, ext = os.path.splitext ( fname ) 
        return doc_id
                        
    def updateInfos ( self, comboBox ):
        current_version = comboBox.currentText ()
        doc_id = comboBox.doc.id
        ver = str ( int ( current_version ) )        
        versions = comboBox.doc [ "review" ]
        path = versions [ ver ]["path" ]
        
        if current_version == comboBox.versions [ -1 ] :
            bg_color = QtGui.QColor ( 128, 255, 128 )
        
        else:
            bg_color = QtGui.QColor ( 255, 128, 128 )
            
        comboBox.docItem.setBackground ( bg_color )

        """Set the data to the plain text"""
        creator  = "Creator:\t%s\n" % versions [ ver ] [ 'creator' ]
        created  = "\nCreated:\t%s\n" % versions [ ver ] [ 'created' ]
        description = "\nDescription:\n\t%s\n" % versions [ ver ] [ 'description' ]
        
        pathinfo = "\nPath:\n\t%s\n" % os.path.expandvars( versions [ ver ] [ "path" ] )
        
        files ="\n\t".join ( map ( str, versions [ ver ] [ "files" ] ) )
        files = "\nFiles:\n\t%s\n" % files
         
        infos = creator + created + description + pathinfo + files
        self.plainTextEdit_description.setPlainText ( infos )

        """Set the screenshot"""
        screenshot = "%s.jpg" % doc_id
        screenshot = os.path.join( path, screenshot )
        
        if not os.path.exists ( screenshot ) :
            screenshot = os.path.join( CC_PATH, "hk_title_medium.png" )

        self.labelImage.setPixmap( screenshot )

    def comboxChanged ( self, value ):

        for i in range( 0, self.tableWidget.rowCount() ):
            comboBox = self.tableWidget.cellWidget ( i, 0 )
                        
            if comboBox.hasFocus():
                self.updateInfos ( comboBox )
                break

    def tableClicked (self, item):        
        comboBox = self.tableWidget.cellWidget ( item.row (), 0  )
        self.updateInfos ( comboBox )
        
    def updateAllClicked ( self ):
        
        for i in range ( 0, self.tableWidget.rowCount() ):
            comboBox = self.tableWidget.cellWidget ( i, 0 )
            item = self.tableWidget.item ( i, 1 )
            current_version = comboBox.currentText ()
            
            if current_version != comboBox.versions [-1] :
                comboBox.setCurrentIndex ( comboBox.findText ( comboBox.versions [-1] ) )
                item.setBackground ( QtGui.QColor ( 128, 255, 128 ) )
                        
    def doneClicked ( self ):
        switchDict = dict ()
                
        for i in range ( 0, self.tableWidget.rowCount() ):
            comboBox = self.tableWidget.cellWidget ( i, 0 )
            versions = comboBox.doc [ "review" ]
            ver = str ( int ( comboBox.currentText () ) )            
            src = comboBox.path
            dst = os.path.join ( versions [ ver ][ "path" ], os.path.basename ( comboBox.path ) )

            if os.path.exists ( src ) and os.path.exists ( dst ) :
                if src != dst :
                    switchDict [ src ] = dst
                
        self.switchReferences ( switchDict )
        self.close()
            
    def switchReferences ( self, paths ):
        setRefsToFile ( paths, self.fpath )
        
    def buildTable (self):              
        count = 0
        
        """Setup the items fonts"""    
        font = QtGui.QFont ()
        font.setPointSize ( 10 )
        font.setWeight ( 75 )
        font.setItalic ( False )
        font.setBold ( True )
                
        for path in self.paths :
            doc_id = self.getDocIdFromPath ( path )
            current_version = self.getVersionFromPath ( path )       
            versions = self.getVersionsList ( doc_id )
            
            comboBox = QtGui.QComboBox ()
            comboBox.doc = self.db [ doc_id ]
            comboBox.addItems ( versions )
            comboBox.setCurrentIndex ( comboBox.findText ( current_version ) )
            comboBox.activated.connect ( self.comboxChanged )
            comboBox.versions = versions
            comboBox.path = path
            
            if current_version == versions [ -1 ] :
                bg_color = QtGui.QColor ( 128, 255, 128 )
            
            else:
                bg_color = QtGui.QColor ( 255, 128, 128 )

            item = QtGui.QTableWidgetItem ( doc_id )
            item.setForeground ( QtGui.QBrush ( QtGui.QColor ( 0, 0, 0 ) ) )
            item.setIcon( QtGui.QIcon ( os.path.join ( CC_PATH, "%s.png" % core.getTypeFromId ( doc_id ) )))
            item.setFlags ( QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled )
            item.setBackground ( bg_color )
            item.setFont ( font )
            
            comboBox.docItem = item
            
            self.tableWidget.setCellWidget ( count, 0, comboBox )
            self.tableWidget.setItem ( count, 1, item )
                        
            count += 1

    def __init__( self, fpath = "", parent=None ):
        super ( UiCheckDependencies, self ).__init__(parent)
        
        self.fpath = fpath
        self.paths = self.getPaths ()
        self.db = utils.getDb ()
        
        self.setObjectName("MainWindow")
        self.resize ( 642, 726 )
        self.centralwidget = QtGui.QWidget ( self )
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
        self.label_sys = QtGui.QLabel(self.centralwidget)
        self.label_sys.setMaximumSize(QtCore.QSize(21, 16777215))
        self.label_sys.setObjectName("label_sys")
        self.horizontalLayout_6.addWidget(self.label_sys)
        self.label_proj = QtGui.QLabel(self.centralwidget)
        self.label_proj.setObjectName("label_proj")
        self.horizontalLayout_6.addWidget(self.label_proj)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
     
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelImage = QtGui.QLabel(self.centralwidget)
        self.labelImage.setMinimumSize(QtCore.QSize(300, 300))
        self.labelImage.setText("")
        self.labelImage.setObjectName("labelImage")
        self.verticalLayout_2.addWidget(self.labelImage)
        self.plainTextEdit_description = QtGui.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_description.setEnabled ( False )
        self.plainTextEdit_description.setPlainText("")
        self.plainTextEdit_description.setObjectName ( "plainTextEdit_description" )
        self.verticalLayout_2.addWidget(self.plainTextEdit_description)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_main.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_main)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.setWindowTitle("Check Dependencies")
        self.label_sys.setPixmap ( os.path.join ( CC_PATH, "%s.png" % self.launcher ) )
        self.label_proj.setText("""<html><head/><body><p><span style=\" font-size:12pt;
                                    font-weight:600;\">Asset Updater </span><span style=\" font-size:12pt;
                                    \"/><span style=\" font-size:12pt;font-weight:600;
                                    \">:</span><span style=\" font-size:12pt;
                                    \"> '%s'</span></p></body></html>""" % (os.getenv ( "HK_PROJECT" ) ) )        
                
        self.tableWidget = QtGui.QTableWidget ( len ( self.paths ), 2 )
        self.tableWidget.setHorizontalScrollBarPolicy ( QtCore.Qt.ScrollBarAlwaysOff )
        self.tableWidget.setAlternatingRowColors ( True )
        self.tableWidget.horizontalHeader().setStretchLastSection ( True )
        self.tableWidget.horizontalHeader().setMinimumSectionSize ( 200 )
        self.tableWidget.verticalHeader().hide ()
        self.tableWidget.horizontalHeader().hide ()
        self.tableWidget.setSelectionMode ( QtGui.QAbstractItemView.SingleSelection )
        self.tableWidget.resizeColumnToContents ( True )
        self.tableWidget.setMouseTracking ( False )
        self.verticalLayout.addWidget( self.tableWidget )
        self.tableWidget.itemClicked.connect ( self.tableClicked )
        self.tableWidget.cellClicked.connect ( self.comboxChanged )
        
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setFixedSize ( QtCore.QSize ( 80, 27 ) )
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setFixedSize( QtCore.QSize ( 60, 27 ) )
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton_2.setText ( "Update All" )
        self.pushButton_2.setIcon ( QtGui.QIcon ( os.path.join ( CC_PATH, "%s.png" % "refresh" ) ) )
        self.pushButton_2.clicked.connect ( self.updateAllClicked )
        self.pushButton.clicked.connect ( self.doneClicked )
        self.pushButton.setText ( "Done")
        self.pushButton.setIcon ( QtGui.QIcon ( os.path.join ( CC_PATH, "%s.png" % "done" ) ) )
        
        self.buildTable()
        QtCore.QMetaObject.connectSlotsByName(self)
                          
if __name__ == '__main__':
    app = QtGui.QApplication ( sys.argv )
    fpath = "/homeworks/projects/bls/shot/studio-bls/lay/main/006/bls_shot_studio-bls_lay_main.ma"
    main = UiCheckDependencies ( fpath = fpath )
    main.show ()
    app.exec_ ()
    sys.exit ()
