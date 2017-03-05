# -*- coding: utf-8 -*-
__author__ = 'Vit'
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QSizePolicy
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt

from common.url import URL

from view.view_manager_interface import ViewManagerFromViewInterface
from view.view_interface import FullViewFromModelInterface
from view.widgets.button_line import ButtonLine, TextButton
from view.widgets.video_player_widget import VideoPlayerWidget


class FullView(FullViewFromModelInterface):
    def __init__(self, parent:QWidget, view_manager:ViewManagerFromViewInterface):

        self.view_manager=view_manager
        self.title=''
        self.parent=parent
        self.current=False

        self.tab = QWidget()
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.parent.addTab(self.tab, self.title)

        self.create_widgets()

        self.little_forward=self.video_player.little_forward

    def create_widgets(self):
        self.top_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.top_line)
        self.top_line.hide()

        self.video_player = VideoPlayerWidget(self.tab)
        self.verticalLayout.addWidget(self.video_player)
        self.video_player.hide()

        self.mid_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.mid_line)
        self.mid_line.hide()

        self.bottom_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.bottom_line)
        self.bottom_line.hide()

    def set_title(self, title:str, tooltip=''):
        self.view_manager.set_tab_text(self,title,tooltip)

    def set_video_list(self, list_of_dict:list, default:int):
        self.video_player.show()
        self.video_player.set_url_list(list_of_dict,default)
        if self.view_manager.is_full_view_tab_active(self):
            self.video_player.play()

    def add_to_bottom_line(self, text:str, href:URL, tooltip:str= '', menu=None, style:dict=None):
        button=TextButton(text,tooltip,lambda : self.view_manager.goto_url(href))
        button.set_menu(self.view_manager.create_button_menu(self.tab, menu))
        button.set_button_style(style)
        self.bottom_line.add_button(button)

    def add_to_mid_line(self, text:str, href:URL, tooltip:str= '', menu=None, style:dict=None):
        button=TextButton(text,tooltip,lambda : self.view_manager.goto_url(href))
        button.set_menu(self.view_manager.create_button_menu(self.tab, menu))
        button.set_button_style(style)
        self.mid_line.add_button(button)

    def add_to_top_line(self, text:str, href:URL, tooltip:str= '', menu=None, style:dict=None):
        button=TextButton(text,tooltip,lambda : self.view_manager.goto_url(href))
        button.set_menu(self.view_manager.create_button_menu(self.tab, menu))
        button.set_button_style(style)
        self.top_line.add_button(button)

    def get_rot_widget(self) -> QWidget:
        return self.tab

    def mute(self, on:bool):
        self.video_player.mute(on)

    def is_muted(self)->bool:
        return self.video_player.is_muted()

    def set_volume(self, volume:int):
        self.video_player.set_volume(volume)

    def get_volume(self)->int:
        return self.video_player.get_volume()

    def pause(self):
        self.video_player.pause()

    def play(self, muted:bool, volume:int):
        self.video_player.play()
        self.video_player.mute(muted)
        self.video_player.set_volume(volume)

    def destroy(self):
        self.video_player.destroy()
        self.bottom_line.destroy()
        self.tab.destroy()

if __name__ == "__main__":
    pass