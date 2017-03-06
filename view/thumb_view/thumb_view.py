# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from common.url import URL
from view.view_manager_interface import ViewManagerFromViewInterface
from view.base_view import BaseView

from view.widgets.thumb_widget import ThumbWidgetVS
from view.widgets.button_line import ButtonLine, TextButton

class ThumbView(BaseView):
    def get_main_content(self, parent:QWidget)->QWidget:
        self.thumbs=ThumbWidgetVS(parent)
        return self.thumbs

    def content_clear(self):
        self.thumbs.clear()

    def set_title(self, title: str, tooltip=''):
        index=self.parent.indexOf(self.tab)
        self.parent.setTabText(index, title)
        self.parent.setTabToolTip(index, tooltip)

    def add_thumb(self, picture_filename: str, href: URL, popup: str = '', labels=list):
        # print('Thumb filename:', picture_filename, 'added')
        # print('           url:', href)
        # print('         popup:', popup)
        # print('        labels:', labels)
        self.thumbs.add(picture_filename, lambda :self.view_manager.goto_url(href), popup, labels)



if __name__ == "__main__":
    pass