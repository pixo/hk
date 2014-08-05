'''
Created on Jul 13, 2014

@author: pixo
'''
import sys, time, os
from PySide import QtCore, QtGui
import badass.utils as utils
import badass.core as core

class UiBreakDown(QtGui.QMainWindow):
    def __init__(self, parent = None, assetManager = None):
        super(UiBreakDown, self).__init__(parent)

        self.project=utils.getProjectName()

        self.setObjectName("Breakdown")
        self.resize(864, 560)

        self.centralwidget=QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutMain=QtGui.QVBoxLayout(self.centralwidget)

        self.verticalLayoutMain.setObjectName("verticalLayoutMain")
        self.horizontalLayoutTitle=QtGui.QHBoxLayout()
        self.horizontalLayoutTitle.setObjectName("horizontalLayoutTitle")

        self.labelTitle=QtGui.QLabel(self.centralwidget)
        self.labelTitle.setObjectName("labelTitle")
        self.horizontalLayoutTitle.addWidget(self.labelTitle)
        self.verticalLayoutMain.addLayout(self.horizontalLayoutTitle)

        self.lineTitle=QtGui.QFrame(self.centralwidget)
        self.lineTitle.setFrameShape(QtGui.QFrame.HLine)
        self.lineTitle.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineTitle.setObjectName("lineTitle")
        self.verticalLayoutMain.addWidget(self.lineTitle)

        self.horizontalLayout=QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayoutAsset=QtGui.QVBoxLayout()
        self.verticalLayoutAsset.setObjectName("verticalLayoutAsset")
        self.horizontalLayoutAssetFilter=QtGui.QHBoxLayout()
        self.horizontalLayoutAssetFilter.setObjectName("horizontalLayoutAssetFilter")

        self.labelAssetSearch=QtGui.QLabel(self.centralwidget)
        self.labelAssetSearch.setObjectName("labelAssetSearch")
        self.horizontalLayoutAssetFilter.addWidget(self.labelAssetSearch)

        self.lineEditAssetSearch=QtGui.QLineEdit(self.centralwidget)
        self.lineEditAssetSearch.setObjectName("lineEditAssetSearch")
        self.horizontalLayoutAssetFilter.addWidget(self.lineEditAssetSearch)

        self.comboBoxAssetType=QtGui.QComboBox(self.centralwidget)
        self.comboBoxAssetType.setObjectName("comboBoxAssetType")
        self.horizontalLayoutAssetFilter.addWidget(self.comboBoxAssetType)

        self.pushButtonAssetRefresh=QtGui.QPushButton(self.centralwidget)
        self.pushButtonAssetRefresh.setMinimumSize(QtCore.QSize(24, 24))
        self.pushButtonAssetRefresh.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonAssetRefresh.setObjectName("pushButtonAssetRefresh")
        self.horizontalLayoutAssetFilter.addWidget(self.pushButtonAssetRefresh)

        self.verticalLayoutAsset.addLayout(self.horizontalLayoutAssetFilter)
        self.treeWidgetAsset=QtGui.QTreeWidget(self.centralwidget)
#         self.treeWidgetAsset.setDragEnabled(True)
#         self.treeWidgetAsset.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.treeWidgetAsset.setAlternatingRowColors(True)
        self.treeWidgetAsset.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeWidgetAsset.setRootIsDecorated(False)
        self.treeWidgetAsset.setItemsExpandable(False)
        self.treeWidgetAsset.setAnimated(True)
        self.treeWidgetAsset.setObjectName("treeWidgetAsset")
        item_0=QtGui.QTreeWidgetItem(self.treeWidgetAsset)
        self.verticalLayoutAsset.addWidget(self.treeWidgetAsset)

        self.horizontalLayout.addLayout(self.verticalLayoutAsset)
        self.lineAssetPackShot=QtGui.QFrame(self.centralwidget)
        self.lineAssetPackShot.setFrameShape(QtGui.QFrame.VLine)
        self.lineAssetPackShot.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineAssetPackShot.setObjectName("lineAssetPackShot")
        self.horizontalLayout.addWidget(self.lineAssetPackShot)

        self.verticalLayoutPackShot=QtGui.QVBoxLayout()
        self.verticalLayoutPackShot.setObjectName("verticalLayoutPackShot")
        self.horizontalLayoutPackFilter=QtGui.QHBoxLayout()
        self.horizontalLayoutPackFilter.setObjectName("horizontalLayoutPackFilter")
        self.labelPackFilter=QtGui.QLabel(self.centralwidget)
        self.labelPackFilter.setObjectName("labelPackFilter")
        self.horizontalLayoutPackFilter.addWidget(self.labelPackFilter)

        self.lineEditPackFilter=QtGui.QLineEdit(self.centralwidget)
        self.lineEditPackFilter.setObjectName("lineEditPackFilter")
        self.horizontalLayoutPackFilter.addWidget(self.lineEditPackFilter)
        self.verticalLayoutPackShot.addLayout(self.horizontalLayoutPackFilter)
        self.horizontalLayoutPackBar=QtGui.QHBoxLayout()
        self.horizontalLayoutPackBar.setObjectName("horizontalLayoutPackBar")

        self.pushButtonPackLink=QtGui.QPushButton(self.centralwidget)
        self.pushButtonPackLink.setMinimumSize(QtCore.QSize(24, 24))
        self.pushButtonPackLink.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonPackLink.setObjectName("pushButtonPackLink")
        self.horizontalLayoutPackBar.addWidget(self.pushButtonPackLink)

        self.pushButtonPackUnlink=QtGui.QPushButton(self.centralwidget)
        self.pushButtonPackUnlink.setMinimumSize(QtCore.QSize(24, 24))
        self.pushButtonPackUnlink.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonPackUnlink.setObjectName("pushButtonPackUnlink")
        self.horizontalLayoutPackBar.addWidget(self.pushButtonPackUnlink)

        self.pushButtonPackAdd=QtGui.QPushButton(self.centralwidget)
        self.pushButtonPackAdd.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonPackAdd.setObjectName("pushButtonPackAdd")
        self.horizontalLayoutPackBar.addWidget(self.pushButtonPackAdd)

        self.pushButtonPackDisable=QtGui.QPushButton(self.centralwidget)
        self.pushButtonPackDisable.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonPackDisable.setObjectName("pushButtonPackDisable")
        self.horizontalLayoutPackBar.addWidget(self.pushButtonPackDisable)
        self.pushButtonPackSettings=QtGui.QPushButton(self.centralwidget)
        self.pushButtonPackSettings.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonPackSettings.setObjectName("pushButtonPackSettings")
        self.horizontalLayoutPackBar.addWidget(self.pushButtonPackSettings)

        spacerItem=QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayoutPackBar.addItem(spacerItem)

        self.verticalLayoutPackShot.addLayout(self.horizontalLayoutPackBar)
        self.treeWidgetPack=QtGui.QTreeWidget(self.centralwidget)
        self.treeWidgetPack.setAlternatingRowColors(True)
        self.treeWidgetPack.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeWidgetPack.setRootIsDecorated(True)
        self.treeWidgetPack.setAnimated(True)
        self.treeWidgetPack.setObjectName("treeWidgetPack")
        item_0=QtGui.QTreeWidgetItem(self.treeWidgetPack)
        self.verticalLayoutPackShot.addWidget(self.treeWidgetPack)

        self.linePackShot=QtGui.QFrame(self.centralwidget)
        self.linePackShot.setFrameShape(QtGui.QFrame.HLine)
        self.linePackShot.setObjectName("linePackShot")
        self.verticalLayoutPackShot.addWidget(self.linePackShot)
        self.horizontalLayoutShotFilter=QtGui.QHBoxLayout()
        self.horizontalLayoutShotFilter.setObjectName("horizontalLayoutShotFilter")
        self.labelShotFilter=QtGui.QLabel(self.centralwidget)
        self.labelShotFilter.setObjectName("labelShotFilter")
        self.horizontalLayoutShotFilter.addWidget(self.labelShotFilter)

        self.lineEditShotFilter=QtGui.QLineEdit(self.centralwidget)
        self.lineEditShotFilter.setObjectName("lineEditShotFilter")
        self.horizontalLayoutShotFilter.addWidget(self.lineEditShotFilter)
        self.verticalLayoutPackShot.addLayout(self.horizontalLayoutShotFilter)

        self.horizontalLayoutShotBar=QtGui.QHBoxLayout()
        self.horizontalLayoutShotBar.setObjectName("horizontalLayoutShotBar")

        self.pushButtonShotLink=QtGui.QPushButton(self.centralwidget)
        self.pushButtonShotLink.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonShotLink.setObjectName("pushButtonShotLink")
        self.horizontalLayoutShotBar.addWidget(self.pushButtonShotLink)

        self.pushButtonShotUnlink=QtGui.QPushButton(self.centralwidget)
        self.pushButtonShotUnlink.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonShotUnlink.setObjectName("pushButtonShotUnlink")
        self.horizontalLayoutShotBar.addWidget(self.pushButtonShotUnlink)

        spacerItem1=QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayoutShotBar.addItem(spacerItem1)
        self.verticalLayoutPackShot.addLayout(self.horizontalLayoutShotBar)

        self.treeWidgetShot=QtGui.QTreeWidget(self.centralwidget)
        self.treeWidgetShot.setAlternatingRowColors(True)
        self.treeWidgetShot.setRootIsDecorated(True)
        self.treeWidgetShot.setAnimated(True)
        self.treeWidgetShot.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeWidgetShot.setObjectName("treeWidgetShot")
        item_0=QtGui.QTreeWidgetItem(self.treeWidgetShot)
        self.verticalLayoutPackShot.addWidget(self.treeWidgetShot)

        self.horizontalLayout.addLayout(self.verticalLayoutPackShot)
        self.verticalLayoutMain.addLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralwidget)

        self.statusbar=QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.lineEditAssetSearch, self.treeWidgetAsset)
        self.setTabOrder(self.treeWidgetAsset, self.lineEditPackFilter)
        self.setTabOrder(self.lineEditPackFilter, self.treeWidgetPack)
        self.setTabOrder(self.treeWidgetPack, self.treeWidgetShot)

    def retranslateUi(self):

        # Title
        self.setWindowTitle(QtGui.QApplication.translate("Breakdown", "Breakdown", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTitle.setText(QtGui.QApplication.translate("Breakdown", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Project</span><span style=\" font-size:12pt;\"/><span style=\" font-size:12pt; font-weight:600;\">:</span><span style=\" font-size:12pt;\"> %s</span></p></body></html>"%(self.project), None, QtGui.QApplication.UnicodeUTF8))

        self.labelAssetSearch.setText(QtGui.QApplication.translate("Breakdown", "searchAssets", None, QtGui.QApplication.UnicodeUTF8))

        icon=QtGui.QIcon(utils.getIconPath("refresh"))
        self.pushButtonAssetRefresh.setIcon(icon)


        self.treeWidgetAsset.setSortingEnabled(True)
        self.treeWidgetAsset.headerItem().setText(0, QtGui.QApplication.translate("Breakdown", "Assets", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled=self.treeWidgetAsset.isSortingEnabled()
        self.treeWidgetAsset.setSortingEnabled(False)
        self.treeWidgetAsset.topLevelItem(0).setText(0, QtGui.QApplication.translate("Breakdown", "asset", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetAsset.setSortingEnabled(__sortingEnabled)

        self.labelPackFilter.setText(QtGui.QApplication.translate("Breakdown", "searchPacks", None, QtGui.QApplication.UnicodeUTF8))

        icon=QtGui.QIcon(utils.getIconPath("link"))
        self.pushButtonPackLink.setIcon(icon)

        icon=QtGui.QIcon(utils.getIconPath("unlink"))
        self.pushButtonPackUnlink.setIcon(icon)

        icon=QtGui.QIcon(utils.getIconPath("add"))
        self.pushButtonPackAdd.setIcon(icon)

        icon=QtGui.QIcon(utils.getIconPath("subtract"))
        self.pushButtonPackDisable.setIcon(icon)

        icon=QtGui.QIcon(utils.getIconPath("settings"))
        self.pushButtonPackSettings.setIcon(icon)

        self.treeWidgetPack.setSortingEnabled(True)
        self.treeWidgetPack.headerItem().setText(0, QtGui.QApplication.translate("Breakdown", "Packs", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled=self.treeWidgetPack.isSortingEnabled()
        self.treeWidgetPack.setSortingEnabled(False)
        self.treeWidgetPack.topLevelItem(0).setText(0, QtGui.QApplication.translate("Breakdown", "pack", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetPack.setSortingEnabled(__sortingEnabled)

        self.labelShotFilter.setText(QtGui.QApplication.translate("Breakdown", "searchShots", None, QtGui.QApplication.UnicodeUTF8))

        icon=QtGui.QIcon(utils.getIconPath("link"))
        self.pushButtonShotLink.setIcon(icon)

        icon=QtGui.QIcon(utils.getIconPath("unlink"))
        self.pushButtonShotUnlink.setIcon(icon)

        self.treeWidgetShot.setSortingEnabled(True)
        self.treeWidgetShot.headerItem().setText(0, QtGui.QApplication.translate("Breakdown", "Shots", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled=self.treeWidgetShot.isSortingEnabled()
        self.treeWidgetShot.setSortingEnabled(False)
        self.treeWidgetShot.topLevelItem(0).setText(0, QtGui.QApplication.translate("Breakdown", "shot", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetShot.setSortingEnabled(__sortingEnabled)

def systemAM () :
    app=QtGui.QApplication (sys.argv)
    main=UiBreakDown()
    main.show()
    app.exec_()
    sys.exit()

if __name__=='__main__':
    systemAM()
