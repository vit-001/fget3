# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from common.util import _iter, quotes
from data_format.url import URL
from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.picture.base_of_tgp import TgpSite


class VibrapornSite(TgpSite):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('vibraporn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        view.add_start_button(picture_filename='model/site/resource/picture/vibraporn.png',
                              url=URL("http://www.vibraporn.com/galleries/"))

    def get_shrink_name(self):
        return 'VP'

    def get_thumbs_containers(self, soup: BeautifulSoup) -> list:
        return soup.find_all('div', id='plugs')

    def get_pagination_container(self, soup: BeautifulSoup)->BeautifulSoup:
        return soup.find('div', id='nav')

    def get_image_containers(self, soup: BeautifulSoup) -> list:
        return soup.find_all('div',{'class':'gallery_w'})

    def get_images_from_container(self,container: BeautifulSoup):
        return container.find_all('img', {'class':'thumb_w'})

    def get_image_url(self, image:BeautifulSoup, base_url:URL)->URL:
        return URL(image.attrs['src'].replace('tn_',''), base_url=base_url)

    def get_picture_tag_containers(self, soup:BeautifulSoup)->list:
        return soup.find_all('div',{'class':'tags'})


if __name__ == "__main__":
    pass