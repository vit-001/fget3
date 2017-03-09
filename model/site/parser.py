# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from common.util import _iter
from data_format.url import URL
from model.site.base_site import BaseSite


class BaseSiteParser(BaseSite):
    def parse_soup(self, soup:BeautifulSoup, url:URL):
        self.parse_video(soup, url)
        if self.is_video:
            self.parse_video_tags(soup, url)
            self.title=self.parse_video_title(soup,url)
            self.generate_video_view()
            return
        self.parse_pictures(soup, url)
        if self.is_pictures:
            self.parse_pictures_tags(soup, url)
            self.title=self.parse_pictures_title(soup,url)
            self.generate_pictures_view()
            return
        self.parse_thumbs(soup, url)
        if self.is_no_result:
            self.parse_others(soup, url)
        if self.is_thumbs:
            self.parse_thumbs_tags(soup, url)
            self.parse_pagination(soup, url)
            self.title=self.parse_thumb_title(soup,url)
            self.generate_thumb_view()

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        self.parse_video_thumbs(soup,url)
        if self.is_thumbs:
            return
        self.parse_picture_thumbs(soup,url)

    def parse_video_thumbs(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_picture_thumbs(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_video(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_pictures(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_others(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container:
            for page in _iter(container.find_all('a', {'href': True})):
                if page.string and page.string.isdigit():
                    self.add_page(page.string, URL(page.attrs['href'], base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def get_pagination_container(self, soup:BeautifulSoup)->BeautifulSoup:
        return None

    def parse_thumbs_tags(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_video_tags(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_pictures_tags(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_thumb_title(self, soup:BeautifulSoup, url:URL)->str:
        return 'No title'

    def parse_video_title(self, soup:BeautifulSoup, url:URL)->str:
        return 'No title'

    def parse_pictures_title(self, soup:BeautifulSoup, url:URL)->str:
        return 'No title'


if __name__ == "__main__":
    pass