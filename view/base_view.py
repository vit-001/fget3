# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from common.url import URL
from common.exception import AbstractMethodError

class AbstractThumbViewFromModelInterface:
    def add_thumb(self,thumb_url:URL, href:URL, popup:str='',labels=list):
        print('Add thumb:', thumb_url,href,popup,labels)

class AbstractVideoViewFromModelInterface:
    pass

class AbstractPictureViewFromModelInterface:
    pass

class AbstractViewFromModelInterface:
    def prepare_thumb_view(self, new=False)->AbstractThumbViewFromModelInterface:
        raise(AbstractMethodError)

    def prepare_video_view(self, new=False)->AbstractVideoViewFromModelInterface:
        raise (AbstractMethodError)

    def prepare_picture_view(self, new=False)->AbstractPictureViewFromModelInterface:
        raise (AbstractMethodError)

    def add_start_button(self, name:str, picture_filename:str, url:URL):
        print('Add start button:', name)


class AbsractViewFromControllerInterface:
    pass

if __name__ == "__main__":
    pass