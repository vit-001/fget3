# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.picture.bravoerotica_like_sites.base_of_be import BravoeroticaLikeSite


class TeenportSite(BravoeroticaLikeSite):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('teenport.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(#Movies=URL('http://www.tomorrowporn.com/porn-movies/'),
                        Pics=URL('http://www.tomorrowporn.com/'),
                        LatestUpdates=URL('http://www.tomorrowporn.com/latest_updates.html'),
                    )

        view.add_start_button(name='Teenport',
                              picture_filename='model/site/resource/picture/teenport.gif',
                              # menu_items=menu_items,
                              url=URL("http://www.teenport.com/st/archives/archive1.html"))

    def get_thumbs_containers(self, soup: BeautifulSoup) -> list:
        return soup.find_all('div',{'class':'thumbs_main'})

    def get_others_thumbs(self, soup: BeautifulSoup) -> list:
        return soup.find_all('a',{'class':['list_model2','list_model']})

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'head'})

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return 'TP '+ url.get().partition('teenport.com/')[2].rpartition('.')[0]

    def get_pictures_containers(self, soup: BeautifulSoup) -> list:
        return soup.find_all('div',{'class':'thumb_box'})

    def parse_pictures_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get().strip('/').rpartition('/')[2]

    def get_picture_tag_containers(self, soup: BeautifulSoup) -> list:
        return soup.find_all('div', {'class': 'title'})


if __name__ == "__main__":
    pass