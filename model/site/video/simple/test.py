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
        t = 'https://ev-ph.rdtcdn.com/videos/202106/23/390077411/720P_4000K_390077411.mp4?validfrom=1628778400&validto=1628785600&rate=281k&burst=1400k&hash=sZS2gX%2BJMGXqtEITnrBdpOq%2BOOE%3D*'
        referrer=URL('https://fr.xhamster.com')
        self.add_video('DEFAULT', URL(t))

if __name__ == "__main__":
    pass