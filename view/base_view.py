# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

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


if __name__ == "__main__":
    pass