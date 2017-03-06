# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from common.url import URL
from common.exception import AbstractMethodError
from view.view_manager_interface import ViewManagerFromModelInterface
from model.loader.base_loader import BaseLoader
from model.history_model.hystory import HistoryModel

class ModelFromControllerInterface:
    def create_sites(self):
        pass

    def goto_url(self, url: URL, **options):
        pass

    def on_cycle_handler(self):
        pass

    def on_exit(self):
        pass

class ModelFromSiteInterface:
    @property
    def view_manager(self)->ViewManagerFromModelInterface:
        raise(AbstractMethodError)

    @property
    def loader(self)->BaseLoader:
        raise (AbstractMethodError)

    @property
    def thumb_history(self)->HistoryModel:
        raise (AbstractMethodError)

    @property
    def full_history(self)->HistoryModel:
        raise (AbstractMethodError)

if __name__ == "__main__":
    pass