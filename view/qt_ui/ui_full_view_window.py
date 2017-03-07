# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/Repository/PyWork/fget3/view/qt_design/full_view_window.ui'
#
# Created: Tue Mar  7 22:10:29 2017
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FullViewWindow(object):
    def setupUi(self, FullViewWindow):
        FullViewWindow.setObjectName("FullViewWindow")
        FullViewWindow.resize(688, 572)
        self.verticalLayout = QtWidgets.QVBoxLayout(FullViewWindow)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(2, 4, 2, 4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(FullViewWindow)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(FullViewWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(FullViewWindow)

    def retranslateUi(self, FullViewWindow):
        _translate = QtCore.QCoreApplication.translate
        FullViewWindow.setWindowTitle(_translate("FullViewWindow", "Form"))

