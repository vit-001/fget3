# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from common.url import URL
from common.exception import AbstractMethodError
from controller.base_controller import ControllerFromViewInterface

class ThumbViewFromModelInterface:
    def clear(self):
        pass

    def re_init(self, title:str):
        pass

    def add_thumb(self,picture_filename:str, href:URL, popup:str='',labels=list):
        pass

    def add_bottom_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass

    def add_top_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass

    def add_mid_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        pass


class FullViewFromModelInterface:
    def play_video(self, name:str, url:URL):
        pass


class ViewManagerFromViewInterface:
    def goto_url(self, url:URL):
        pass

    def on_exit(self):
        pass


class ViewManagerFromModelInterface:
    def prepare_thumb_view(self, name:str)->ThumbViewFromModelInterface:
        raise(AbstractMethodError)

    def prepare_full_view(self, name:str)->FullViewFromModelInterface:
        raise (AbstractMethodError)

    def add_start_button(self, name:str, picture_filename:str, url:URL):
        print('Add start button:', name)


class ViewManagerFromControllerInterface:
    def create_main_window(self, controller: ControllerFromViewInterface):
        pass

if __name__ == "__main__":
    pass