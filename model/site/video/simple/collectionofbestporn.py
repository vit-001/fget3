# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL

from model.site.base_site import AbstractSite,AbstractViewFromModelInterface

class CollectionofbestpornSite(AbstractSite):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('collectionofbestporn.com/')

    @staticmethod
    def create_start_button(view: AbstractViewFromModelInterface):
        print('Create CollectionofbestpornSite button')

    def goto_url(self, url: URL, **options):
        print('CollectionofbestpornSite goto:',url)


if __name__ == "__main__":
    pass