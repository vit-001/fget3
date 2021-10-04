# -*- coding: utf-8 -*-
__author__ = 'Vit'

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from data_format.error import AbstractMethodError
from data_format.url import URL

from common.setting import Setting

from interface.view_interface import ThumbViewFromModelInterface,FullViewFromModelInterface
from interface.view_manager_interface import ViewManagerFromViewInterface

from view_qt5.widgets.button_line import TextButton, ButtonLine
from view_qt5.widgets.progress_line import ProgressHLine


class BaseView(ThumbViewFromModelInterface,FullViewFromModelInterface):
    def __init__(self, parent:QWidget,view_manager:ViewManagerFromViewInterface):
        self.view_manager=view_manager
        self.title = ''
        self.parent = parent
        self.flags=None

        self.url=URL()
        self.history_handler=lambda dict:None
        self.no_history = True
        self.on_stop=lambda:None

        self.tab = QWidget()
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.parent.addTab(self.tab, self.title)

        self.create_widgets()
        self.binding()

        # self.content_prepare()

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

        self.progress=ProgressHLine(self.tab)
        self.verticalLayout.addWidget(self.progress)
        self.progress.show()

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

    def on_error(self, error_string: str):
        Setting.log.write(error_string)

    def subscribe_to_history_event(self, handler=lambda dict: None):
        self.history_handler=handler

    def prepare(self, url:URL, title:str, tooltip='',on_stop=lambda:None, flags:dict=None, max_progress:int=0):
        self.on_stop()
        self.on_stop=on_stop

        self.flags=flags

        if self.flags:
            self.no_history=flags.get('no_history', False)
        if not self.no_history:
            self.history_event()
        self.no_history=False

        self.set_url(url)
        self.set_title(title,tooltip)

        self.progress.reset()
        self.progress.set_max_value(max_progress)
        self.prepare_content()
        self.top_line.clear()
        self.mid_line.clear()
        self.bottom_line.clear()

    def prepare_to_close(self):
        self.on_stop()
        self.history_event()
        self.prepare_content_to_close()
        self.top_line.clear()
        self.mid_line.clear()
        self.bottom_line.clear()

    def set_url(self, url:URL):
        self.url=url

    def set_title(self, title:str, tooltip=''):
        pass

    def prepare_content(self):
        pass

    def prepare_content_to_close(self):
        pass

    def history_event(self):
        pass

    def resize_event(self):
        pass

    def add_to_bottom_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        self.add_button(self.bottom_line, text, href, tooltip, menu, style)
        # button = TextButton(text, tooltip, lambda: self.view_manager.goto_url(href))
        # button.set_menu(self.view_manager.create_button_menu(self.tab, menu))
        # button.set_button_style(style)
        # self.bottom_line.add_button(button)

    def add_to_mid_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        self.add_button(self.mid_line, text, href, tooltip, menu, style)
        # button = TextButton(text, tooltip, lambda: self.view_manager.goto_url(href))
        # button.set_menu(self.view_manager.create_button_menu(self.tab, menu))
        # button.set_button_style(style)
        # self.mid_line.add_button(button)

    def add_to_top_line(self, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        self.add_button(self.top_line,text,href,tooltip,menu,style)
        # button = TextButton(text, tooltip, lambda: self.view_manager.goto_url(href))
        # button.set_menu(self.view_manager.create_button_menu(self.tab, menu))
        # button.set_button_style(style)
        # self.top_line.add_button(button)

    def add_button(self, destination:ButtonLine, text: str, href: URL, tooltip: str = '', menu=None, style: dict = None):
        button = TextButton(text, tooltip, lambda: self.view_manager.goto_url(href))
        button.set_menu(self.view_manager.create_button_menu(self.tab, menu))
        button.set_button_style(style)
        destination.add_button(button)
        # self.resize_event()


if __name__ == "__main__":
    pass