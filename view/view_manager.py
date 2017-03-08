# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

# from PyQt5 import Qt

from PyQt5.QtCore import QTimer, QEventLoop, Qt, QRect
from PyQt5.QtGui import QGuiApplication, QKeySequence
from PyQt5.QtWidgets import QApplication, QAction, QMenu

from common.setting import Setting
from common.util import get_menu_handler

from data_format.url import URL

from interface.view_manager_interface import ViewManagerFromModelInterface, ViewManagerFromControllerInterface, \
    ViewManagerFromViewInterface
from interface.controller_interface import ControllerFromViewInterface
from interface.hystory_interface import HistoryFromViewInterface
from interface.view_interface import FullViewFromModelInterface,ThumbViewFromModelInterface

from view.full_view.full_view_window import FullViewWindow
from view.thumb_view.main_window import MainWindow

from view.widgets.button_line import ImageButton


class ViewManager(ViewManagerFromControllerInterface, ViewManagerFromModelInterface, ViewManagerFromViewInterface):
    def create_main_window(self, controller: ControllerFromViewInterface):
        self.controller = controller

        self.main = MainWindow(self)
        self.main.show()

        self.full = FullViewWindow(self)
        self.full.show()

        self.configure_viewports()

        self.add_keyboard_shortcut(self.main, 'Ctrl+`', self.panic)

        self.timer = QTimer()
        self.timer.timeout.connect(self.controller.on_cycle_handler)
        self.timer.start(100)

    def configure_viewports(self):
        desktop = QApplication.desktop().screenGeometry()
        main_x_base = Setting.main_window_x0_in_percents * desktop.width() // 100
        main_y_base = Setting.main_window_y0_in_percents * desktop.height() // 100
        main_h = Setting.main_window_h_in_percents * desktop.height() // 100

        self.main.setGeometry(QRect(main_x_base, main_y_base, Setting.main_window_w_in_pixels, main_h))

        full_x_base = main_x_base + Setting.main_window_w_in_pixels + (Setting.full_window_w_gap_in_percents +
                      Setting.full_window_x1_in_percents) * desktop.width() // 100
        full_y_base = Setting.full_window_y0_in_percents * desktop.height() // 100
        full_w = desktop.width() - full_x_base - Setting.full_window_x1_in_percents * desktop.width() // 100
        full_h = Setting.full_window_h_in_percents * desktop.height() // 100

        self.full.setGeometry(QRect(full_x_base, full_y_base, full_w, full_h))


        # self.main.resize(458, 779)

    def add_keyboard_shortcut(self, window, shortcut='', on_pressed=lambda: None):
        action = QAction(window)
        action.setShortcut(QKeySequence(shortcut))
        action.setShortcutContext(Qt.ApplicationShortcut)
        window.addAction(action)
        action.triggered.connect(on_pressed)

    def add_start_button(self, name: str, picture_filename: str, url: URL, menu_items:dict=None):
        b = ImageButton(picture_filename, name, lambda: self.goto_url(url))

        menu=self.create_button_menu(self.main,menu_items)
        if menu:
            b.setMenu(menu)
        self.main.create_site_button(b)

    def create_button_menu(self, parent, menu_items:dict)->QMenu:
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

    def prepare_thumb_view(self, flags) -> ThumbViewFromModelInterface:
        view=self.main.get_new_thumb_view(flags)

        QEventLoop().processEvents(QEventLoop.AllEvents)
        self.main.update()

        return view

    def prepare_full_view(self, flags)->FullViewFromModelInterface:
        view=self.full.get_new_full_view(flags)
        QEventLoop().processEvents(QEventLoop.AllEvents)
        self.full.update()

        return view

    def set_tab_text(self, view, text:str, tooltip:str=''):
        self.main.set_tab_text(view,text, tooltip)
        self.full.set_tab_text(view,text, tooltip)

    def on_thumb_tab_url_changed(self, view):
        self.main.on_url_in_tab_changed(view)

    def goto_url(self, url: URL, flags=None):

        if flags is None:
            flags=dict()

        if QGuiApplication.keyboardModifiers() == Qt.ControlModifier:
            # print('control')
            self.controller.goto_url(url, flags=flags)
        else:
            self.controller.goto_url(url,
                                     current_thumb_view=self.main.get_current_thumb_view(),
                                     current_full_view=self.full.get_current_full_view(),
                                     flags=flags
                                     )

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
