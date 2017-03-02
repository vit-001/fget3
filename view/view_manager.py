# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QGuiApplication

from view.main_window import MainWindow
from view.base_view import ViewFromModelInterface, ViewFromControllerInterface
from view.base_view import ThumbViewFromModelInterface
from view.base_view import VideoViewFromModelInterface
from view.base_view import PictureViewFromModelInterface
from controller.base_controller import ControllerFromViewInterface

from view.thumb_view import ThumbView

class ViewManager(ViewFromControllerInterface, ViewFromModelInterface):

    def create_main_window(self, controller:ControllerFromViewInterface):
        self.controller=controller

        self.main=MainWindow(controller=controller)
        self.main.show()

        self.thumb_views=list()

        self.timer = QTimer()
        self.timer.timeout.connect(self.controller.on_cycle_handler)
        self.timer.start(100)

    def prepare_thumb_view(self, name:str, new=False) -> ThumbViewFromModelInterface:
        tab=self.main.ui.tabWidget
        view=ThumbView(tab, name)
        self.thumb_views.append(view)
        return view

    def on_exit(self):
        QGuiApplication.exit(0)


if __name__ == "__main__":
    pass