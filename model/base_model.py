# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from common.url import URL
from common.exception import AbstractMethodError
from view.base_view import ViewManagerFromModelInterface
from model.loader.base_loader import BaseLoader

class ModelFromControllerInterface:
    def goto_url(self, url:URL):
        pass

    def on_cycle_handler(self):
        pass

    def on_exit(self):
        pass

class ModelFromSiteInterface:
    @property
    def view(self)->ViewManagerFromModelInterface:
        raise(AbstractMethodError)

    @property
    def loader(self)->BaseLoader:
        raise (AbstractMethodError)

if __name__ == "__main__":
    pass