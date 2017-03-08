# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.base_site import BaseSiteParser


class TomorrowpornSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('tomorrowporn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(HD=URL('http://collectionofbestporn.com/tag/hd-porn*'),
                    Latest=URL('http://collectionofbestporn.com/most-recent*'),
                    TopRated=URL('http://collectionofbestporn.com/top-rated*'),
                    MostViewed=URL('http://collectionofbestporn.com/most-viewed*'),
                    Categories=URL('http://collectionofbestporn.com/channels/'),
                    Longest=URL('http://collectionofbestporn.com/longest*'))

        view.add_start_button(name='Tomorrowporn',
                              picture_filename='model/site/resource/picture/tomorrowporn.png',
                              # menu_items=menu_items,
                              url=URL("http://www.tomorrowporn.com/"))

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        thumb_containers=_iter(soup.find_all('div',{'class':'thumbs'}))
        for thumb_container in thumb_containers:
            if thumb_container:
                for thumbnail in _iter(thumb_container.find_all('a')):
                    # psp(thumbnail.prettify())
                    href_txt = quotes(thumbnail.attrs['href'],'url=','&')
                    # print(href_txt)

                    href=URL(href_txt)
                    # print(href)
                    description = thumbnail.img.attrs['alt']
                    thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                    #
                    # duration = thumbnail.find('span', {'class': "time"})
                    # dur_time = '' if duration is None else str(duration.string)
                    #
                    # quality = thumbnail.find('span', {'class': "quality"})
                    # qual = '' if quality is None else str(quality.string)
                    #
                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                               labels=[#{'text': dur_time, 'align': 'top right'},
                                                       {'text': description, 'align': 'bottom center'}])
                                                       # {'text': qual, 'align': 'top left', 'bold': True}])

        # print(len(self.thumbs))

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'pages'})

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return 'TOP '+ url.get().partition('tomorrowporn.com/')[2].rpartition('.')[0]

    def parse_pictures(self, soup: BeautifulSoup, url: URL):
        # print(url)
        image_containers=soup.find_all('div',{'class':'thumb_box'})
        for image_container in _iter(image_containers):
            for image in _iter(image_container.find_all('img')):
                # psp(image)
                image_url=URL(image.attrs['src'].replace('t.','.'),base_url=url)
                filename=image_url.get_path()+image_url.get().rpartition('/')[2]
                # print(image_url)
                # print(image_url.get_path())
                self.add_picture(filename,image_url)

    def parse_pictures_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get().strip('/').rpartition('/')[2]


if __name__ == "__main__":
    pass