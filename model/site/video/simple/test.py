# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
# from common.util import _iter, quotes, pretty, psp, collect_string_to_array

import json

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class TestSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('google.com')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        view.add_start_button(picture_filename='model/site/resource/test.png',
                              url=URL("http://www.google.com"))

    def get_shrink_name(self):
        return 'TT'

    def parse_video(self, soup: BeautifulSoup, url: URL):
        t = 'https://cdn.its.porn/63000/63020/63020_vs.mp4?cdn_hash=42dd197f4048e0f5896c41c941ce5331&cdn_creation_time=1629790560&cdn_ttl=14400*'
        referrer=URL('https://fr.xhamster.com')
        self.add_video('DEFAULT', URL(t))

if __name__ == "__main__":
    pass