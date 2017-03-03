# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5 import QtCore, QtGui, QtWidgets

from common.url import URL
from view.base_view import ThumbViewFromModelInterface, ViewManagerFromViewInterface

from view.widgets.thumb_widget import ThumbWidgetVS
from view.widgets.button_line import ButtonLine, TextButton

class ThumbView(ThumbViewFromModelInterface):
    def __init__(self,parent:QtWidgets.QWidget, name:str, view_manager:ViewManagerFromViewInterface):

        self.view_manager=view_manager

        self.tab = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        parent.addTab(self.tab, name)

        self.create_widgets()

    def create_widgets(self):
        self.thumbs=ThumbWidgetVS(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thumbs.sizePolicy().hasHeightForWidth())
        self.thumbs.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.thumbs)

        self.pages=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.pages)
        self.pages.hide()

    def add_thumb(self, picture_filename: str, href: URL, popup: str = '', labels=list):
        # print('Thumb filename:', picture_filename, 'added')
        # print('           url:', href)
        # print('         popup:', popup)
        # print('        labels:', labels)
        self.thumbs.add(picture_filename, lambda :self.view_manager.goto_url(href), popup, labels)

    def add_bottom_line(self, text:str, href:URL, tooltip:str='', menu=None, style:dict=None):
        button=TextButton(text,tooltip,lambda : self.view_manager.goto_url(href))
        button.set_menu(menu)
        button.set_button_style(style)
        self.pages.add_button(button)

if __name__ == "__main__":
    pass