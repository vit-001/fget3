# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QSizePolicy
from PyQt5.QtGui import QBrush,QColor,QPalette

from common.url import URL

from view.qt_ui.ui_full_view_window import Ui_FullViewWindow
from view.widgets.thumb_widget import ThumbWidgetVS
from view.widgets.button_line import ButtonLine,TextButton,ImageButton
from view.widgets.video_player_widget import VideoPlayerWidget
from view.full_view import FullView

from controller.controller import ControllerFromViewInterface
from view.base_view import ViewManagerFromViewInterface

class FullViewWindow(QWidget):
    def __init__(self, view_manager: ViewManagerFromViewInterface=None):
        QWidget.__init__(self, None)
        self.view_manager=view_manager

        self.ui = Ui_FullViewWindow()
        self.ui.setupUi(self)

        self.create_widgets()

        self.full_views=list()

        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.tabWidget.currentChanged.connect(self.change_tab)


    def create_widgets(self):
        pass
        # self.video_widget=VideoPlayerWidget(self.ui.tab)
        # self.ui.tab_layout.addWidget(self.video_widget)
        # self.video_widget.show()
        #
        # sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.video_widget.sizePolicy().hasHeightForWidth())
        # self.video_widget.setSizePolicy(sizePolicy)

    def get_new_full_view(self, name: str) -> FullView:
        tab = self.ui.tabWidget
        view = FullView(tab, name, self.view_manager)
        self.full_views.append(view)

        return view

    def get_current_full_view(self)->FullView:
        index = self.ui.tabWidget.currentIndex()
        if index >= 0:
            return self.full_views[index]
        else:
            return None

    def close_tab(self,index:int):
        self.full_views.pop(index)
        self.ui.tabWidget.removeTab(index)
        self.update()

    def change_tab(self,index:int):
        print('change tab', index)
        for view in self.full_views:
            view.pause()
        if index>=0:
            self.full_views[index].resume()

if __name__ == "__main__":
    pass