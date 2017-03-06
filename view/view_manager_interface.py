# -*- coding: utf-8 -*-

__author__ = 'Nikitin'
from PyQt5.QtWidgets import QMenu

from common.exception import AbstractMethodError
from common.url import URL
from controller.base_controller import ControllerFromViewInterface
from model.history_model.hystory_interface import HistoryFromViewInterface

from view.view_interface import ViewFromModelInterface

class ViewManagerFromViewInterface:
    def add_keyboard_shortcut(self, window, shortcut='', on_pressed=lambda: None):
        pass

    def goto_url(self, url:URL, context=None):
        pass

    def set_tab_text(self, view, text:str, tooltip:str=''):
        pass

    def is_full_view_tab_active(self, full_view: ViewFromModelInterface)->bool:
        return False

    def create_button_menu(self, parent, menu_items:dict)->QMenu:
        pass

    def on_exit(self):
        pass


class ViewManagerFromModelInterface:
    def prepare_thumb_view(self)-> ViewFromModelInterface:
        raise(AbstractMethodError)

    def prepare_full_view(self)-> ViewFromModelInterface:
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