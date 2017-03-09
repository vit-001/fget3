# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class Space:
    def __init__(self, text:str, icon_filename:str=None):
        self.text=text
        self.icon_filename=icon_filename

    def can_accept_url(*args) -> bool:
        return False

    def create_start_button(self,view:ViewManagerFromModelInterface):
        view.add_start_button(name=self.text,
                              picture_filename=self.icon_filename,
                              # menu_items=menu_items,
                              url=URL())





if __name__ == "__main__":
    pass