# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5.QtWidgets import QMainWindow

from view.qt_ui.thumb_view import Ui_MainWindow
from controller.controller import ControllerFromViewInterface

class MainWindow(QMainWindow):
    def __init__(self, parent=None, controller: ControllerFromViewInterface=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.controller=controller

    def closeEvent(self, *args, **kwargs):
        self.controller.on_exit()


if __name__ == "__main__":
    pass