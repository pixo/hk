# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_task_3.ui'
#
# Created: Sun Jun  9 16:14:21 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(803, 593)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout_center = QtGui.QHBoxLayout()
        self.horizontalLayout_center.setObjectName("horizontalLayout_center")
        self.verticalLayout_file = QtGui.QVBoxLayout()
        self.verticalLayout_file.setObjectName("verticalLayout_file")
        self.label_proj = QtGui.QLabel(Form)
        self.label_proj.setObjectName("label_proj")
        self.verticalLayout_file.addWidget(self.label_proj)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_fork = QtGui.QLabel(Form)
        self.label_fork.setMinimumSize(QtCore.QSize(30, 0))
        self.label_fork.setMaximumSize(QtCore.QSize(16, 16))
        self.label_fork.setObjectName("label_fork")
        self.horizontalLayout.addWidget(self.label_fork)
        self.lineEdit_fork = QtGui.QLineEdit(Form)
        self.lineEdit_fork.setObjectName("lineEdit_fork")
        self.horizontalLayout.addWidget(self.lineEdit_fork)
        self.verticalLayout_file.addLayout(self.horizontalLayout)
        self.listWidget_task = QtGui.QListWidget(Form)
        self.listWidget_task.setMinimumSize(QtCore.QSize(300, 0))
        self.listWidget_task.setObjectName("listWidget_task")
        self.verticalLayout_file.addWidget(self.listWidget_task)
        self.horizontalLayout_center.addLayout(self.verticalLayout_file)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_comments = QtGui.QLabel(Form)
        self.label_comments.setAlignment(QtCore.Qt.AlignCenter)
        self.label_comments.setObjectName("label_comments")
        self.verticalLayout.addWidget(self.label_comments)
        self.plainTextEdit_comments = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit_comments.setMinimumSize(QtCore.QSize(300, 0))
        self.plainTextEdit_comments.setObjectName("plainTextEdit_comments")
        self.verticalLayout.addWidget(self.plainTextEdit_comments)
        self.horizontalLayout_center.addLayout(self.verticalLayout)
        self.verticalLayout_main.addLayout(self.horizontalLayout_center)
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_bottom.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_bottom.addWidget(self.pushButton)
        self.verticalLayout_main.addLayout(self.horizontalLayout_bottom)
        self.labelStatus = QtGui.QLabel(Form)
        self.labelStatus.setText("")
        self.labelStatus.setObjectName("labelStatus")
        self.verticalLayout_main.addWidget(self.labelStatus)
        self.verticalLayout_2.addLayout(self.verticalLayout_main)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Asset Push", None, QtGui.QApplication.UnicodeUTF8))
        self.label_proj.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Create Task :</span><span style=\" font-size:12pt;\"> Project name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_fork.setText(QtGui.QApplication.translate("Form", "Fork", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_task.setSortingEnabled(True)
        self.label_comments.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Description</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "create", None, QtGui.QApplication.UnicodeUTF8))

