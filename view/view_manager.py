# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from view.main_window import MainWindow
from view.base_view import AbstractViewFromModelInterface, AbsractViewFromControllerInterface

class ViewManager(AbsractViewFromControllerInterface,AbstractViewFromModelInterface):
    def __init__(self):
        self.main=MainWindow()
        self.main.show()

if __name__ == "__main__":
    pass