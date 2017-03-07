# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5.QtWidgets import QMainWindow

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

        self.thumb_views = list()

        self.ui.tabWidget.tabCloseRequested.connect(self.on_close_tab)
        self.ui.tabWidget.currentChanged.connect(self.on_current_tab_changed)

    def create_widgets(self):
        self.sites=ButtonLine(self.ui.top_frame,height=50, speed=90, space=5)
        self.ui.top_frame_layout.addWidget(self.sites)

        self.history=HistoryView(self, self.view_manager)
        self.ui.controls_frame_layout.addWidget(self.history)

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

    def create_site_button(self,button):
        self.sites.add_button(button)

    def on_close_tab(self, index:int):
        # self.thumb_views[index].history_event()
        self.thumb_views[index].re_init(dict())
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
            print(view.url.get())
            self.history.set_current_url(view.url)

    def closeEvent(self, *args, **kwargs):
        for thumbs in self.thumb_views:
            thumbs.history_event()
        self.view_manager.on_exit()

if __name__ == "__main__":
    pass