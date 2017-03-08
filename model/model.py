# -*- coding: utf-8 -*-
__author__ = 'Vit'
from data_format.url import URL

from interface.loader_interface import LoaderInterface
from interface.model_interface import ModelFromControllerInterface,ModelFromSiteInterface
from interface.view_manager_interface import ViewManagerFromModelInterface
from interface.site_interface import SiteInterface

from model.history_model.hystory import HistoryModel
from model.loader.multiprocess_az_loader import MultiprocessAZloader

from model.site.picture.tomorrowporn import TomorrowpornSite

from model.site.video.script.shockingmovies import ShockingmoviesSite
from model.site.video.script.xhamster import XhamsterSite
from model.site.video.simple.collectionofbestporn import CollectionofbestpornSite
from model.site.video.simple.hd_easyporn import HdEasypornSite
from model.site.video.simple.veronicca import VeroniccaComSite
from model.site.video.script.v24videos import V24videoSite
from model.site.video.script.redtube import RedtubeSite
from model.site.video.script.realgf import RealGfSite
from model.site.video.script.pornoxo import PornoxoSite
from model.site.video.script.porncom import PornComSite
from model.site.video.script.motherless import MotherlessSite


class Model(ModelFromControllerInterface, ModelFromSiteInterface):

    def __init__(self, view_manager:ViewManagerFromModelInterface):
        self._view_manager=view_manager
        self._loader=MultiprocessAZloader()
        self._site_models=[TomorrowpornSite,
                           XhamsterSite, CollectionofbestpornSite,PornComSite,
                           RedtubeSite, RealGfSite, PornoxoSite, MotherlessSite,
                           VeroniccaComSite, HdEasypornSite, ShockingmoviesSite, V24videoSite
                           ]

        self._thumb_history=HistoryModel('thumb', self._view_manager.on_thumb_history_changed)
        self._full_history=HistoryModel('full', self._view_manager.on_full_history_changed)

    def create_sites(self):
        for site_class in self._site_models:
            site_class.create_start_button(self.view_manager)

    def goto_url(self, url: URL, **options):
        site=self.can_accept_url(url)
        if site:
            site(self).goto_url(url, **options)
        else:
            print('Rejected', url)
        # for site_class in self._site_models:
        #     if site_class.can_accept_url(url):
        #         site=site_class(self)
        #         site.goto_url(url, **options)
        #         return
        # print('Rejected', url)

    def can_accept_url(self, url: URL) -> SiteInterface.__class__:
        for site_class in self._site_models:
            if site_class.can_accept_url(url):
                return site_class
        return None

    def on_cycle_handler(self):
        self._loader.on_update()

    def on_exit(self):
        self._loader.on_exit()

    @property
    def view_manager(self) -> ViewManagerFromModelInterface:
        return self._view_manager

    @property
    def loader(self) -> LoaderInterface:
        return self._loader

    @property
    def full_history(self) -> HistoryModel:
        return self._full_history

    @property
    def thumb_history(self) -> HistoryModel:
        return self._thumb_history


if __name__ == "__main__":
    pass