# -*- coding: utf-8 -*-
__author__ = 'Vit'
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QSizePolicy

from common.url import URL

from view.view_manager_interface import ViewManagerFromViewInterface
from view.view_interface import FullViewFromModelInterface
from view.widgets.button_line import ButtonLine
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
        self.video_player = VideoPlayerWidget(self.tab)
        self.verticalLayout.addWidget(self.video_player)
        self.video_player.hide()

        self.bottom_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.bottom_line)
        self.bottom_line.hide()

    def set_title(self, title:str, tooltip=''):
        self.view_manager.set_tab_text(self,title,tooltip)

    def set_video(self, url:URL):
        self.video_player.show()
        self.video_player.set_url(url)
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