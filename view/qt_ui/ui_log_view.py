# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/repo/fget3/view/qt_design/log_view.ui'
#
# Created: Thu Mar 23 18:43:06 2017
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogView(object):
    def setupUi(self, LogView):
        LogView.setObjectName("LogView")
        LogView.resize(722, 442)
        self.verticalLayout = QtWidgets.QVBoxLayout(LogView)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text = QtWidgets.QTextEdit(LogView)
        self.text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text.setReadOnly(True)
        self.text.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)

        self.retranslateUi(LogView)
        QtCore.QMetaObject.connectSlotsByName(LogView)

    def retranslateUi(self, LogView):
        _translate = QtCore.QCoreApplication.translate
        LogView.setWindowTitle(_translate("LogView", "Form"))

