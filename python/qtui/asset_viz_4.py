# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asset_viz_3.ui'
#
# Created: Tue Feb  5 00:02:25 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!
import sys, os
from PySide import QtCore, QtGui

class Ui_MainWindow ( QtGui.QMainWindow ) :
    def __init__(self, parent=None):

        super(Ui_MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.resize(668, 715)
        self.centralwidget = QtGui.QWidget(self)
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
        self.label_sys.setMaximumSize(QtCore.QSize(21, 21))
        self.label_sys.setObjectName("label_sys")
        self.horizontalLayout_6.addWidget(self.label_sys)
        self.label_proj = QtGui.QLabel(self.centralwidget)
        self.label_proj.setObjectName("label_proj")
        self.horizontalLayout_6.addWidget(self.label_proj)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_filter = QtGui.QLabel(self.centralwidget)
        self.label_filter.setEnabled(True)
        self.label_filter.setMaximumSize(QtCore.QSize(16, 16))
        self.label_filter.setObjectName("label_filter")
        self.horizontalLayout_4.addWidget(self.label_filter)
        self.comboBox_a = QtGui.QComboBox(self.centralwidget)
        self.comboBox_a.setObjectName("comboBox_a")
        self.comboBox_a.addItem("")
        self.comboBox_a.addItem("")
        self.comboBox_a.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_a)
        self.comboBox_b = QtGui.QComboBox(self.centralwidget)
        self.comboBox_b.setObjectName("comboBox_b")
        self.comboBox_b.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_b)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(16, 16))
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.lineEdit_a = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_a.setObjectName("lineEdit_a")
        self.horizontalLayout_5.addWidget(self.lineEdit_a)
        self.lineEdit_b = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_b.setObjectName("lineEdit_b")
        self.horizontalLayout_5.addWidget(self.lineEdit_b)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.treeWidget_a = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget_a.setAlternatingRowColors(True)
        self.treeWidget_a.setObjectName("treeWidget_a")
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_a)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setItalic(False)
        font.setBold(True)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_2 = QtGui.QTreeWidgetItem(item_1)
        font = QtGui.QFont()
        font.setItalic(True)
        item_2 = QtGui.QTreeWidgetItem(item_1)
        font = QtGui.QFont()
        font.setItalic(True)
        item_2 = QtGui.QTreeWidgetItem(item_1)
        font = QtGui.QFont()
        font.setItalic(True)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        self.verticalLayout.addWidget(self.treeWidget_a)
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
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.verticalLayout_main.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_main)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sys.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_proj.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Project</span><span style=\" font-size:12pt;\"/><span style=\" font-size:12pt; font-weight:600;\">:</span><span style=\" font-size:12pt;\"> Project name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_filter.setText(QtGui.QApplication.translate("MainWindow", "filter", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_a.setItemText(0, QtGui.QApplication.translate("MainWindow", "environment", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_a.setItemText(1, QtGui.QApplication.translate("MainWindow", "character", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_a.setItemText(2, QtGui.QApplication.translate("MainWindow", "prop", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_b.setItemText(0, QtGui.QApplication.translate("MainWindow", "model", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "search", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_a.setSortingEnabled(True)
        self.treeWidget_a.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "asset", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.treeWidget_a.isSortingEnabled()
        self.treeWidget_a.setSortingEnabled(False)
        self.treeWidget_a.topLevelItem(0).setText(0, QtGui.QApplication.translate("MainWindow", "mickey", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_a.topLevelItem(0).child(0).setText(0, QtGui.QApplication.translate("MainWindow", "texture", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_a.topLevelItem(0).child(1).setText(0, QtGui.QApplication.translate("MainWindow", "surface", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_a.topLevelItem(0).child(1).child(0).setText(0, QtGui.QApplication.translate("MainWindow", "v003", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_a.topLevelItem(0).child(1).child(1).setText(0, QtGui.QApplication.translate("MainWindow", "v002", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_a.topLevelItem(0).child(1).child(2).setText(0, QtGui.QApplication.translate("MainWindow", "v001", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_a.topLevelItem(0).child(2).setText(0, QtGui.QApplication.translate("MainWindow", "rig", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_a.topLevelItem(0).child(3).setText(0, QtGui.QApplication.translate("MainWindow", "model", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_a.setSortingEnabled(__sortingEnabled)

app = QtGui.QApplication(sys.argv)

main = Ui_MainWindow()
main.show()

# Enter Qt application main loop
app.exec_()
sys.exit()