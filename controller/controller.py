# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL

from controller.base_controller import ControllerFromModelInterface,ControllerFromViewInterface
from view.base_view import ViewManagerFromControllerInterface
from model.base_model import ModelFromControllerInterface

class Controller(ControllerFromModelInterface,ControllerFromViewInterface):
    def __init__(self, view:ViewManagerFromControllerInterface, model:ModelFromControllerInterface):
        self.view=view
        self.model=model
        self.view.create_main_window(self)
        self.model.create_sites()


        self.goto_url=self.model.goto_url

    def goto_url(self, url: URL, **options):
        self.model.goto_url(url, **options)

    def on_cycle_handler(self):
        self.model.on_cycle_handler()

    def on_exit(self):
        self.model.on_exit()
        self.view.on_exit()

if __name__ == "__main__":
    pass