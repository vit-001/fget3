# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from data_format.error import AbstractMethodError
from data_format.url import URL

from interface.loader_interface import LoaderInterface
from interface.view_manager_interface import ViewManagerFromModelInterface
from interface.site_interface import SiteInterface
from interface.hystory_interface import HistoryFromModelInterface

class ModelFromControllerInterface:
    def create_sites(self):
        pass

    def goto_url(self, url: URL, **options):
        pass

    def add_to_favorites(self, url: URL, label:str=None):
        pass

    def on_cycle_handler(self):
        pass

    def on_exit(self):
        pass

class ModelFromSiteInterface:
    def can_accept_url(self,url:URL)->SiteInterface.__class__:
        return None

    def get_favorite_items(self, site:SiteInterface)->list:
        pass

    def remove_favorite(self, url):
        pass

    @property
    def view_manager(self)->ViewManagerFromModelInterface:
        raise(AbstractMethodError)

    @property
    def loader(self)->LoaderInterface:
        raise (AbstractMethodError)

    @property
    def thumb_history(self)->HistoryFromModelInterface:
        raise (AbstractMethodError)

    @property
    def full_history(self)->HistoryFromModelInterface:
        raise (AbstractMethodError)

if __name__ == "__main__":
    pass