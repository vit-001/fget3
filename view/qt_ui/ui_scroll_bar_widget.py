# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/Repository/PyWork/fget3/view/qt_design/scroll_bar_widget.ui'
#
# Created: Thu Mar  9 00:24:56 2017
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ScrollBarWidget(object):
    def setupUi(self, ScrollBarWidget):
        ScrollBarWidget.setObjectName("ScrollBarWidget")
        ScrollBarWidget.resize(376, 657)
        self.main_layout = QtWidgets.QHBoxLayout(ScrollBarWidget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName("main_layout")
        self.area = QtWidgets.QFrame(ScrollBarWidget)
        self.area.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.area.setFrameShadow(QtWidgets.QFrame.Raised)
        self.area.setObjectName("area")
        self.area_layout = QtWidgets.QVBoxLayout(self.area)
        self.area_layout.setSpacing(0)
        self.area_layout.setContentsMargins(0, 0, 0, 0)
        self.area_layout.setObjectName("area_layout")
        self.main_layout.addWidget(self.area)
        self.scroll_bar = QtWidgets.QScrollBar(ScrollBarWidget)
        self.scroll_bar.setOrientation(QtCore.Qt.Vertical)
        self.scroll_bar.setObjectName("scroll_bar")
        self.main_layout.addWidget(self.scroll_bar)

        self.retranslateUi(ScrollBarWidget)
        QtCore.QMetaObject.connectSlotsByName(ScrollBarWidget)

    def retranslateUi(self, ScrollBarWidget):
        _translate = QtCore.QCoreApplication.translate
        ScrollBarWidget.setWindowTitle(_translate("ScrollBarWidget", "Form"))

