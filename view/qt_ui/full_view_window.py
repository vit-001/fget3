# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/repo/fget3/view/qt_design/full_view_window.ui'
#
# Created: Fri Mar  3 18:07:15 2017
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FullViewWindow(object):
    def setupUi(self, FullViewWindow):
        FullViewWindow.setObjectName("FullViewWindow")
        FullViewWindow.resize(688, 572)
        self.verticalLayout = QtWidgets.QVBoxLayout(FullViewWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(FullViewWindow)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(FullViewWindow)
        QtCore.QMetaObject.connectSlotsByName(FullViewWindow)

    def retranslateUi(self, FullViewWindow):
        _translate = QtCore.QCoreApplication.translate
        FullViewWindow.setWindowTitle(_translate("FullViewWindow", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("FullViewWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("FullViewWindow", "Tab 2"))

