# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class TgpSite(BaseSiteParser):
    def parse_picture_thumbs(self, soup:BeautifulSoup, url:URL):
        for thumb_container in _iter(self.get_thumbs_containers(soup)):
            for thumbnail in _iter(self.get_thumbs_from_container(thumb_container)):
                self.parse_one_thumb(thumbnail,url)

    def get_thumbs_containers(self,soup:BeautifulSoup)->list:
        return soup.find_all('div',{'class':'thumbs'})

    def get_thumbs_from_container(self, container:BeautifulSoup)->list:
        return container.find_all('a')

    def parse_others(self, soup: BeautifulSoup, url: URL):
        for thumb in _iter(self.get_others_thumbs(soup)):
            self.parse_one_thumb(thumb, url)

    def get_others_thumbs(self, soup:BeautifulSoup)->list:
        return soup.find_all('a',{'class':['list','list_model']})

    def parse_one_thumb(self, thumbnail:BeautifulSoup, url:URL):
        # psp(thumbnail.prettify())
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
        for image_container in _iter(self.get_image_containers(soup)):
            for image in _iter(self.get_images_from_container(image_container)):
                image_url=self.get_image_url(image, url)
                filename=self.get_image_filename(image_url)
                self.add_picture(filename,image_url)

    def get_image_containers(self, soup:BeautifulSoup)->list:
        return soup.find_all('div', {'class': 'thumb_box'})

    def get_images_from_container(self,container: BeautifulSoup)->list:
        return container.find_all('img')

    def get_image_url(self, image:BeautifulSoup, base_url:URL)->URL:
        return URL(image.attrs['src'].replace('t.','.'), base_url=base_url)

    def get_image_filename(self,url:URL)->str:
        return url.get_path()+url.get().rpartition('/')[2]

    def parse_pictures_tags(self, soup:BeautifulSoup, url:URL):
        for tag_container in _iter(self.get_picture_tag_containers(soup)):
            for href in _iter(tag_container.find_all('a', href=True)):
                caption=collect_string(href).strip(' |')
                if caption:
                    self.add_tag(caption, URL(href.attrs['href'], base_url=url))

    def get_picture_tag_containers(self, soup:BeautifulSoup)->list:
        return []

if __name__ == "__main__":
    pass