# -*- coding: utf-8 -*-
__author__ = 'Vit'
import os

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import  QMediaPlayer, QAudioOutput #,QMediaContent
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtNetwork import QNetworkRequest
from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtGui import QAction

import requests
import requests.exceptions

from common.util import get_menu_handler
from data_format.url import URL

from view_qt6.qt_ui.ui_video_player_widget import Ui_VideoPlayerWidget

class VideoWidget(QVideoWidget):
    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.setFullScreen(not self.isFullScreen())


class VideoPlayerWidget(QWidget):
    def __init__(self, QWidget_parent=None, Qt_WindowFlags_flags=0):
        QWidget.__init__(self, QWidget_parent)

        self.ui=Ui_VideoPlayerWidget()
        savecwd = os.getcwd()
        os.chdir('view_qt5/qt_ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)

        self.duration=0
        self.urls=list()
        self.default=-1
        self.url=URL()
        self.saved_position=None

        self.ui.buffer.setMaximum(100)

        self.media_player = QMediaPlayer()#None, QMediaPlayer.VideoSurface)
        self.audio_output= QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        self.media_player_widget = VideoWidget(self.ui.top_frame)
        self.ui.top_frame_layout.addWidget(self.media_player_widget)
        self.media_player.setVideoOutput(self.media_player_widget)
        self.media_player_widget.show()

        # self.media_player.bufferProgressChanged.connect(lambda x:self.ui.buffer.setValue(x))
        self.media_player.bufferProgressChanged.connect(self.buffer_progress_changed)
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)
        self.media_player.errorOccurred.connect(self.handleError)

        # self.ui.buffer.hide()

        self.ui.bn_play.clicked.connect(self.media_player.play)
        self.ui.bn_pause.clicked.connect(self.media_player.pause)
        self.ui.bn_stop.clicked.connect(self.stop)
        self.ui.bn_mute.clicked.connect(self.audio_output.setMuted)
        self.ui.progress.sliderMoved.connect(self.media_player.setPosition)
        self.ui.volume.valueChanged.connect(self.volume_changed)


    def buffer_progress_changed(self,x:float):
        # print(x)
        self.ui.buffer.setValue(int(100*x))

    def volume_changed(self,x:int):
        # print(x)
        self.audio_output.setVolume(float(x)/100.0)

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
        self.url=url
        # request = QNetworkRequest(QUrl(url.get()))
        # request.setHeader(QNetworkRequest.UserAgentHeader,url.user_agent)
        # if url.referer:
        #     request.setRawHeader('Referer',url.referer.get())

        # todo: сделать добавление cookie и подготовку proxу

        # print(request.rawHeaderList())
        # print(request.rawHeader('User-Agent'))
        # print(request.rawHeader('Referer'))

        # print(QUrl(url.get()))

        url_get=url.get()

        if url.redirect:
            r=requests.get(url.get(), allow_redirects=False)
            url_get= r.headers.get('Location', url.get())
            print('Player redirect to', url_get)


        self.media_player.setSource(QUrl(url_get))

        # print(self.media_player.media().canonicalRequest())

    def media_status_changed(self, media_status):
        if media_status == QMediaPlayer.MediaStatus.BufferedMedia:
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

    def stop(self):
        self.media_player.stop()

    def pause(self):
        self.media_player.pause()

    def set_volume(self, volume:int):
        self.ui.volume.setValue(volume)
        self.volume_changed(volume)

    def get_volume(self)->int:
        return self.ui.volume.value()

    def mute(self, on:bool):
        self.audio_output.setMuted(on)
        self.ui.bn_mute.setChecked(on)

    def is_muted(self):
        return self.ui.bn_mute.isChecked()

    def set_error_handler(self, on_error=lambda error_text:None):
        self.on_error=on_error

    def handleError(self):
        # print(self.media_player.error())
        print("Error in " + self.url.get() + ': ' + self.media_player.errorString())
        self.on_error("Error in " + self.url.link() + ': ' + self.media_player.errorString())
        # self.error_handler('Player error: ' + self.media_player.errorString())

    def destroy(self, bool_destroyWindow=True, bool_destroySubWindows=True):
        self.media_player.deleteLater()
        super().destroy(bool_destroyWindow, bool_destroySubWindows)


if __name__ == "__main__":
    pass