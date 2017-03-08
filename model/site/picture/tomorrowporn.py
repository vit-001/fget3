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
        menu_items=dict(#Movies=URL('http://www.tomorrowporn.com/porn-movies/'),
                        Pics=URL('http://www.tomorrowporn.com/'),
                        LatestUpdates=URL('http://www.tomorrowporn.com/latest_updates.html'),
                    )

        view.add_start_button(name='Tomorrowporn',
                              picture_filename='model/site/resource/picture/tomorrowporn.png',
                              menu_items=menu_items,
                              url=URL("http://www.tomorrowporn.com/"))

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        thumb_containers=_iter(soup.find_all('div',{'class':'thumbs'}))
        for thumb_container in thumb_containers:
            if thumb_container:
                for thumbnail in _iter(thumb_container.find_all('a')):
                    # psp(thumbnail)
                    href_txt = thumbnail.attrs['href']
                    if 'url=' in href_txt:
                        href_txt = quotes(thumbnail.attrs['href'],'url=','&')
                    href=URL(href_txt)
                    description = thumbnail.img.attrs.get('alt','')
                    if description is '':
                        description=href_txt.strip('/').rpartition('/')[2].replace('-',' ')
                    thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                    # print(thumb_url,href,description)
                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                   labels=[{'text': description, 'align': 'bottom center'}])

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'pages'})

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return 'TOP '+ url.get().partition('tomorrowporn.com/')[2].rpartition('.')[0]

    def parse_pictures(self, soup: BeautifulSoup, url: URL):
        image_containers=soup.find_all('div',{'class':'thumb_box'})
        for image_container in _iter(image_containers):
            for image in _iter(image_container.find_all('img')):
                image_url=URL(image.attrs['src'].replace('t.','.'),base_url=url)
                filename=image_url.get_path()+image_url.get().rpartition('/')[2]
                self.add_picture(filename,image_url)

    def parse_pictures_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get().strip('/').rpartition('/')[2]


if __name__ == "__main__":
    pass