# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL
from model.base_model import ModelFromControllerInterface,ModelFromSiteInterface
from model.loader.multiprocess_az_loader import MultiprocessAZloader,BaseLoader
from view.base_view import ViewFromModelInterface

from model.site.video.simple.collectionofbestporn import CollectionofbestpornSite
from model.site.video.simple.veronicca_com import VeroniccaComSite


class Model(ModelFromControllerInterface, ModelFromSiteInterface):

    def __init__(self, view:ViewFromModelInterface):
        self._view=view
        self._loader=MultiprocessAZloader()
        self._site_models=[CollectionofbestpornSite,VeroniccaComSite,
                           ]

        for site_class in self._site_models:
            site_class.create_start_button(view)

    def goto_url(self, url: URL):
        for site_class in self._site_models:
            if site_class.can_accept_url(url):
                site=site_class(self)
                site.goto_url(url)
                return
        print('Rejected', url)

    def on_cycle_handler(self):
        self._loader.on_update()

    def on_exit(self):
        self._loader.on_exit()

    @property
    def view(self) -> ViewFromModelInterface:
        return self._view

    @property
    def loader(self) -> BaseLoader:
        return self._loader


if __name__ == "__main__":
    pass