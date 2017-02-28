# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL
from view.base_view import AbstractViewFromModelInterface

class AbstractSite:

    @staticmethod
    def create_start_button(view:AbstractViewFromModelInterface):
        pass

    @staticmethod
    def can_accept_url(url:URL)->bool:
        return False

    def goto_url(self, url:URL, **options):
        pass

if __name__ == "__main__":
    pass