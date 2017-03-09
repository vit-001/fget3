# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class TeenportSite(BaseSiteParser):
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

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        thumb_containers=_iter(soup.find_all('div',{'class':'thumbs_main'}))
        for thumb_container in thumb_containers:
            if thumb_container:
                for thumbnail in _iter(thumb_container.find_all('a')):
                    self.parse_thumb(thumbnail,url)
                    # psp(thumbnail)
                    # href_txt = thumbnail.attrs['href']
                    # if 'url=' in href_txt:
                    #     href_txt = quotes(href_txt,'url=','&')
                    # href=URL(href_txt)
                    # description = thumbnail.img.attrs.get('alt','')
                    # if description is '':
                    #     description=href_txt.strip('/').rpartition('/')[2].replace('-',' ')
                    # thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
                    # # print(thumb_url,href,description)
                    # self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                    #                labels=[{'text': description, 'align': 'bottom center'}])

    def parse_others(self, soup: BeautifulSoup, url: URL):
        # container=soup.find_all('body')
        # for item in _iter(container):
        #     psp(item.prettify())
            thumbs=soup.find_all('a',{'class':['list_model2','list_model']})
            for thumb in _iter(thumbs):
                psp(thumb)
                self.parse_thumb(thumb, url)

    def parse_thumb(self, thumbnail:BeautifulSoup, url:URL):
        # psp(thumbnail)
        href_txt = thumbnail.attrs['href']
        if 'url=' in href_txt:
            href_txt = quotes(href_txt, 'url=', '&')
        href = URL(href_txt.strip('/')+'/')
        description = thumbnail.img.attrs.get('alt', '')
        if description is '':
            description = href_txt.strip('/').rpartition('/')[2].replace('-', ' ')
        thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
        # print(thumb_url,href,description)
        self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                       labels=[{'text': description, 'align': 'bottom center'}])

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'head'})

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return 'TP '+ url.get().partition('teenport.com/')[2].rpartition('.')[0]

    def parse_pictures(self, soup: BeautifulSoup, url: URL):
        image_containers=soup.find_all('div',{'class':'thumb_box'})
        for image_container in _iter(image_containers):
            for image in _iter(image_container.find_all('img')):
                print(url,image.attrs['src'])
                image_url=URL(image.attrs['src'].replace('t.','.'),base_url=url)
                filename=image_url.get_path()+image_url.get().rpartition('/')[2]
                self.add_picture(filename,image_url)

    def parse_pictures_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get().strip('/').rpartition('/')[2]

    def parse_pictures_tags(self, soup:BeautifulSoup, url:URL):
        for tag_container in _iter(soup.find_all('div', {'class': 'title'})):
            for href in _iter(tag_container.find_all('a')):
                if href.string is not None:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url))

if __name__ == "__main__":
    pass