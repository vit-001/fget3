# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5.QtWidgets import QMainWindow

from view.qt_ui.thumb_widget import Ui_MainWindow
from view.widgets.thumb_widget import ThumbWidgetVS


from controller.controller import ControllerFromViewInterface

class MainWindow(QMainWindow):
    def __init__(self, parent=None, controller: ControllerFromViewInterface=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.controller=controller
        self.resize(454, 779)
        print(self.geometry())

    def closeEvent(self, *args, **kwargs):
        self.controller.on_exit()


if __name__ == "__main__":
    pass