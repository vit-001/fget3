# -*- coding: utf-8 -*-

__author__ = 'Nikitin'
from PyQt5.QtWidgets import QMenu

from data_format.error import AbstractMethodError
from data_format.url import URL
from interface.controller_interface import ControllerFromViewInterface
from interface.hystory_interface import HistoryFromViewInterface
from interface.view_interface import ViewFromModelInterface, ThumbViewFromModelInterface, FullViewFromModelInterface

class ViewManagerFromViewInterface:
    def add_keyboard_shortcut(self, window, shortcut='', on_pressed=lambda: None):
        pass

    def goto_url(self, url:URL, flags=None):
        pass

    def set_tab_text(self, view, text:str, tooltip:str=''):
        pass

    def on_thumb_tab_url_changed(self, view):
        pass

    def is_full_view_tab_active(self, full_view: FullViewFromModelInterface)->bool:
        return False

    def create_button_menu(self, parent, menu_items:dict)->QMenu:
        pass

    def on_exit(self):
        pass


class ViewManagerFromModelInterface:
    def new_thumb_view(self)-> ThumbViewFromModelInterface:
        raise(AbstractMethodError)

    def new_full_view(self)-> FullViewFromModelInterface:
        raise (AbstractMethodError)

    def on_thumb_history_changed(self, history:HistoryFromViewInterface):
        print('thumb history changed')

    def on_full_history_changed(self, history:HistoryFromViewInterface):
        print('full history changed')

    def add_start_button(self, name:str, picture_filename:str, url:URL, menu_items:dict=None):
        print('Add start button:', name)

class ViewManagerFromControllerInterface:
    def create_main_window(self, controller: ControllerFromViewInterface):
        pass

if __name__ == "__main__":
    pass