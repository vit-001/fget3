# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/repo/fget3/view_qt5/qt_design/log_view.ui'
#
# Created: Thu Jul 20 16:45:56 2017
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
        self.text = QtWidgets.QTextBrowser(LogView)
        self.text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.text.setReadOnly(True)
        self.text.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.text.setOpenExternalLinks(True)
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)

        self.retranslateUi(LogView)
        QtCore.QMetaObject.connectSlotsByName(LogView)

    def retranslateUi(self, LogView):
        _translate = QtCore.QCoreApplication.translate
        LogView.setWindowTitle(_translate("LogView", "Form"))

