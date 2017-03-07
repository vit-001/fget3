# -*- coding: utf-8 -*-
__author__ = 'Vit'

from data_format.url import URL
from interface.view_manager_interface import ViewManagerFromModelInterface

class SiteInterface:
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        pass

    @staticmethod
    def can_accept_url(url:URL)->bool:
        return False

    def goto_url(self, url:URL, **options):
        pass


if __name__ == "__main__":
    pass

