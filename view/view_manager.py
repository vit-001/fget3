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


class ViewManager(ViewFromControllerInterface, ViewFromModelInterface):
    def __init__(self):
        pass

    def register_controller(self, controller:ControllerFromViewInterface):
        self.controller=controller

        self.main=MainWindow(controller=controller)
        self.main.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.controller.on_cycle_handler)
        self.timer.start(100)

    def prepare_thumb_view(self, new=False) -> ThumbViewFromModelInterface:
        return ThumbViewFromModelInterface()

    def on_exit(self):
        QGuiApplication.exit(0)


if __name__ == "__main__":
    pass