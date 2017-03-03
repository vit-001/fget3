# -*- coding: utf-8 -*-
__author__ = 'Vit'
import os

from PyQt5.QtCore import QUrl, QPoint, QRect, QSize, Qt, QEventLoop
from PyQt5.QtNetwork import QNetworkRequest, QNetworkProxy
from PyQt5.QtGui import QPixmap, QIcon, QPalette
from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from common.url import URL

from view.qt_ui.ui_video_player_widget import Ui_VideoPlayerWidget


class VideoPlayerWidget(QWidget):
    def __init__(self, QWidget_parent=None, Qt_WindowFlags_flags=0):
        QWidget.__init__(self, QWidget_parent)
        self.ui=Ui_VideoPlayerWidget()
        savecwd = os.getcwd()
        os.chdir('view/qt_ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.media_player_widget = QVideoWidget(self.ui.top_frame)
        self.ui.top_frame_layout.addWidget(self.media_player_widget)
        self.media_player.setVideoOutput(self.media_player_widget)
        self.media_player_widget.show()

        self.media_player.bufferStatusChanged.connect(lambda x:self.ui.buffer.setValue(x))
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)


        self.ui.bn_play.clicked.connect(self.media_player.play)
        self.ui.bn_pause.clicked.connect(self.media_player.pause)
        self.ui.bn_stop.clicked.connect(self.media_player.stop)
        self.ui.bn_mute.clicked.connect(self.media_player.setMuted)
        self.ui.progress.sliderMoved.connect(self.media_player.setPosition)
        self.ui.volume.valueChanged.connect(self.media_player.setVolume)

    def play_url(self, url:URL):
        request = QNetworkRequest(QUrl(url.get()))
        # todo: сделать добавление cookie и подготовку proxу

        self.media_player.setMedia(QMediaContent(request))
        self.media_player.play()
        self.media_player.setMuted(True)

    def positionChanged(self, position):
        self.ui.progress.setValue(position)
        # self.ui.lbl_time.setText(self.time_format(position) + ' / ' + self.duration)

    def durationChanged(self, duration):
        self.ui.progress.setRange(0, duration)
        # self.duration = self.time_format(duration)


    def resume(self):
        # if self.save_state == QMediaPlayer.PlayingState:
        self.media_player.play()

    def pause(self):
        # self.save_state=self.media_player.state()
        # print(self.save_state)
        # if self.save_state == QMediaPlayer.PlayingState:
        self.media_player.pause()


if __name__ == "__main__":
    pass