# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QBrush,QColor,QPalette

from common.url import URL

from view.base_view import ViewManagerFromViewInterface
from view.qt_ui.ui_main_window import Ui_MainWindow
from view.widgets.thumb_widget import ThumbWidgetVS
from view.widgets.button_line import ButtonLine,TextButton,ImageButton
from view.thumb_view import ThumbView



from controller.controller import ControllerFromViewInterface

class MainWindow(QMainWindow):
    def __init__(self, view_manager: ViewManagerFromViewInterface=None):
        QMainWindow.__init__(self, None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.view_manager=view_manager
        self.create_widgets()

        self.thumb_views = list()

        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

    def create_widgets(self):
        self.sites=ButtonLine(self.ui.top_frame,height=50)
        self.ui.top_frame_layout.addWidget(self.sites)

    def get_new_thumb_view(self, name: str) -> ThumbView:
        tab = self.ui.tabWidget
        view = ThumbView(tab, name, self.view_manager)
        self.thumb_views.append(view)

        return view

    def get_current_thumb_view(self)->ThumbView:
        index = self.ui.tabWidget.currentIndex()
        if index >= 0:
            return self.thumb_views[index]
        else:
            return None

    def create_site_button(self,button):
        self.sites.add_button(button)

    def close_tab(self,index:int):
        self.thumb_views[index].clear()
        self.thumb_views.pop(index)
        self.ui.tabWidget.removeTab(index)
        self.update()

    def closeEvent(self, *args, **kwargs):
        self.view_manager.on_exit()

if __name__ == "__main__":
    pass