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
        t = 'http://video-hw.xvideos-cdn.com/videos/mp4/9/1/a/xvideos.com_91a2212955b408d0f9551ebabf1ea91a.mp4?e=1626344676&ri=1024&rs=85&h=ef86eebae8432b98e7972fa062f44c8a*'
        # referrer=URL('https://bdsmstreak.com/')
        self.add_video('DEFAULT', URL(t))

if __name__ == "__main__":
    pass