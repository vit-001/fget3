# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from data_format.url import URL

from interface.view_interface import ViewFromModelInterface
from interface.view_manager_interface import ViewManagerFromViewInterface
from interface.log_interface import LogViewInterface

from view.full_view.full_view import FullView
from view.qt_ui.ui_log_view import Ui_LogView


class LogViewWindow(QWidget, LogViewInterface):
    def __init__(self, view_manager: ViewManagerFromViewInterface=None):
        QWidget.__init__(self, None)
        self.view_manager=view_manager

        self.ui = Ui_LogView()
        self.ui.setupUi(self)

        # self.ui.text.setAcceptRichText(False)

        # self.setWindowFlags(Qt.Tool)

    def write(self, *data, **options):
        # self.log_text+=text
        # self.ui.text.append(text)
        sep=options.get('sep',' ')
        text=''
        for item in data:
            if isinstance(item, URL):
                text += item.link()+sep
            else:
                text +=str(item)+sep
        self.ui.text.append(text.rstrip(sep))

if __name__ == "__main__":
    pass