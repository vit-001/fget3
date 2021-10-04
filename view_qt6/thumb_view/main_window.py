# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
import os

from PyQt6.QtWidgets import QMainWindow, QToolButton,QSizePolicy
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt

from data_format.url import URL

from interface.hystory_interface import HistoryFromViewInterface
from interface.view_manager_interface import ViewManagerFromViewInterface
from interface.log_interface import LogViewInterface

from view_qt6.log.log_window import LogViewWindow
from view_qt6.history_view.history_view import HistoryView
from view_qt6.thumb_view.thumb_view import ThumbView
from view_qt6.widgets.button_line import ButtonLine

from view_qt6.qt_ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, view_manager: ViewManagerFromViewInterface=None):
        QMainWindow.__init__(self, None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.view_manager=view_manager
        self.create_widgets()

        pixmap = QPixmap('view_qt5/resource/icons_my/icon.png')
        icon = QIcon()
        icon.addPixmap(pixmap, QIcon.Mode.Normal, QIcon.State.Off)

        self.setWindowTitle('P Browser - thumbnail view_qt5')
        self.setWindowIcon(icon)

        self.thumb_views = list()

        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.tabWidget.currentChanged.connect(self.on_current_tab_changed)
        self.bn_favorite.clicked.connect(self.view_manager.add_to_favorite)
        self.log_button.toggled.connect(self.log_button_toggle)

    def create_widgets(self):
        self.sites=ButtonLine(self.ui.top_frame,height=50, speed=90, space=5)
        self.ui.top_frame_layout.addWidget(self.sites)

        self.history=HistoryView(self, self.view_manager)
        self.ui.controls_frame_layout.addWidget(self.history)

        self.bn_favorite = QToolButton(self.ui.controls_frame)
        self.bn_favorite.setAutoRaise(True)
        icon = QIcon()
        icon.addPixmap(QPixmap("view_qt5/resource/icons/ic_add_box_white_48dp.png"), QIcon.Mode.Normal, QIcon.State.Off)
        self.bn_favorite.setIcon(icon)
        self.bn_favorite.setIconSize(QSize(32, 32))
        self.ui.controls_frame_layout.addWidget(self.bn_favorite)

        self.log_button = QToolButton()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Ignored)
        self.log_button.setSizePolicy(sizePolicy)
        self.log_button.setMinimumSize(QSize(0, 10))
        icon = QIcon()
        icon.addPixmap(QPixmap("view_qt5/resource/icons/ic_arrow_drop_up_white_24dp.png"), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addPixmap(QPixmap("view_qt5/resource/icons/ic_arrow_drop_down_white_24dp.png"), QIcon.Mode.Normal, QIcon.State.On)
        self.log_button.setIcon(icon)
        self.log_button.setIconSize(QSize(24, 24))
        self.log_button.setCheckable(True)
        self.log_button.setAutoRaise(True)
        self.ui.bottom_frame_layout.addWidget(self.log_button)

        self.log=LogViewWindow(self.view_manager)
        self.ui.bottom_frame_layout.addWidget(self.log)
        self.log.setMaximumHeight(70)
        self.log.hide()

        # self.updateGeometry()

    def log_button_toggle(self):
        # return
        if self.log_button.isChecked():
            self.log.show()
        else:
            self.log.hide()

    def get_new_thumb_view(self) -> ThumbView:
        # print('New tv')
        tab = self.ui.tabWidget
        view = ThumbView(tab, self.view_manager)
        self.thumb_views.append(view)
        # print('New tv Ok')
        return view

    def get_current_thumb_view(self)->ThumbView:
        index = self.ui.tabWidget.currentIndex()
        if index >= 0:
            return self.thumb_views[index]
        else:
            return None

    def get_log(self)->LogViewInterface:
        return self.log

    def set_tab_text(self, view,text:str, tooltip=''):
        try:
            index=self.thumb_views.index(view)
            self.ui.tabWidget.setTabText(index,text)
            self.ui.tabWidget.setTabToolTip(index,tooltip)
        except ValueError:
            pass

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
            # print(view_qt5.url.get())
            self.history.set_current_url(view.url)

    def closeEvent(self, *args, **kwargs):
        for thumbs in self.thumb_views:
            thumbs.history_event()
        self.view_manager.on_exit()

if __name__ == "__main__":
    pass