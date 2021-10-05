# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

# from PyQt5 import Qt

from PyQt6.QtCore import QTimer, QEventLoop, Qt, QRect, qVersion
from PyQt6.QtGui import QGuiApplication, QKeySequence, QAction
from PyQt6.QtWidgets import QApplication, QMenu

from common.setting import Setting
from common.util import get_menu_handler

from data_format.url import URL

from interface.view_manager_interface import ViewManagerFromModelInterface, ViewManagerFromControllerInterface, \
    ViewManagerFromViewInterface
from interface.controller_interface import ControllerFromViewInterface
from interface.hystory_interface import HistoryFromViewInterface
from interface.view_interface import FullViewFromModelInterface,ThumbViewFromModelInterface
from interface.log_interface import LogViewInterface

from view_qt6.full_view.full_view_window import FullViewWindow
from view_qt6.thumb_view.main_window import MainWindow

from view_qt6.widgets.button_line import ImageButton


class ViewManager(ViewManagerFromControllerInterface, ViewManagerFromModelInterface, ViewManagerFromViewInterface):
    def __init__(self):
        print('PyQt version: ' + qVersion())

    def create_main_window(self, controller: ControllerFromViewInterface):
        self.controller = controller



        self.main = MainWindow(self)
        self.main.show()

        self.full = FullViewWindow(self)
        # self.full.show()

        # self.log=LogViewWindow(self)
        # self.log.show()
        self.log=self.main.get_log()

        self.configure_viewports()

        self.add_keyboard_shortcut(self.main, 'Ctrl+`', self.panic)

        self.timer = QTimer()
        self.timer.timeout.connect(self.controller.on_cycle_handler)
        self.timer.start(100)

    def configure_viewports(self):
        # desktop = QApplication.desktop().screenGeometry()
        desktop=QApplication.primaryScreen()
        # print(desktop.size().)
        main_x_base = Setting.main_window_x0_in_percents * desktop.size().width() // 100
        main_y_base = Setting.main_window_y0_in_percents * desktop.size().height() // 100
        main_h = Setting.main_window_h_in_percents * desktop.size().height() // 100

        self.main.setGeometry(QRect(main_x_base, main_y_base, Setting.main_window_w_in_pixels, main_h))

        full_x_base = main_x_base + Setting.main_window_w_in_pixels + (Setting.full_window_w_gap_in_percents +
                      Setting.full_window_x1_in_percents) * desktop.size().width() // 100
        full_y_base = Setting.full_window_y0_in_percents * desktop.size().height() // 100
        full_w = desktop.size().width() - full_x_base - Setting.full_window_x1_in_percents * desktop.size().width() // 100
        full_h = Setting.full_window_h_in_percents * desktop.size().height() // 100

        self.full.setGeometry(QRect(full_x_base, full_y_base, full_w, full_h))

        # log_x_base = main_x_base + Setting.main_window_w_in_pixels + (Setting.log_window_w_gap_in_percents +
        #               Setting.log_window_x1_in_percents) * desktop.width() // 100
        # log_y_base = Setting.log_window_y0_in_percents * desktop.height() // 100
        # log_w = desktop.width() - log_x_base - Setting.log_window_x1_in_percents * desktop.width() // 100
        # log_h = Setting.log_window_h_in_percents * desktop.height() // 100
        #
        # self.log.setGeometry(QRect(log_x_base, log_y_base, log_w, log_h))


        # self.main.resize(458, 779)

    def add_keyboard_shortcut(self, window, shortcut='', on_pressed=lambda: None):
        action = QAction(window)
        action.setShortcut(QKeySequence(shortcut))
        action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        window.addAction(action)
        action.triggered.connect(on_pressed)

    def add_start_button(self, picture_filename: str, url: URL, menu_items:dict=None, name:str=None):
        if not name:
            name=url.domain()
        b = ImageButton(picture_filename, name, lambda: self.goto_url(url))

        menu=self.create_button_menu(self.main,menu_items)
        if menu:
            b.setMenu(menu)
        self.main.create_site_button(b)

    def create_button_menu(self, parent, menu_items:dict)->QMenu:
        # return
        if menu_items:
            menu = QMenu(parent)
            for key in sorted(menu_items.keys()):
                menu_action = QAction(key, parent, triggered=get_menu_handler(self.goto_url,menu_items[key]))
                menu.addAction(menu_action)
            return menu
        else:
            return None

    def on_thumb_history_changed(self, history: HistoryFromViewInterface):
        self.main.on_history_changed(history)

    def new_thumb_view(self) -> ThumbViewFromModelInterface:
        # print('new_thumb_view****************')
        view=self.main.get_new_thumb_view()

        QEventLoop().processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
        self.main.update()

        return view

    def new_full_view(self)->FullViewFromModelInterface:
        view=self.full.get_new_full_view()
        QEventLoop().processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
        self.full.update()

        return view

    def set_tab_text(self, view, text:str, tooltip:str=''):
        self.main.set_tab_text(view,text, tooltip)
        self.full.set_tab_text(view,text, tooltip)

    def get_log(self) -> LogViewInterface:
        return self.log

    def on_thumb_tab_url_changed(self, view):
        self.main.on_url_in_tab_changed(view)

    def goto_url(self, url: URL, flags=None):
        if flags is None:
            flags=dict()

        if QGuiApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier:
            # print('control')
            self.controller.goto_url(url, flags=flags)
        else:
            self.controller.goto_url(url,
                                     current_thumb_view=self.main.get_current_thumb_view(),
                                     current_full_view=self.full.get_current_full_view(),
                                     flags=flags
                                     )

    def refresh_thumb_view(self):
        view = self.main.get_current_thumb_view()
        if view:
            url = view.url
            self.goto_url(url)

    def add_to_favorite(self):
        view=self.main.get_current_thumb_view()
        if view:
            url=view.url
            self.controller.favorite_add(url)
            self.goto_url(url)

    def is_full_view_tab_active(self, full_view: FullViewFromModelInterface) -> bool:
        return self.full.is_tab_active(full_view)

    def panic(self):
        print('Panic!!')
        self.main.panic()
        self.full.panic()

    def on_exit(self):
        self.full.on_exit()
        self.controller.on_exit()
        QGuiApplication.exit(0)


if __name__ == "__main__":
    pass
