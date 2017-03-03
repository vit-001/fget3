# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5 import QtCore, QtGui, QtWidgets

from common.url import URL
from view.base_view import ThumbViewFromModelInterface, ViewManagerFromViewInterface

from view.widgets.thumb_widget import ThumbWidgetVS
from view.widgets.button_line import ButtonLine, TextButton

class ThumbView(ThumbViewFromModelInterface):
    def __init__(self, parent:QtWidgets.QWidget, title:str, view_manager:ViewManagerFromViewInterface):

        self.view_manager=view_manager
        self.title=title
        self.parent=parent

        self.tab = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.parent.addTab(self.tab, title)

        self.create_widgets()

    def create_widgets(self):
        self.top_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.top_line)
        self.top_line.hide()


        self.thumbs=ThumbWidgetVS(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thumbs.sizePolicy().hasHeightForWidth())
        self.thumbs.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.thumbs)

        self.mid_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.mid_line)
        self.mid_line.hide()

        self.bottom_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.bottom_line)
        self.bottom_line.hide()

    def clear(self):
        self.thumbs.clear()
        self.top_line.clear()
        self.mid_line.clear()
        self.bottom_line.clear()


    def re_init(self, title: str):
        self.title=title
        index=self.parent.indexOf(self.tab)
        self.parent.setTabText(index, self.title)

        self.clear()


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
        self.bottom_line.add_button(button)

    def add_mid_line(self, text:str, href:URL, tooltip:str='', menu=None, style:dict=None):
        button=TextButton(text,tooltip,lambda : self.view_manager.goto_url(href))
        button.set_menu(menu)
        button.set_button_style(style)
        self.mid_line.add_button(button)

    def add_top_line(self, text:str, href:URL, tooltip:str='', menu=None, style:dict=None):
        button=TextButton(text,tooltip,lambda : self.view_manager.goto_url(href))
        button.set_menu(menu)
        button.set_button_style(style)
        self.top_line.add_button(button)

if __name__ == "__main__":
    pass