# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL
from model.base_model import AbstractModelFromControllerInterface,AbstractModelFromSiteInterface
from model.loader.multiprocess_az_loader import MultiprocessAZloader,BaseLoader
from view.base_view import AbstractViewFromModelInterface

from model.site.base_site import AbstractSite

from model.site.video.simple.collectionofbestporn import CollectionofbestpornSite


class Model(AbstractModelFromControllerInterface,AbstractModelFromSiteInterface):

    def __init__(self, view:AbstractViewFromModelInterface):
        self._view=view
        self._loader=MultiprocessAZloader()
        self.site_models=[CollectionofbestpornSite,
                     ]

        for site_class in self.site_models:
            site_class.create_start_button(view)


    def goto_url(self, url: URL):
        for site_class in self.site_models:
            if site_class.can_accept_url(url):
                site=site_class(self)
                site.goto_url(url)
                return
        print('Rejected', url)

    @property
    def view(self) -> AbstractViewFromModelInterface:
        return self._view

    @property
    def loader(self) -> BaseLoader:
        return self._loader

    def on_cycle_handler(self):
        self._loader.on_update()

    def on_exit(self):
        self._loader.on_exit()


if __name__ == "__main__":
    pass