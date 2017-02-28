# -*- coding: utf-8 -*-
__author__ = 'Vit'

from bs4 import BeautifulSoup

from common.url import URL
from model.loader.base_loader import FLData
from model.base_model import AbstractModelFromSiteInterface
from view.base_view import AbstractViewFromModelInterface, AbstractThumbViewFromModelInterface

class AbstractSite:

    @staticmethod
    def create_start_button(view:AbstractViewFromModelInterface):
        pass

    @staticmethod
    def can_accept_url(url:URL)->bool:
        return False

    def goto_url(self, url:URL, **options):
        pass


class BaseSite(AbstractSite):
    def __init__(self, model:AbstractModelFromSiteInterface):
        self.model=model

    def goto_url(self, url: URL, **options):
        print('Goto url:', url)
        loader=self.model.loader
        filedata=FLData(url,'')

        loader.start_load_file(filedata, self.on_load_url)

    def on_load_url(self, filedata:FLData):
        print(filedata.url, 'loaded')
        soup=BeautifulSoup(filedata.text,'html.parser')
        if not self.parse_soup(soup, filedata.url):
            print('Parsing has no result')

    def parse_soup(self, soup:BeautifulSoup, url:URL)->bool:
        if self.parse_video(soup, url):
            self.parse_video_tags(soup, url)
            return True
        if self.parse_pictures(soup, url):
            self.parse_pictures_tags(soup, url)
            return True
        if self.parse_thumbs(soup, url) or self.parse_others(soup, url):
            self.parse_thumbs_tags(soup, url)
            self.parse_pagination(soup, url)
            return True
        return False

    def parse_thumbs(self, soup: BeautifulSoup, url: URL)->bool:
        return False

    def parse_others(self, soup: BeautifulSoup, url: URL)->bool:
        return False

    def parse_video(self, soup: BeautifulSoup, url: URL)->bool:
        return False

    def parse_pictures(self, soup: BeautifulSoup, url: URL)->bool:
        return False

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container is not None:
            for page in container.find_all('a', {'href': True}):
                # psp(page.prettify())
                if page.string is not None and page.string.isdigit():
                    # result.add_page(ControlInfo(page.string, URL(page.attrs['href'], base_url=base_url)))
                    print('Add page',page.string, URL(page.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return None

    def parse_thumbs_tags(self, soup: BeautifulSoup, base_url: URL):
        return

    def parse_video_tags(self, soup: BeautifulSoup, base_url: URL):
        return

    def parse_pictures_tags(self, soup: BeautifulSoup, base_url: URL):
        return

    def prepare_thumb_view(self)->AbstractThumbViewFromModelInterface:
        self.view=self.model.view.prepare_thumb_view()
        return self.view


if __name__ == "__main__":
    pass