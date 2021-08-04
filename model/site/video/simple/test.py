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
        t = 'https://19-17.b.cdn13.com/020/936/600/720p.h264.mp4?cdn_creation_time=1628092800&cdn_ttl=14400&cdn_bw=228k&cdn_bw_fs=2208k&cdn_cv_data=217.66.159.144-dvp&cdn_hash=d9e76e7a658f93ea1a736e951e2a9dcb*'
        referrer=URL('https://fr.xhamster.com')
        self.add_video('DEFAULT', URL(t))

if __name__ == "__main__":
    pass