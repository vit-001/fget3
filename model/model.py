# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.url import URL
from model.base_model import ModelFromControllerInterface,ModelFromSiteInterface
from model.loader.multiprocess_az_loader import MultiprocessAZloader,BaseLoader
from model.history_model.hystory import HistoryModel

from view.view_manager_interface import ViewManagerFromModelInterface

from model.site.video.script.shockingmovies import ShockingmoviesSite
from model.site.video.simple.collectionofbestporn import CollectionofbestpornSite
from model.site.video.simple.hd_easyporn import HdEasypornSite
from model.site.video.simple.veronicca import VeroniccaComSite
from model.site.video.script.xhamster import XhamsterSite

class Model(ModelFromControllerInterface, ModelFromSiteInterface):

    def __init__(self, view_manager:ViewManagerFromModelInterface):
        self._view_manager=view_manager
        self._loader=MultiprocessAZloader()
        self._site_models=[XhamsterSite, CollectionofbestpornSite, VeroniccaComSite, HdEasypornSite, ShockingmoviesSite
                           ]

        self._thumb_history=HistoryModel('thumb', self._view_manager.on_thumb_history_changed)
        self._full_history=HistoryModel('full', self._view_manager.on_full_history_changed)

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

    @property
    def full_history(self) -> HistoryModel:
        return self._full_history

    @property
    def thumb_history(self) -> HistoryModel:
        return self._thumb_history


if __name__ == "__main__":
    pass