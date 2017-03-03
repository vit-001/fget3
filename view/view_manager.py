# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

# from PyQt5 import Qt

from PyQt5.QtCore import QTimer, QEventLoop, Qt, QRect
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication

from common.setting import Setting
from common.url import URL
from controller.base_controller import ControllerFromViewInterface
from view.base_view import ThumbViewFromModelInterface
from view.base_view import ViewManagerFromModelInterface, ViewManagerFromControllerInterface, \
    ViewManagerFromViewInterface, FullViewFromModelInterface
from view.full_view_window import FullViewWindow
from view.main_window import MainWindow
from view.thumb_view import ThumbView
from view.widgets.button_line import ImageButton


class ViewManager(ViewManagerFromControllerInterface, ViewManagerFromModelInterface, ViewManagerFromViewInterface):
    def create_main_window(self, controller: ControllerFromViewInterface):
        self.controller = controller

        self.main = MainWindow(self)
        self.main.show()

        self.full = FullViewWindow(self)
        self.full.show()

        self.configure_viewports()



        self.timer = QTimer()
        self.timer.timeout.connect(self.controller.on_cycle_handler)
        self.timer.start(100)

    def configure_viewports(self):
        desktop = QApplication.desktop().screenGeometry()
        print(desktop)
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

    def add_start_button(self, name: str, picture_filename: str, url: URL):
        b = ImageButton(picture_filename, name, lambda: self.goto_url(url))
        self.main.create_site_button(b)

    def prepare_thumb_view(self, name: str) -> ThumbViewFromModelInterface:
        view=self.main.get_new_thumb_view(name)

        QEventLoop().processEvents(QEventLoop.AllEvents)
        self.main.update()

        return view

    def prepare_full_view(self, name:str)->FullViewFromModelInterface:
        view=self.full.get_new_full_view(name)
        QEventLoop().processEvents(QEventLoop.AllEvents)
        self.full.update()

        return view

    def goto_url(self, url: URL):

        if QGuiApplication.keyboardModifiers() == Qt.ControlModifier:
            # print('control')
            self.controller.goto_url(url)
        else:
            self.controller.goto_url(url,
                                     current_thumb_view=self.main.get_current_thumb_view(),
                                     current_full_view=self.full.get_current_full_view()
                                     )

    def on_exit(self):
        self.controller.on_exit()
        QGuiApplication.exit(0)


if __name__ == "__main__":
    pass
