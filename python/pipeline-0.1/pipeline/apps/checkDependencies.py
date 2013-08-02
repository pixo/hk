'''
Created on Jul 31, 2013

@author: pixo
'''
from PySide import QtCore, QtGui
import pipeline.utils as utils
import pipeline.core as core
import sys, os

try :
    CC_PATH = utils.getCCPath()
except:
    CC_PATH = "/tmp"
    print "assetManager module: Can't set CC_PATH \n set CC_PATH > /tmp"

def getRefsFromFile ( fname ):
    """open file"""
    fil = open( fname, "r" )
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

class UiCheckDependencies ( QtGui.QMainWindow ):
    
    launcher = "terminal"
        
    def getPaths (self):
        fname = "/homeworks/users/pixo/projects/testing/shot/op001/lay/a/testing_shot_op001_lay_a.v003.base1/testing_shot_op001_lay_a.ma"
        return getRefsFromFile ( fname )
    
    def getVersionFromPath ( self, path ):
        repo = os.getenv ( "HK_REPO" )
        result = path.replace ( repo + os.sep, "" )
        version = result.split ( os.sep )[5] 
        return version 
    
    def getVersionsList ( self, id = "" ):
        paths = core.getAssetVersions ( id )
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
        versions = comboBox.doc [ "versions" ]
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

    def tableClicked (self, item):        
        comboBox = self.tableWidget.cellWidget ( item.row (), 0  )
        self.updateInfos ( comboBox )
        
    def buildTable (self):        
        paths = self.getPaths ()
        row = len ( paths )
        
        self.tableWidget = QtGui.QTableWidget ( row, 2 )
        self.tableWidget.setHorizontalScrollBarPolicy ( QtCore.Qt.ScrollBarAlwaysOff )
        self.tableWidget.setAlternatingRowColors ( True )
        self.tableWidget.horizontalHeader().setStretchLastSection ( True )
        self.tableWidget.horizontalHeader().setMinimumSectionSize ( 200 )
        self.tableWidget.verticalHeader().hide ()
        self.tableWidget.horizontalHeader().hide ()
        self.tableWidget.setSelectionMode ( QtGui.QAbstractItemView.SingleSelection )
        self.tableWidget.setSelectionBehavior ( QtGui.QAbstractItemView.SelectRows )
        self.tableWidget.resizeColumnToContents ( True )
        self.tableWidget.setMouseTracking ( False )
        self.verticalLayout.addWidget( self.tableWidget )
        self.tableWidget.itemClicked.connect ( self.tableClicked )
        self.tableWidget.cellClicked.connect ( self.comboxChanged )
                
        count = 0
        
        for path in paths :
            
            doc_id = self.getDocIdFromPath ( path )
            current_version = self.getVersionFromPath ( path )       
            versions = self.getVersionsList ( doc_id )
            
            comboBox = QtGui.QComboBox ( )
            comboBox.doc = self.db [ doc_id ]
            comboBox.addItems ( versions )
            comboBox.setCurrentIndex ( comboBox.findText ( current_version ) )
            comboBox.activated.connect ( self.comboxChanged )
            comboBox.versions = versions
            
            if current_version == versions [ -1 ] :
                bg_color = QtGui.QColor ( 128, 255, 128 )
            
            else:
                bg_color = QtGui.QColor ( 255, 128, 128 )

            item = QtGui.QTableWidgetItem ( doc_id )
            item.setFlags ( QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled )
            item.setBackground ( bg_color )
            comboBox.docItem = item
            
            self.tableWidget.setCellWidget ( count, 0, comboBox )
            self.tableWidget.setItem ( count, 1, item )
                        
            count += 1

    def __init__(self, parent=None):
        super ( UiCheckDependencies, self).__init__(parent)
        
        self.db = utils.getDb ()
        self.setObjectName("MainWindow")
        self.resize(642, 726)
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
        self.plainTextEdit_description.setEnabled(False)
        self.plainTextEdit_description.setPlainText("")
        self.plainTextEdit_description.setObjectName("plainTextEdit_description")
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
                                    font-weight:600;\">Asset updater </span><span style=\" font-size:12pt;
                                    \"/><span style=\" font-size:12pt;font-weight:600;
                                    \">:</span><span style=\" font-size:12pt;
                                    \"> '%s'</span></p></body></html>""" % (os.getenv ( "HK_PROJECT" ) ) )       
        
        self.buildTable ()
        
        QtCore.QMetaObject.connectSlotsByName(self)
                
def cli () :
    app = QtGui.QApplication ( sys.argv )
    main = UiCheckDependencies ()
    main.show()
    app.exec_()
    sys.exit()
    
if __name__ == '__main__':
    cli ()