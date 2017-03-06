# -*- coding: utf-8 -*-
__author__ = 'Vit'
import os
from PyQt5.QtWidgets import QWidget

from view.qt_ui.ui_history_view import Ui_HistoryView

class HistoryView(QWidget):
    def __init__(self, parent:QWidget=None):
        super().__init__(parent)
        self.ui=Ui_HistoryView()
        savecwd = os.getcwd()
        os.chdir('view/qt_ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)



if __name__ == "__main__":
    pass