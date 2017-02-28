# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from common.url import URL
from common.exception import AbstractMethodError
from controller.base_controller import ControllerFromViewInterface

class ThumbViewFromModelInterface:
    def add_thumb(self,thumb_url:URL, href:URL, popup:str='',labels=list):
        pass

class VideoViewFromModelInterface:
    pass

class PictureViewFromModelInterface:
    pass

class ViewFromModelInterface:
    def prepare_thumb_view(self, new=False)->ThumbViewFromModelInterface:
        raise(AbstractMethodError)

    def prepare_video_view(self, new=False)->VideoViewFromModelInterface:
        raise (AbstractMethodError)

    def prepare_picture_view(self, new=False)->PictureViewFromModelInterface:
        raise (AbstractMethodError)

    def add_start_button(self, name:str, picture_filename:str, url:URL):
        print('Add start button:', name)


class ViewFromControllerInterface:
    def register_controller(self, controller: ControllerFromViewInterface):
        pass

if __name__ == "__main__":
    pass