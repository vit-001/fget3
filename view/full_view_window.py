# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QBrush,QColor,QPalette

from common.url import URL

from view.qt_ui.full_view_window import Ui_FullViewWindow
from view.widgets.thumb_widget import ThumbWidgetVS
from view.widgets.button_line import ButtonLine,TextButton,ImageButton


from controller.controller import ControllerFromViewInterface

class FullViewWindow(QWidget):
    def __init__(self, controller: ControllerFromViewInterface=None):
        QWidget.__init__(self, None)
        self.ui = Ui_FullViewWindow()
        self.ui.setupUi(self)
        self.controller=controller
        # self.resize(458, 779)
        print(self.geometry())
        self.create_widgets()

    def create_widgets(self):
        pass


if __name__ == "__main__":
    pass