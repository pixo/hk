# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template_task.ui'
#
# Created: Sun Jan 13 23:47:14 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(972, 806)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.type = QtGui.QListWidget(self.centralwidget)
        self.type.setObjectName("type")
        QtGui.QListWidgetItem(self.type)
        QtGui.QListWidgetItem(self.type)
        QtGui.QListWidgetItem(self.type)
        QtGui.QListWidgetItem(self.type)
        self.horizontalLayout_2.addWidget(self.type)
        self.asset = QtGui.QListWidget(self.centralwidget)
        self.asset.setObjectName("asset")
        QtGui.QListWidgetItem(self.asset)
        self.horizontalLayout_2.addWidget(self.asset)
        self.task = QtGui.QListWidget(self.centralwidget)
        self.task.setObjectName("task")
        self.horizontalLayout_2.addWidget(self.task)
        self.fork = QtGui.QListWidget(self.centralwidget)
        self.fork.setObjectName("fork")
        self.horizontalLayout_2.addWidget(self.fork)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.type.isSortingEnabled()
        self.type.setSortingEnabled(False)
        self.type.item(0).setText(QtGui.QApplication.translate("MainWindow", "asdas", None, QtGui.QApplication.UnicodeUTF8))
        self.type.item(1).setText(QtGui.QApplication.translate("MainWindow", "asdas", None, QtGui.QApplication.UnicodeUTF8))
        self.type.item(2).setText(QtGui.QApplication.translate("MainWindow", "sas", None, QtGui.QApplication.UnicodeUTF8))
        self.type.item(3).setText(QtGui.QApplication.translate("MainWindow", "sad", None, QtGui.QApplication.UnicodeUTF8))
        self.type.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.asset.isSortingEnabled()
        self.asset.setSortingEnabled(False)
        self.asset.item(0).setText(QtGui.QApplication.translate("MainWindow", "asd", None, QtGui.QApplication.UnicodeUTF8))
        self.asset.setSortingEnabled(__sortingEnabled)
        self.label.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Pull", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Push", None, QtGui.QApplication.UnicodeUTF8))

