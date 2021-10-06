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
        t = 'https://hls.youngpornvideos.com/_hls/flv/0550/282395/,default,mobile,480p,720p,1080p,.mp4.urlset/master.m3u8?validfrom=1633512062&validto=1633519262&hash=TfKdaSvxxBntA%2BlKXLPP%2FXkGiwI%3D'
        referrer=URL('https://fr.xhamster.com')
        self.add_video('DEFAULT', URL(t, redirect=False))

if __name__ == "__main__":
    pass