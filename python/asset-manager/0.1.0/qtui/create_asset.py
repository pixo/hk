# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_asset.ui'
#
# Created: Sun Jan 27 18:52:05 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(486, 429)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_lineedit = QtGui.QLabel(Form)
        self.label_lineedit.setObjectName("label_lineedit")
        self.horizontalLayout.addWidget(self.label_lineedit)
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_description = QtGui.QLabel(Form)
        self.label_description.setObjectName("label_description")
        self.verticalLayout.addWidget(self.label_description)
        self.plainTextEdit = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.label_status = QtGui.QLabel(Form)
        self.label_status.setObjectName("label_status")
        self.verticalLayout.addWidget(self.label_status)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Create on database", None, QtGui.QApplication.UnicodeUTF8))
        self.label_lineedit.setText(QtGui.QApplication.translate("Form", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "create", None, QtGui.QApplication.UnicodeUTF8))
        self.label_description.setText(QtGui.QApplication.translate("Form", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_status.setText(QtGui.QApplication.translate("Form", "Status", None, QtGui.QApplication.UnicodeUTF8))

