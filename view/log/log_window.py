# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from interface.view_interface import ViewFromModelInterface
from interface.view_manager_interface import ViewManagerFromViewInterface

from view.full_view.full_view import FullView
from view.qt_ui.ui_log_view import Ui_LogView


class LogViewWindow(QWidget):
    def __init__(self, view_manager: ViewManagerFromViewInterface=None):
        QWidget.__init__(self, None)
        self.view_manager=view_manager

        # self.log_text=''

        # create interface
        self.ui = Ui_LogView()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.Tool)

    def out_text(self, text:str):
        # self.log_text+=text
        self.ui.text.append(text)

if __name__ == "__main__":
    pass