# -*- coding: utf-8 -*-
__author__ = 'Vit'

from common.url import URL

class ViewFromModelInterface:
    def set_title(self, title:str, tooltip=''):
        pass


class ThumbViewFromModelInterface(ViewFromModelInterface):
    def clear(self):
        pass

    def add_thumb(self,picture_filename:str, href:URL, popup:str='',labels=list):
        pass

    def add_to_bottom_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass

    def add_to_top_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass

    def add_to_mid_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass


class FullViewFromModelInterface(ViewFromModelInterface):
    def set_video(self, url:URL):
        pass