# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL

from controller.base_controller import ControllerFromModelInterface,ControllerFromViewInterface
from view.base_view import ViewFromControllerInterface
from model.base_model import ModelFromControllerInterface

class Controller(ControllerFromModelInterface,ControllerFromViewInterface):
    def __init__(self, view:ViewFromControllerInterface,model:ModelFromControllerInterface):
        self.view=view
        self.model=model
        self.view.register_controller(self)

    def on_cycle_handler(self):
        self.model.on_cycle_handler()

if __name__ == "__main__":
    pass