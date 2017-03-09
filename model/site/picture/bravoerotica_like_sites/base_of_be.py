# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class BravoeroticaLikeSite(BaseSiteParser):
    def parse_picture_thumbs(self, soup:BeautifulSoup, url:URL):
        for thumb_container in _iter(self.get_thumbs_containers(soup)):
            if thumb_container:
                for thumbnail in _iter(thumb_container.find_all('a')):
                    self.parse_one_thumb(thumbnail,url)

    def get_thumbs_containers(self,soup:BeautifulSoup)->list:
        return soup.find_all('div',{'class':'thumbs'})

    def parse_others(self, soup: BeautifulSoup, url: URL):
        for thumb in _iter(self.get_others_thumbs(soup)):
            self.parse_one_thumb(thumb, url)

    def get_others_thumbs(self, soup:BeautifulSoup)->list:
        return soup.find_all('a',{'class':['list','list_model']})

    def parse_one_thumb(self, thumbnail:BeautifulSoup, url:URL):
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

    def get_pagination_container(self, soup: BeautifulSoup)->BeautifulSoup:
        return soup.find('div', {'class': 'pages'})

    def parse_pictures(self, soup: BeautifulSoup, url: URL):
        for image_container in _iter(self.get_pictures_containers(soup)):
            for image in _iter(image_container.find_all('img')):
                image_url=self.get_image_url(image.attrs['src'], url)
                filename=self.get_image_filename(image_url)
                self.add_picture(filename,image_url)

    def get_pictures_containers(self, soup:BeautifulSoup)->list:
        return soup.find_all('div', {'class': 'thumb_box'})

    def get_image_url(self, imagename:str, base_url:URL)->URL:
        return URL(imagename.replace('t.','.'), base_url=base_url)

    def get_image_filename(self,url:URL)->str:
        return url.get_path()+url.get().rpartition('/')[2]

    def parse_pictures_tags(self, soup:BeautifulSoup, url:URL):
        for tag_container in _iter(self.get_picture_tag_containers(soup)):
            for href in _iter(tag_container.find_all('a')):
                caption=''
                for s in href.stripped_strings:
                    caption+=s
                if caption is not None:
                    self.add_tag(caption, URL(href.attrs['href'], base_url=url))

    def get_picture_tag_containers(self, soup:BeautifulSoup)->list:
        return []

if __name__ == "__main__":
    pass