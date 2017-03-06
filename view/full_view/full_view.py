# -*- coding: utf-8 -*-
__author__ = 'Vit'
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QSizePolicy
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt

from common.url import URL

# from view.view_manager_interface import ViewManagerFromViewInterface
# from view.view_interface import FullViewFromModelInterface
from view.full_view.base_full_view import BaseFullView
from view.widgets.button_line import ButtonLine, TextButton
from view.widgets.video_player_widget import VideoPlayerWidget


class FullView(BaseFullView):
    def get_main_content(self, parent: QWidget) -> QWidget:
        self.video_player = VideoPlayerWidget(parent)
        return self.video_player

    def binding(self):
        self.little_forward = self.video_player.little_forward

    def content_clear(self):
        super().content_clear()

    def set_title(self, title:str, tooltip=''):
        self.view_manager.set_tab_text(self,title,tooltip)

    def set_video_list(self, list_of_dict:list, default:int):
        self.video_player.show()
        self.video_player.set_url_list(list_of_dict,default)
        if self.view_manager.is_full_view_tab_active(self):
            self.video_player.play()

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