# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/Repository/PyWork/fget3/view/qt_design/history_view.ui'
#
# Created: Mon Mar 20 12:09:24 2017
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HistoryView(object):
    def setupUi(self, HistoryView):
        HistoryView.setObjectName("HistoryView")
        HistoryView.resize(616, 56)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HistoryView.sizePolicy().hasHeightForWidth())
        HistoryView.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(HistoryView)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bn_back = QtWidgets.QToolButton(HistoryView)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../resource/icons/ic_backspace_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bn_back.setIcon(icon)
        self.bn_back.setIconSize(QtCore.QSize(32, 32))
        self.bn_back.setAutoRaise(True)
        self.bn_back.setObjectName("bn_back")
        self.horizontalLayout.addWidget(self.bn_back)
        self.combo_history = QtWidgets.QComboBox(HistoryView)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_history.sizePolicy().hasHeightForWidth())
        self.combo_history.setSizePolicy(sizePolicy)
        self.combo_history.setEditable(True)
        self.combo_history.setCurrentText("")
        self.combo_history.setMaxVisibleItems(30)
        self.combo_history.setDuplicatesEnabled(True)
        self.combo_history.setObjectName("combo_history")
        self.horizontalLayout.addWidget(self.combo_history)
        self.bn_go = QtWidgets.QToolButton(HistoryView)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../resource/icons/ic_forward_white_48dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bn_go.setIcon(icon1)
        self.bn_go.setIconSize(QtCore.QSize(32, 32))
        self.bn_go.setAutoRaise(True)
        self.bn_go.setObjectName("bn_go")
        self.horizontalLayout.addWidget(self.bn_go)

        self.retranslateUi(HistoryView)
        QtCore.QMetaObject.connectSlotsByName(HistoryView)

    def retranslateUi(self, HistoryView):
        _translate = QtCore.QCoreApplication.translate
        HistoryView.setWindowTitle(_translate("HistoryView", "Form"))
        self.bn_back.setText(_translate("HistoryView", "..."))
        self.bn_go.setText(_translate("HistoryView", "..."))

