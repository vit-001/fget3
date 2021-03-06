# -*- coding: utf-8 -*-
__author__ = 'Vit'
from common.setting import Setting
from data_format.url import URL
from interface.loader_interface import LoaderInterface
from interface.model_interface import ModelFromControllerInterface, ModelFromSiteInterface
from interface.site_interface import SiteInterface
from interface.view_manager_interface import ViewManagerFromModelInterface
from model.favorites.favorites import Favorites
from model.history_model.hystory import HistoryModel
from model.loader.multiprocess_az_loader import MultiprocessAZloader
from model.site.other.space import Space
from model.site.picture.tgp_sites.babesandbitches import BabesandbitchesSite
from model.site.picture.tgp_sites.bravoerotica import BravoeroticaSite
from model.site.picture.tgp_sites.fuskator import FuskatorSite
from model.site.picture.tgp_sites.teenport import TeenportSite
from model.site.picture.tgp_sites.tomorrowporn import TomorrowpornSite
from model.site.picture.tgp_sites.vibraporn import VibrapornSite
from model.site.video.plus_file.pornbaze import PornbrazeSite
from model.site.video.plus_file.pornfun import PornfunSite
from model.site.video.plus_file.post.donfreeporn import DonfreepornSite
from model.site.video.plus_file.sexix import SexixSite
from model.site.video.plus_file.toseeporn import ToseepornSite
from model.site.video.plus_file.yourporn import YourpornSite
from model.site.video.script.beemtube import BeemtubeSite
from model.site.video.script.deviantclip import DeviantclipSite
from model.site.video.script.motherless import MotherlessSite
from model.site.video.script.porncom import PornComSite
from model.site.video.script.pornhd import PornhdSite
from model.site.video.script.pornoxo import PornoxoSite
from model.site.video.script.pornsland import PornslandSite
from model.site.video.script.porntrex import PorntrexSite
from model.site.video.script.realgf import RealGfSite
from model.site.video.script.redtube import RedtubeSite
from model.site.video.script.shockingmovies import ShockingmoviesSite
from model.site.video.script.spankwire import SpankwireSite
from model.site.video.script.thumbzilla import ThumbzillaSite
from model.site.video.script.tube8 import Tube8Site
from model.site.video.script.v24videos import V24videoSite
from model.site.video.script.xhamster import XhamsterSite
from model.site.video.script.xvideo import XvideoSite
from model.site.video.simple.collectionofbestporn import CollectionofbestpornSite
from model.site.video.simple.hd_easyporn import HdEasypornSite
from model.site.video.simple.heavy_r import HeavyRSite
from model.site.video.simple.plusone8 import PlusoneSite
from model.site.video.simple.pornbozz import PornbozzSite
from model.site.video.simple.sextube_nl import SextubeNlSite
from model.site.video.simple.veronicca import VeroniccaComSite
from model.site.video.simple.vporn import VpornSite
from model.site.video.xhr.extremetube import ExtremetubeSite
from model.site.video.xhr.pervertslut import PervertslutSite
from model.site.video.script.xnxx import XnxxSite
from model.site.video.simple.tnaflix import TnaflixSite


class Model(ModelFromControllerInterface, ModelFromSiteInterface):

    def __init__(self, view_manager:ViewManagerFromModelInterface):
        self._view_manager=view_manager
        self._loader=MultiprocessAZloader()
        self._site_models=[



                           Space('Classic:'),
                           YourpornSite, PlusoneSite, TnaflixSite, PorntrexSite,SexixSite,RedtubeSite,
                           XhamsterSite, CollectionofbestpornSite, PornComSite, PornhdSite,ThumbzillaSite,
                           PornbrazeSite,XvideoSite,ToseepornSite,SextubeNlSite,
                           PornoxoSite,  VpornSite,DonfreepornSite,SpankwireSite,XnxxSite,
                           VeroniccaComSite, HdEasypornSite, Tube8Site,BeemtubeSite,

                           Space('Amateur:'),
                           MotherlessSite, RealGfSite, PornfunSite,PornbozzSite,

                           Space('Deviant:'),
                           ShockingmoviesSite,DeviantclipSite,ExtremetubeSite,PervertslutSite,

                           # Space('Short:'),

                           Space('Photo:'),
                           BravoeroticaSite,TomorrowpornSite,TeenportSite,VibrapornSite,
                           BabesandbitchesSite,FuskatorSite,
                           Space('Non working:'),
                           HeavyRSite,PornslandSite,V24videoSite,

                           # Space('Info:'),

                           ]

        self._thumb_history=HistoryModel('thumb', self._view_manager.on_thumb_history_changed)
        self._full_history=HistoryModel('full', self._view_manager.on_full_history_changed)
        self._favorites=Favorites(Setting.global_data_path+'favorites.json')

        n=0
        for site in self._site_models:
           n+=site.number_of_accepted_dimains()
        print('No of sites:',n)


    def create_sites(self):
        for site_class in self._site_models:
            site_class.create_start_button(self.view_manager)

    def goto_url(self, url: URL, **options):
        site=self.can_accept_url(url)
        if site:
            site(self).goto_url(url, **options)
        else:
            print('Rejected', url)

    def add_to_favorites(self, url: URL, label:str=None):
        if label:
            self._favorites.add(label,url)
        else:
            site_class=self.can_accept_url(url)
            if site_class:
                label=site_class.get_thumb_label(url)
                self._favorites.add(label, url)

    def remove_favorite(self, url):
        print('Removing',url)
        self._favorites.remove(url)
        self._view_manager.refresh_thumb_view()

    def get_favorite_items(self, site: SiteInterface) -> list:
        return self._favorites.get_favorite_items(site)

    def can_accept_url(self, url: URL):
        for site_class in self._site_models:
            if site_class.can_accept_url(url):
                return site_class
        return None

    def on_cycle_handler(self):
        self._loader.on_update()

    def on_exit(self):
        self._loader.on_exit()
        self._favorites.on_exit()

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