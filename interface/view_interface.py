# -*- coding: utf-8 -*-
__author__ = 'Vit'

from data_format.url import URL

class ViewFromModelInterface:
    def set_url(self, url:URL):
        pass

    def set_title(self, title:str, tooltip=''):
        pass

    def add_to_bottom_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass

    def add_to_top_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass

    def add_to_mid_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass

    def subscribe_to_history_event(self, handler=lambda dict:None):
        pass

    def re_init(self, flags):
        pass

class ThumbViewFromModelInterface(ViewFromModelInterface):
    def add_thumb(self,picture_filename:str, href:URL, popup:str='',labels=list):
        pass


class FullViewFromModelInterface(ViewFromModelInterface):
    def set_video_list(self, list_of_dict:list, default:int):
        pass

    def add_picture(self, filename):
        print(filename)
        pass

