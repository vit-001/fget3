# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from common.util import _iter, quotes, psp, collect_string

from common.util import _iter, quotes
from data_format.url import URL
from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.picture.base_of_tgp import TgpSite


class BabesandbitchesSite(TgpSite):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('babesandbitches.net/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        view.add_start_button(picture_filename='model/site/resource/picture/babesandbithes.png',
                              url=URL("http://www.babesandbitches.net/galleries/"))

    def get_shrink_name(self):
        return 'BB'

    def get_thumbs_containers(self, soup: BeautifulSoup) -> list:
        return soup.find_all('div', id='inner-center-content')

    def get_thumbs_from_container(self, container: BeautifulSoup) -> list:
        return container.find_all('div',{'class':'thumb-wrap'})

    def parse_one_thumb(self, thumbnail:BeautifulSoup, url:URL):
        href = URL(thumbnail.a.attrs['href'],base_url=url)
        description = thumbnail.img.attrs.get('alt', '')
        thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
        self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                       labels=[{'text': description, 'align': 'bottom center'}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        container=soup.find('ul',id='nav-ul')
        if container:
            for href in _iter(container.find_all('a', href=lambda x:'/?category=' in str(x))):
                self.add_tag(href.string, URL(href.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup)->BeautifulSoup:
        return soup.find('div', {'class':'pager'})

    def get_image_containers(self, soup: BeautifulSoup) -> list:
        return soup.find_all('div', id='gallery-holder')

    def get_images_from_container(self,container: BeautifulSoup):
        return container.find_all('img', {'class':'gallery-image'})

    def get_image_url(self, image:BeautifulSoup, base_url:URL)->URL:
        return URL(image.attrs['src'].replace('tn_',''), base_url=base_url)

    def get_picture_tag_containers(self, soup:BeautifulSoup)->list:
        return soup.find_all('div', id='gallery-model')


if __name__ == "__main__":
    pass