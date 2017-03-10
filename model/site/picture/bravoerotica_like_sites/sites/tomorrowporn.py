# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.picture.bravoerotica_like_sites.base_of_be import BravoeroticaLikeSite


class TomorrowpornSite(BravoeroticaLikeSite):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('tomorrowporn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(#Movies=URL('http://www.tomorrowporn.com/porn-movies/'),
                        Pics=URL('http://www.tomorrowporn.com/'),
                        LatestUpdates=URL('http://www.tomorrowporn.com/latest_updates.html'),
                    )

        view.add_start_button(picture_filename='model/site/resource/picture/tomorrowporn.png',
                              # menu_items=menu_items,
                              url=URL("http://www.tomorrowporn.com/"))

    def get_shrink_name(self):
        return 'TWP '

    def get_thumbs_containers(self, soup: BeautifulSoup) -> list:
        container = soup.find_all('div',{'class':'thumbs'})
        if container:
            return container

        container = soup.find_all('ul',{'class':'sub_thumb_list'})
        if container:
            return container

    # def parse_pictures_title(self, soup: BeautifulSoup, url: URL) -> str:
    #     return url.get().strip('/').rpartition('/')[2]

    def get_picture_tag_containers(self, soup: BeautifulSoup) -> list:
        tag_container=soup.find('div',{'class':'menus'})
        return tag_container.find_all('h2') if tag_container else []


if __name__ == "__main__":
    pass