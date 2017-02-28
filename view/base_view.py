# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from common.url import URL

class AbstractThumbViewFromModelInterface:
    pass

class AbstractVideoViewFromModelInterface:
    pass

class AbstractPictureViewFromModelInterface:
    pass

class AbstractViewFromModelInterface:
    def prepare_thumb_view(self, new=False)->AbstractThumbViewFromModelInterface:
        pass

    def prepare_video_view(self, new=False)->AbstractVideoViewFromModelInterface:
        pass

    def prepare_picture_view(self, new=False)->AbstractPictureViewFromModelInterface:
        pass

    def add_start_button(self, name:str, picture_filename:str, url:URL):
        pass

if __name__ == "__main__":
    pass