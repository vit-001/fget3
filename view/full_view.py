# -*- coding: utf-8 -*-
__author__ = 'Vit'
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QSizePolicy

from common.url import URL

from view.base_view import FullViewFromModelInterface, ViewManagerFromViewInterface
from view.widgets.button_line import ButtonLine
from view.widgets.video_player_widget import VideoPlayerWidget

class FullView(FullViewFromModelInterface):
    def __init__(self, parent:QWidget, title:str, view_manager:ViewManagerFromViewInterface):

        self.view_manager=view_manager
        self.title=title
        self.parent=parent
        self.current=False

        self.tab = QWidget()
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.parent.addTab(self.tab, title)

        self.create_widgets()

    def create_widgets(self):
        self.video_player = VideoPlayerWidget(self.tab)
        self.verticalLayout.addWidget(self.video_player)
        self.video_player.hide()

        self.bottom_line=ButtonLine(self.tab)
        self.verticalLayout.addWidget(self.bottom_line)
        self.bottom_line.hide()

    def play_video(self, name:str, url:URL):
        self.video_player.show()
        self.video_player.play_url(url)

    def pause(self):
        self.video_player.pause()

    def resume(self):
        self.video_player.resume()

if __name__ == "__main__":
    pass