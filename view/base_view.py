# -*- coding: utf-8 -*-
__author__ = 'Vit'

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from data_format.error import AbstractMethodError
from data_format.url import URL

from interface.view_interface import ThumbViewFromModelInterface,FullViewFromModelInterface
from interface.view_manager_interface import ViewManagerFromViewInterface

from view.widgets.button_line import TextButton, ButtonLine


class BaseView(ThumbViewFromModelInterface,FullViewFromModelInterface):
    def __init__(self, parent:QWidget,view_manager:ViewManagerFromViewInterface, flags):
        self.view_manager=view_manager
        self.title = ''
        self.parent = parent
        self.flags=flags

        self.url=URL()
        self.history_handler=lambda dict:None

        self.tab = QWidget()
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.parent.addTab(self.tab, self.title)

        self.create_widgets()
        self.binding()

        self.content_re_init()

    def create_widgets(self):
        self.top_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.top_line)
        self.top_line.hide()

        content=self.get_main_content(self.tab)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(content.sizePolicy().hasHeightForWidth())
        content.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(content)

        self.mid_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.mid_line)
        self.mid_line.hide()

        self.bottom_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.bottom_line)
        self.bottom_line.hide()

    def get_main_content(self, parent:QWidget)->QWidget:
        raise(AbstractMethodError)

    def binding(self):
        pass

    def subscribe_to_history_event(self, handler=lambda dict: None):
        self.history_handler=handler

    def set_url(self, url:URL):
        self.url=url

    def re_init(self, flags):
        self.flags=flags

        no_history=False
        if self.flags:
            no_history=flags.get('no_history', False)

        if not no_history:
            self.history_event()
        self.content_re_init()
        self.top_line.clear()
        self.mid_line.clear()
        self.bottom_line.clear()

    def content_re_init(self):
        pass

    def history_event(self):
        pass

    def add_to_bottom_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        button = TextButton(text, tooltip, lambda: self.view_manager.goto_url(href))
        button.set_menu(self.view_manager.create_button_menu(self.tab, menu))
        button.set_button_style(style)
        self.bottom_line.add_button(button)

    def add_to_mid_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        button = TextButton(text, tooltip, lambda: self.view_manager.goto_url(href))
        button.set_menu(self.view_manager.create_button_menu(self.tab, menu))
        button.set_button_style(style)
        self.mid_line.add_button(button)

    def add_to_top_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        button = TextButton(text, tooltip, lambda: self.view_manager.goto_url(href))
        button.set_menu(self.view_manager.create_button_menu(self.tab, menu))
        button.set_button_style(style)
        self.top_line.add_button(button)

if __name__ == "__main__":
    pass