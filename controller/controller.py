# -*- coding: utf-8 -*-
__author__ = 'Vit'
from data_format.url import URL

from interface.controller_interface import ControllerFromModelInterface,ControllerFromViewInterface
from interface.model_interface import ModelFromControllerInterface
from interface.view_manager_interface import ViewManagerFromControllerInterface

class Controller(ControllerFromModelInterface,ControllerFromViewInterface):
    def __init__(self, view:ViewManagerFromControllerInterface, model:ModelFromControllerInterface):
        self.view=view
        self.model=model
        self.view.create_main_window(self)
        self.model.create_sites()


        self.goto_url=self.model.goto_url

    def goto_url(self, url: URL, **options):
        self.model.goto_url(url, **options)

    def favorite_add(self, url: URL):
        self.model.add_to_favorites(url)

    def on_cycle_handler(self):
        self.model.on_cycle_handler()

    def on_exit(self):
        self.model.on_exit()


if __name__ == "__main__":
    pass