# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asset_pull.ui'
#
# Created: Thu Jan 17 13:54:00 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(556, 532)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_search = QtGui.QLineEdit(Form)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.verticalLayout.addWidget(self.lineEdit_search)
        self.listWidget_version = QtGui.QListWidget(Form)
        self.listWidget_version.setObjectName("listWidget_version")
        self.verticalLayout.addWidget(self.listWidget_version)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelImage = QtGui.QLabel(Form)
        self.labelImage.setMinimumSize(QtCore.QSize(300, 300))
        self.labelImage.setText("")
        self.labelImage.setObjectName("labelImage")
        self.verticalLayout_2.addWidget(self.labelImage)
        self.plainTextEdit_comment = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit_comment.setEnabled(False)
        self.plainTextEdit_comment.setObjectName("plainTextEdit_comment")
        self.verticalLayout_2.addWidget(self.plainTextEdit_comment)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_main.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.pullButton = QtGui.QPushButton(Form)
        self.pullButton.setObjectName("pullButton")
        self.horizontalLayout_3.addWidget(self.pullButton)
        self.verticalLayout_main.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_main)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.plainTextEdit_comment.setPlainText(QtGui.QApplication.translate("Form", "mabite", None, QtGui.QApplication.UnicodeUTF8))
        self.pullButton.setText(QtGui.QApplication.translate("Form", "Pull", None, QtGui.QApplication.UnicodeUTF8))

