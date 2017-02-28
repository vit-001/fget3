# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from PyQt5.QtCore import QTimer

from view.main_window import MainWindow
from view.base_view import ViewFromModelInterface, ViewFromControllerInterface
from view.base_view import ThumbViewFromModelInterface
from view.base_view import VideoViewFromModelInterface
from view.base_view import PictureViewFromModelInterface
from controller.base_controller import ControllerFromViewInterface


class ViewManager(ViewFromControllerInterface, ViewFromModelInterface):
    def __init__(self):
        self.main=MainWindow()
        self.main.show()

    def register_controller(self, controller:ControllerFromViewInterface):
        self.controller=controller
        self.timer = QTimer()
        self.timer.timeout.connect(self.controller.on_cycle_handler)
        self.timer.start(100)

    def prepare_thumb_view(self, new=False) -> ThumbViewFromModelInterface:
        return ThumbViewFromModelInterface()


if __name__ == "__main__":
    pass