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

from model.site.video.plus_file._nonwork.pornfun import PornfunSite
from model.site.video.plus_file._nonwork.sexix import SexixSite
from model.site.video.plus_file._nonwork.yourporn import YourpornSite
from model.site.video.plus_file.pornmz import PornmzSite
from model.site.video.plus_file.pornvibe import PornvibeSite
from model.site.video.plus_file.pornwild import PornwildSite
from model.site.video.plus_file.redtube import RedtubeSite
from model.site.video.plus_file.yespornpleasexxx import YespornpleasexxxSite

from model.site.video.script._nonwork.beemtube import BeemtubeSite
from model.site.video.script._nonwork.deviantclip import DeviantclipSite
from model.site.video.script._nonwork.motherless import MotherlessSite
from model.site.video.script._nonwork.porn0sex import Porn0sexSite
from model.site.video.script._nonwork.porncom import PornComSite
from model.site.video.script._nonwork.pornhd import PornhdSite
from model.site.video.script._nonwork.pornoxo import PornoxoSite
from model.site.video.script._nonwork.pornsland import PornslandSite
from model.site.video.script._nonwork.porntrex import PorntrexSite
from model.site.video.script._nonwork.rusvideos import RusvideosSite
from model.site.video.script._nonwork.spankwire import SpankwireSite
from model.site.video.script._nonwork.thumbzilla import ThumbzillaSite
from model.site.video.script._nonwork.tube8 import Tube8Site
from model.site.video.script._nonwork.v24videos import V24videoSite
from model.site.video.script._nonwork.youngpornvideos import YoungPornVideosSite
from model.site.video.script.boundhub import BoundhubSite
from model.site.video.script.jizzbunker import JizzbunkerSite
from model.site.video.script.katestube import KatestubeSite
from model.site.video.script.pervclips import PervclipsSite
from model.site.video.script.petardashd import PetardashdSite
from model.site.video.script.pornhub import PornhubSite
from model.site.video.script.pornicom import PornicomSite
from model.site.video.script.pornobomba import PornobombaSite
from model.site.video.script.pornwatchers import PornwatchersSite
from model.site.video.script.pornwhite import PornwhiteSite
from model.site.video.script.realgf import RealGfSite
from model.site.video.script.shockingmovies import ShockingmoviesSite
from model.site.video.script.shooshtime import ShooshtimeSite
from model.site.video.script.sleazyneasy import SleazyneasySite
from model.site.video.script.vikiporn import VikipornSite
from model.site.video.script.xhamster import XhamsterSite
from model.site.video.script.xnxx import XnxxSite
from model.site.video.script.xvideo import XvideoSite
from model.site.video.script.tprn import TprnSite
from model.site.video.script.frprn import FrprnSite
from model.site.video.script.xhand import XhandSite
from model.site.video.script.analdin import AnaldinSite
from model.site.video.script.crockotube import CrockotubeSite
from model.site.video.script.tryboobs import TryboobsSite
from model.site.video.script.xozilla import XozillaSite
from model.site.video.script.tubous import TubousSite
from model.site.video.script.xtits import XtitsSite

from model.site.video.simple.bravotube import BravotubeSite
from model.site.video.simple._nonwork.plusone8 import PlusoneSite
from model.site.video.simple._nonwork.collectionofbestporn import CollectionofbestpornSite
from model.site.video.simple._nonwork.hd_easyporn import HdEasypornSite
from model.site.video.simple._nonwork.heavy_r import HeavyRSite
from model.site.video.simple._nonwork.hotscope import HotscopeSite
from model.site.video.simple._nonwork.pornbozz import PornbozzSite
from model.site.video.simple._nonwork.porngo import PorngoSite
from model.site.video.simple._nonwork.pornone import PornoneSite
from model.site.video.simple._nonwork.tnaflix import TnaflixSite
from model.site.video.simple._nonwork.darknessporn import DarknesspornSite
from model.site.video.simple.dlouha import DlouhaSite
from model.site.video.simple.fapmeifyoucan import FapmeifyoucanSite
from model.site.video.simple.freeuseporn import FreeusepornSite
from model.site.video.simple.gigporno import GigpornoSite
from model.site.video.simple.homeporno import HomepornoSite
from model.site.video.simple.its import ItsSite
from model.site.video.simple.pohub import PohubSite
from model.site.video.simple.pornoakt import PornoaktSite
from model.site.video.simple.pornozot import PornozotSite
from model.site.video.simple.pornxxxvideos import PornxxxvideosSite
from model.site.video.simple.rapelust import RapelustSite
from model.site.video.simple.ruleporn import RulepornSite
from model.site.video.simple.sextube_nl import SextubeNlSite
from model.site.video.simple.sickjunk import SickjunkSite
from model.site.video.simple.spreee import SpreeeSite
from model.site.video.simple.test import TestSite
from model.site.video.simple.xdporner import XdpornerSite
from model.site.video.simple.iporntoo import IporntooSite
from model.site.video.simple.bdsmone import BdsmoneSite
from model.site.video.simple.crocotube import CrocotubeSite
from model.site.video.simple.fapguru import FapguruSite
from model.site.video.simple.freeporn import FreepornSite
from model.site.video.simple.hdporn import HdpornSite
from model.site.video.simple.pornpapa import PornpapaSite
from model.site.video.simple.sex3 import Sex3Site
from model.site.video.simple.sextubefun import SextubefunSite
from model.site.video.simple.stileproject import StileprojectSite
from model.site.video.simple.spicyflix import SpicyflixSite
from model.site.video.simple.xcum import XcumSite


from model.site.video.xhr._nonwork.extremetube import ExtremetubeSite
from model.site.video.xhr._nonwork.pervertslut import PervertslutSite


class Model(ModelFromControllerInterface, ModelFromSiteInterface):

    def __init__(self, view_manager:ViewManagerFromModelInterface):
        self._view_manager=view_manager
        self._loader=MultiprocessLoader()
        self._site_models=[
                            TestSite,   XcumSite, TubousSite, SextubefunSite,




                            Space('Classic:'),


                            XozillaSite,XtitsSite,
                            XhamsterSite,Sex3Site,
                            AnaldinSite,
                            BravotubeSite,
                            KatestubeSite,ShockingmoviesSite,HdpornSite,
                            PornhubSite,TprnSite,CrocotubeSite,
                            RedtubeSite,PornicomSite,SleazyneasySite,PervclipsSite,VikipornSite,IporntooSite,
                            XhandSite,ShooshtimeSite,
                            ItsSite,FapmeifyoucanSite,
                            DlouhaSite,FrprnSite,
                            PornwildSite,PornmzSite,PornwhiteSite,CrockotubeSite,
                            YespornpleasexxxSite,SickjunkSite,
                            SpreeeSite,XdpornerSite,
                            PornvibeSite,
                            XvideoSite,RulepornSite,
                            GigpornoSite,JizzbunkerSite,
                            HomepornoSite,PetardashdSite,


                            SextubeNlSite,


                            Space('Static:'),
            TryboobsSite,SpicyflixSite,StileprojectSite, FapguruSite,FreepornSite,PornpapaSite,PornwatchersSite,XnxxSite,PornxxxvideosSite,



                            # Space('Amateur:'),


                            Space('Deviant:'),
                            BoundhubSite,BdsmoneSite,RapelustSite,FreeusepornSite,

                           # Space('Short:'),

                            Space('Photo:'),
                            BravoeroticaSite,TomorrowpornSite,TeenportSite,VibrapornSite,
                            BabesandbitchesSite,

                            Space('Non working:'),
                            DarknesspornSite,PornobombaSite,RealGfSite,
                            RusvideosSite, HdEasypornSite,PohubSite,PornozotSite,PornoaktSite,
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