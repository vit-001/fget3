# -*- coding: utf-8 -*-
__author__ = 'Vit'
from PyQt6.QtWidgets import QWidget, QLabel, QFrame, QHBoxLayout, QToolButton, QSizePolicy
from PyQt6.QtGui import QPixmap, QPicture, QIcon
from PyQt6.QtCore import Qt

from data_format.history_data import HistoryData

from view_qt6.full_view.base_full_view import BaseFullView
from view_qt6.widgets.video_player_widget import VideoPlayerWidget
from view_qt6.widgets.picture_browser import PictureBrowser


class FullView(BaseFullView):
    def get_main_content(self, parent: QWidget) -> QWidget:
        self.parent=parent
        self.frame=QFrame(self.parent)

        layout=QHBoxLayout(self.frame)
        # layout.setAlignment(Qt.AlignCenter)

        self.video_player = VideoPlayerWidget(self.frame)
        self.picture=PictureBrowser(self.parent, lambda index:self.progress.set_value('current pix', index+1))
        self.video_player.set_error_handler(self.on_error)

        layout.addWidget(self.video_player)
        self.picture.hide()
        self.video_player.hide()
        return self.frame

    def binding(self):
        self.little_forward = self.video_player.little_forward

    def prepare_content(self):
        self.picture.re_init()
        self.video_player.stop()
        self.video_player.hide()
        self.picture.hide()
        self.progress.add_progress('loaded pix',Qt.GlobalColor.darkBlue)
        self.progress.add_progress('current pix', Qt.GlobalColor.red)
        self.progress.set_autohide_bar_name('loaded pix')

    def prepare_content_to_close(self):
        self.picture.re_init()
        self.video_player.stop()

    def set_title(self, title:str, tooltip=''):
        self.view_manager.set_tab_text(self,title,tooltip)

    def set_video_list(self, list_of_dict:list, default:int):
        self.video_player.show()
        self.video_player.set_url_list(list_of_dict,default)
        if self.view_manager.is_full_view_tab_active(self):
            self.video_player.play()

    def add_picture(self, filename):
        self.picture.show()
        self.picture.add_picture(filename)
        self.resize_event()
        self.progress.set_value('loaded pix', self.picture.count)

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

    def history_event(self):
        history_data=HistoryData(self.url)
        self.history_handler(history_data)

    def resize_event(self):
        self.picture.setFixedSize(self.frame.size())
        self.picture.show_current_picture()

    def destroy(self):
        self.history_event()
        self.video_player.destroy()
        self.bottom_line.destroy()
        self.tab.destroy()

if __name__ == "__main__":
    pass