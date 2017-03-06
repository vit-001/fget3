# -*- coding: utf-8 -*-
__author__ = 'Vit'

from PyQt5.QtWidgets import QWidget

from common.url import URL




class ViewFromModelInterface:
    def get_rot_widget(self)->QWidget:
        pass

    def set_title(self, title:str, tooltip=''):
        pass

    def add_to_bottom_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass

    def add_to_top_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass

    def add_to_mid_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass

    def clear(self):
        pass

# class ThumbViewFromModelInterface(ViewFromModelInterface):
#
#
#     def add_thumb(self,picture_filename:str, href:URL, popup:str='',labels=list):
#         pass
#
#
# class FullViewFromModelInterface(ViewFromModelInterface):
#     def set_video_list(self, list_of_dict:list, default:int):
#         pass