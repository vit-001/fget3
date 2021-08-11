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
from model.loader.multiprocess_loader import MultiprocessLoader
from model.site.other.space import Space
from model.site.picture.tgp_sites.babesandbitches import BabesandbitchesSite
from model.site.picture.tgp_sites.bravoerotica import BravoeroticaSite
from model.site.picture.tgp_sites.teenport import TeenportSite
from model.site.picture.tgp_sites.tomorrowporn import TomorrowpornSite
from model.site.picture.tgp_sites.vibraporn import VibrapornSite
from model.site.video.plus_file.pornfun import PornfunSite
from model.site.video.plus_file.pornmz import PornmzSite
from model.site.video.plus_file.pornwild import PornwildSite
from model.site.video.plus_file.sexix import SexixSite
from model.site.video.plus_file.yespornpleasexxx import YespornpleasexxxSite
from model.site.video.plus_file.yourporn import YourpornSite
from model.site.video.script.beemtube import BeemtubeSite
from model.site.video.script.boundhub import BoundhubSite
from model.site.video.script.deviantclip import DeviantclipSite
from model.site.video.script.jizzbunker import JizzbunkerSite
from model.site.video.script.motherless import MotherlessSite
from model.site.video.script.porn0sex import Porn0sexSite
from model.site.video.script.porncom import PornComSite
from model.site.video.script.pornhd import PornhdSite
from model.site.video.script.pornoxo import PornoxoSite
from model.site.video.script.pornsland import PornslandSite
from model.site.video.script.porntrex import PorntrexSite
from model.site.video.script.realgf import RealGfSite
from model.site.video.script.redtube import RedtubeSite
from model.site.video.script.rusvideos import RusvideosSite
from model.site.video.script.shockingmovies import ShockingmoviesSite
from model.site.video.script.spankwire import SpankwireSite
from model.site.video.script.thumbzilla import ThumbzillaSite
from model.site.video.script.tube8 import Tube8Site
from model.site.video.script.v24videos import V24videoSite
from model.site.video.script.xhamster import XhamsterSite
from model.site.video.script.xnxx import XnxxSite
from model.site.video.script.xvideo import XvideoSite
from model.site.video.script.youngpornvideos import YoungPornVideosSite
from model.site.video.simple.collectionofbestporn import CollectionofbestpornSite
from model.site.video.simple.gigporno import GigpornoSite
from model.site.video.simple.hd_easyporn import HdEasypornSite
from model.site.video.simple.heavy_r import HeavyRSite
from model.site.video.simple.plusone8 import PlusoneSite
from model.site.video.simple.pornbozz import PornbozzSite
from model.site.video.simple.porngo import PorngoSite
from model.site.video.simple.pornone import PornoneSite
from model.site.video.simple.sextube_nl import SextubeNlSite
from model.site.video.simple.test import TestSite
from model.site.video.simple.tnaflix import TnaflixSite
from model.site.video.xhr.extremetube import ExtremetubeSite
from model.site.video.xhr.pervertslut import PervertslutSite
from model.site.video.simple.pornoakt import PornoaktSite
from model.site.video.script.pornobomba import PornobombaSite
from model.site.video.simple.homeporno import HomepornoSite
from model.site.video.simple.spreee import SpreeeSite
from model.site.video.simple.hotscope import HotscopeSite
from model.site.video.simple.ruleporn import RulepornSite
from model.site.video.simple.pohub import PohubSite
from model.site.video.simple.xdporner import XdpornerSite
from model.site.video.plus_file.pornvibe import PornvibeSite
from model.site.video.simple.rapelust import RapelustSite
from model.site.video.simple.freeuseporn import FreeusepornSite
from model.site.video.simple.pornxxxvideos import PornxxxvideosSite
from model.site.video.simple.dlouha import DlouhaSite
from model.site.video.simple.darknessporn import DarknesspornSite
from model.site.video.simple.sickjunk import SickjunkSite
from model.site.video.script.shooshtime import ShooshtimeSite
from model.site.video.script.petardashd import PetardashdSite
from model.site.video.simple.pornozot import PornozotSite
from model.site.video.script.pornhub import PornhubSite
from model.site.video.simple.fapmeifyoucan import FapmeifyoucanSite

class Model(ModelFromControllerInterface, ModelFromSiteInterface):

    def __init__(self, view_manager:ViewManagerFromModelInterface):
        self._view_manager=view_manager
        self._loader=MultiprocessLoader()
        self._site_models=[
                            TestSite,











                            Space('Classic:'),
                            PornhubSite,XhamsterSite,FapmeifyoucanSite,
                            DlouhaSite,ShooshtimeSite,
                            PornwildSite,PornmzSite,PornozotSite,
                            YespornpleasexxxSite,PohubSite,SickjunkSite,
                            PornoaktSite,SpreeeSite,XnxxSite,XdpornerSite,
                            PornvibeSite,RapelustSite,DarknesspornSite,FreeusepornSite,
                            PornobombaSite,XvideoSite,RulepornSite,
                            GigpornoSite,JizzbunkerSite,PornxxxvideosSite,
                            HomepornoSite,PetardashdSite,


            SextubeNlSite,


                            Space('Amateur:'),
                             RealGfSite,

                            Space('Deviant:'),
                            BoundhubSite, ShockingmoviesSite,

                           # Space('Short:'),

                            Space('Photo:'),
                            BravoeroticaSite,TomorrowpornSite,TeenportSite,VibrapornSite,
                            BabesandbitchesSite,
                            Space('Non working:'),
                            RusvideosSite, HdEasypornSite, RedtubeSite,
                             PlusoneSite,
                            CollectionofbestpornSite,
                            PorngoSite,
            HotscopeSite,
                            HeavyRSite,PornslandSite,V24videoSite,YourpornSite,TnaflixSite,SexixSite,
                            PornhdSite,ThumbzillaSite,SpankwireSite,
                            PornComSite,PornoxoSite,YoungPornVideosSite,
                            DeviantclipSite,ExtremetubeSite,PervertslutSite,MotherlessSite,PornfunSite,PornbozzSite,
                            Tube8Site,BeemtubeSite,PornoneSite,Porn0sexSite,
                            Space('Blocked'),
                            PorntrexSite,

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