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

    @staticmethod
    def number_of_accepted_dimains()->int:
        return 0

    @staticmethod
    def get_thumb_label(url:URL)->str:
        return 'xxxx'

    @staticmethod
    def get_full_label(url:URL)->str:
        return ''

    def goto_url(self, url:URL, **options):
        pass

    def log(self, text:str):
        pass

if __name__ == "__main__":
    pass

