# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5.QtWidgets import QMainWindow, QToolButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

from data_format.url import URL

from interface.hystory_interface import HistoryFromViewInterface
from interface.view_manager_interface import ViewManagerFromViewInterface

from view.history_view.history_view import HistoryView
from view.thumb_view.thumb_view import ThumbView
from view.widgets.button_line import ButtonLine

from view.qt_ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, view_manager: ViewManagerFromViewInterface=None):
        QMainWindow.__init__(self, None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.view_manager=view_manager
        self.create_widgets()

        pixmap = QPixmap('view/resource/icons_my/icon.png')
        icon = QIcon()
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)

        self.setWindowTitle('P Browser - thumbnail view')
        self.setWindowIcon(icon)

        self.thumb_views = list()

        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.tabWidget.currentChanged.connect(self.on_current_tab_changed)
        self.bn_favorite.clicked.connect(self.view_manager.add_to_favorite)

    def create_widgets(self):
        self.sites=ButtonLine(self.ui.top_frame,height=50, speed=90, space=5)
        self.ui.top_frame_layout.addWidget(self.sites)

        self.history=HistoryView(self, self.view_manager)
        self.ui.controls_frame_layout.addWidget(self.history)

        self.bn_favorite = QToolButton(self.ui.controls_frame)
        self.bn_favorite.setAutoRaise(True)
        icon = QIcon()
        icon.addPixmap(QPixmap("view/resource/icons/ic_add_box_white_48dp.png"), QIcon.Normal, QIcon.Off)
        self.bn_favorite.setIcon(icon)
        self.bn_favorite.setIconSize(QSize(32, 32))
        self.bn_favorite.setObjectName("bn_favorite")
        self.ui.controls_frame_layout.addWidget(self.bn_favorite)

    def get_new_thumb_view(self) -> ThumbView:
        tab = self.ui.tabWidget
        view = ThumbView(tab, self.view_manager)
        self.thumb_views.append(view)

        return view

    def get_current_thumb_view(self)->ThumbView:
        index = self.ui.tabWidget.currentIndex()
        if index >= 0:
            return self.thumb_views[index]
        else:
            return None

    def set_tab_text(self, view,text:str, tooltip=''):
        try:
            index=self.thumb_views.index(view)
            self.ui.tabWidget.setTabText(index,text)
            self.ui.tabWidget.setTabToolTip(index,tooltip)
        except ValueError:
            pass

    def show_status(self, text:str):
        self.ui.statusbar.showMessage(text,5000)

    def create_site_button(self,button):
        self.sites.add_button(button)

    def close_tab(self, index:int):
        # self.thumb_views[index].history_event()
        self.thumb_views[index].prepare_to_close()
        self.thumb_views.pop(index)
        self.ui.tabWidget.removeTab(index)
        self.update()

    def panic(self):
        self.showMinimized()

    def on_history_changed(self, history:HistoryFromViewInterface):
        self.history.update_history(history)

    def on_current_tab_changed(self, index:int):
        if index>=0 and len(self.thumb_views)>0:
            self.history.set_current_url(self.thumb_views[index].url)
        else:
            self.history.set_current_url(URL())

    def on_url_in_tab_changed(self, view):
        if self.thumb_views[self.ui.tabWidget.currentIndex()] == view:
            # print(view.url.get())
            self.history.set_current_url(view.url)

    def closeEvent(self, *args, **kwargs):
        for thumbs in self.thumb_views:
            thumbs.history_event()
        self.view_manager.on_exit()

if __name__ == "__main__":
    pass