# -*- coding: utf-8 -*-
__author__ = 'Vit'
import os

from PyQt5.QtCore import QUrl, QPoint, QRect, QSize, Qt, QEventLoop
from PyQt5.QtNetwork import QNetworkRequest, QNetworkProxy
from PyQt5.QtGui import QPixmap, QIcon, QPalette
from PyQt5.QtWidgets import QWidget, QSizePolicy, QMenu, QAction
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from common.url import URL
from common.util import get_menu_handler

from view.qt_ui.ui_video_player_widget import Ui_VideoPlayerWidget


class VideoPlayerWidget(QWidget):
    def __init__(self, QWidget_parent=None, Qt_WindowFlags_flags=0):
        QWidget.__init__(self, QWidget_parent)

        self.ui=Ui_VideoPlayerWidget()
        savecwd = os.getcwd()
        os.chdir('view/qt_ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)

        self.duration=0
        self.urls=list()
        self.default=-1
        self.saved_position=None

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.media_player_widget = QVideoWidget(self.ui.top_frame)
        self.ui.top_frame_layout.addWidget(self.media_player_widget)
        self.media_player.setVideoOutput(self.media_player_widget)
        self.media_player_widget.show()

        self.media_player.bufferStatusChanged.connect(lambda x:self.ui.buffer.setValue(x))
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)

        self.ui.bn_play.clicked.connect(self.media_player.play)
        self.ui.bn_pause.clicked.connect(self.media_player.pause)
        self.ui.bn_stop.clicked.connect(self.media_player.stop)
        self.ui.bn_mute.clicked.connect(self.media_player.setMuted)
        self.ui.progress.sliderMoved.connect(self.media_player.setPosition)
        self.ui.volume.valueChanged.connect(self.media_player.setVolume)

    def set_url_list(self, list_of_dict:list, default:int):
        self.urls=list_of_dict
        self.default=default
        self.set_url(self.urls[self.default]['url'])

        menu = QMenu(self)
        for item in self.urls:
            menu_action = QAction(item['text'], self, triggered=get_menu_handler(self.re_open,item['url']))
            menu.addAction(menu_action)
        self.ui.bn_quality.setMenu(menu)

    def re_open(self, url:URL):
        self.saved_position=self.media_player.position()
        self.set_url(url)
        self.media_player.play()

    def set_url(self, url:URL):
        request = QNetworkRequest(QUrl(url.get()))

        # todo: сделать добавление cookie и подготовку proxу

        self.media_player.setMedia(QMediaContent(request))

        # print(self.media_player.media().canonicalRequest())

    def media_status_changed(self, media_status):
        if media_status == QMediaPlayer.BufferedMedia:
            if self.saved_position:
                self.media_player.setPosition(self.saved_position)
                self.saved_position = None

    def positionChanged(self, position):
        def time_format(ms):
            dur = ms // 1000
            hours=dur // 3600
            minutes =  dur // 60 - hours*60
            secundes = dur - minutes * 60- hours*3600
            if hours==0:
                return '%2d:%02d' % (minutes, secundes)
            else:
                return '%d:%02d:%02d' % (hours, minutes, secundes)
        self.ui.progress.setValue(position)
        self.ui.lb_time.setText(time_format(position) + ' / ' + time_format(self.duration))

    def durationChanged(self, duration):
        self.ui.progress.setRange(0, duration)
        self.duration = duration

    def little_forward(self, second:int):
        current_position=self.media_player.position()
        new_position=current_position + second*1000
        if new_position < self.duration:
            self.media_player.setPosition(new_position)

    def play(self):
        self.media_player.play()

    def pause(self):
        self.media_player.pause()

    def set_volume(self, volume:int):
        self.ui.volume.setValue(volume)
        self.media_player.setVolume(volume)

    def get_volume(self)->int:
        return self.ui.volume.value()

    def mute(self, on:bool):
        self.media_player.setMuted(on)
        self.ui.bn_mute.setChecked(on)

    def is_muted(self):
        return self.ui.bn_mute.isChecked()

    def destroy(self, bool_destroyWindow=True, bool_destroySubWindows=True):
        self.media_player.deleteLater()
        super().destroy(bool_destroyWindow, bool_destroySubWindows)


if __name__ == "__main__":
    pass