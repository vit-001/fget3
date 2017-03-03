# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from PyQt5.QtCore import QTimer, QEventLoop
from PyQt5.QtGui import QGuiApplication

from common.url import URL

from view.main_window import MainWindow
from view.base_view import ViewManagerFromModelInterface, ViewManagerFromControllerInterface, ViewManagerFromViewInterface
from view.base_view import ThumbViewFromModelInterface
from view.base_view import VideoViewFromModelInterface
from view.base_view import PictureViewFromModelInterface
from controller.base_controller import ControllerFromViewInterface

from view.thumb_view import ThumbView

class ViewManager(ViewManagerFromControllerInterface, ViewManagerFromModelInterface,ViewManagerFromViewInterface):

    def create_main_window(self, controller:ControllerFromViewInterface):
        self.controller=controller

        self.main=MainWindow(controller=controller)
        self.main.show()

        self.thumb_views=list()

        self.timer = QTimer()
        self.timer.timeout.connect(self.controller.on_cycle_handler)
        self.timer.start(200)

    def prepare_thumb_view(self, name:str, new=False) -> ThumbViewFromModelInterface:
        tab=self.main.ui.tabWidget
        view=ThumbView(tab, name, self)
        self.thumb_views.append(view)

        QEventLoop().processEvents(QEventLoop.AllEvents)
        self.main.update()

        return view

    def goto_url(self,url:URL):
        self.controller.goto_url(url)

    def on_exit(self):
        QGuiApplication.exit(0)


if __name__ == "__main__":
    pass