# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL
from model.base_model import AbstractModelFromControllerInterface
from view.base_view import AbstractViewFromModelInterface

from model.site.video.simple.collectionofbestporn import CollectionofbestpornSite


class Model(AbstractModelFromControllerInterface):

    def __init__(self, view:AbstractViewFromModelInterface):
        self.site_models=[CollectionofbestpornSite,
                     ]

        for site_class in self.site_models:
            site_class.create_start_button(view)


    def goto_url(self, url: URL):
        for site_class in self.site_models:
            if site_class.can_accept_url(url):
                site=site_class()
                site.goto_url(url)
                return
        print('Rejected', url)


if __name__ == "__main__":
    pass