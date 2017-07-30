# -*- coding: utf-8 -*-
__author__ = 'Vit'

from data_format.url import URL
from interface.site_interface import SiteInterface

class FavoritesInterface:
    def on_exit(self):
        pass

    def add(self, label:str, url: URL):
        pass

    def remove(self, url:URL):
        pass

    def get_favorite_items(self, site: SiteInterface) -> list:
        pass

if __name__ == "__main__":
    pass