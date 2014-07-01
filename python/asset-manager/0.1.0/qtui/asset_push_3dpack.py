# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asset_push_3dpack.ui'
#
# Created: Sat Feb  9 18:30:50 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(394, 666)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_main = QtGui.QVBoxLayout()
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_launcher = QtGui.QLabel(Form)
        self.label_launcher.setMinimumSize(QtCore.QSize(16, 16))
        self.label_launcher.setMaximumSize(QtCore.QSize(16, 16))
        self.label_launcher.setText("")
        self.label_launcher.setObjectName("label_launcher")
        self.horizontalLayout_2.addWidget(self.label_launcher)
        self.label_proj = QtGui.QLabel(Form)
        self.label_proj.setObjectName("label_proj")
        self.horizontalLayout_2.addWidget(self.label_proj)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.labelImage = QtGui.QLabel(Form)
        self.labelImage.setMinimumSize(QtCore.QSize(300, 300))
        self.labelImage.setText("")
        self.labelImage.setObjectName("labelImage")
        self.verticalLayout_3.addWidget(self.labelImage)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.screenshotButton = QtGui.QPushButton(Form)
        self.screenshotButton.setObjectName("screenshotButton")
        self.horizontalLayout.addWidget(self.screenshotButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_comments = QtGui.QLabel(Form)
        self.label_comments.setAlignment(QtCore.Qt.AlignCenter)
        self.label_comments.setObjectName("label_comments")
        self.verticalLayout_3.addWidget(self.label_comments)
        self.plainTextEdit_comments = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit_comments.setMinimumSize(QtCore.QSize(300, 0))
        self.plainTextEdit_comments.setObjectName("plainTextEdit_comments")
        self.verticalLayout_3.addWidget(self.plainTextEdit_comments)
        self.verticalLayout_main.addLayout(self.verticalLayout_3)
        self.horizontalLayout_bottom = QtGui.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setMinimumSize(QtCore.QSize(300, 0))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_bottom.addWidget(self.progressBar)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_bottom.addItem(spacerItem1)
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
        self.label_proj.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Push Asset :</span><span style=\" font-size:12pt;\"> Project name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.screenshotButton.setText(QtGui.QApplication.translate("Form", "Screenshot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_comments.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">User comments</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Push", None, QtGui.QApplication.UnicodeUTF8))

