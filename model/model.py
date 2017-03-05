# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL
from common.setting import Setting
from model.base_model import ModelFromControllerInterface,ModelFromSiteInterface
from model.loader.multiprocess_az_loader import MultiprocessAZloader,BaseLoader
from view.view_manager_interface import ViewManagerFromModelInterface

from model.site.video.simple.collectionofbestporn import CollectionofbestpornSite
from model.site.video.simple.veronicca_com import VeroniccaComSite
from model.site.video.simple.hd_easyporn import HdEasyporn


class Model(ModelFromControllerInterface, ModelFromSiteInterface):

    def __init__(self, view_manager:ViewManagerFromModelInterface):
        self._view_manager=view_manager
        self._loader=MultiprocessAZloader()
        self._site_models=[CollectionofbestpornSite,VeroniccaComSite,HdEasyporn
                           ]

    def create_sites(self):
        for site_class in self._site_models:
            site_class.create_start_button(self.view_manager)

    def goto_url(self, url: URL, **options):
        for site_class in self._site_models:
            if site_class.can_accept_url(url):
                site=site_class(self)
                site.goto_url(url, **options)
                return
        print('Rejected', url)

    def on_cycle_handler(self):
        self._loader.on_update()

    def on_exit(self):
        self._loader.on_exit()

    @property
    def view_manager(self) -> ViewManagerFromModelInterface:
        return self._view_manager

    @property
    def loader(self) -> BaseLoader:
        return self._loader


if __name__ == "__main__":
    pass