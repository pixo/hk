# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asset_push_2.ui'
#
# Created: Tue Jan 15 22:57:30 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(665, 573)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout_top = QtGui.QHBoxLayout()
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")
        self.label_file = QtGui.QLabel(Form)
        self.label_file.setAlignment(QtCore.Qt.AlignCenter)
        self.label_file.setObjectName("label_file")
        self.horizontalLayout_top.addWidget(self.label_file)
        self.label_comments = QtGui.QLabel(Form)
        self.label_comments.setAlignment(QtCore.Qt.AlignCenter)
        self.label_comments.setObjectName("label_comments")
        self.horizontalLayout_top.addWidget(self.label_comments)
        self.verticalLayout_main.addLayout(self.horizontalLayout_top)
        self.horizontalLayout_center = QtGui.QHBoxLayout()
        self.horizontalLayout_center.setObjectName("horizontalLayout_center")
        self.verticalLayout_file = QtGui.QVBoxLayout()
        self.verticalLayout_file.setObjectName("verticalLayout_file")
        self.lineEdit_file = QtGui.QLineEdit(Form)
        self.lineEdit_file.setObjectName("lineEdit_file")
        self.verticalLayout_file.addWidget(self.lineEdit_file)
        self.listWidget_file = QtGui.QListWidget(Form)
        self.listWidget_file.setObjectName("listWidget_file")
        item = QtGui.QListWidgetItem(self.listWidget_file)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.verticalLayout_file.addWidget(self.listWidget_file)
        self.horizontalLayout_center.addLayout(self.verticalLayout_file)
        self.plainTextEdit_comments = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit_comments.setObjectName("plainTextEdit_comments")
        self.horizontalLayout_center.addWidget(self.plainTextEdit_comments)
        self.verticalLayout_main.addLayout(self.horizontalLayout_center)
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_bottom.addWidget(self.progressBar)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_bottom.addWidget(self.pushButton)
        self.verticalLayout_main.addLayout(self.horizontalLayout_bottom)
        self.verticalLayout_2.addLayout(self.verticalLayout_main)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Asset Push", None, QtGui.QApplication.UnicodeUTF8))
        self.label_file.setText(QtGui.QApplication.translate("Form", "File ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_comments.setText(QtGui.QApplication.translate("Form", "Comments", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listWidget_file.isSortingEnabled()
        self.listWidget_file.setSortingEnabled(False)
        self.listWidget_file.item(0).setText(QtGui.QApplication.translate("Form", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_file.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Push", None, QtGui.QApplication.UnicodeUTF8))

