# -*- coding: utf-8 -*-
__author__ = 'Vit'

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEventLoop

class PictureBrowser(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setAlignment(Qt.AlignCenter)
        self.pictures=list()
        self.current_picture=0

    def re_init(self):
        self.pictures = list()
        self.current_picture = 0

    def add_picture(self, filename):
        self.pictures.append(QPixmap(filename))
        self.show_current_picture()
        QEventLoop().processEvents(QEventLoop.AllEvents)
        self.update()

    def show_current_picture(self):
        self.show_picture(self.current_picture)

    def show_picture(self, index):
        try:
            picture=self.pictures[index]

            container_rect = self.contentsRect()
            picture_rect = picture.rect()

            try:
                if container_rect.height() / container_rect.width() < picture_rect.height() / picture_rect.width():
                    pix1 = picture.scaledToHeight(container_rect.height(), Qt.SmoothTransformation)
                else:
                    pix1 = picture.scaledToWidth(container_rect.width(), Qt.SmoothTransformation)
                self.setPixmap(pix1)
            except ZeroDivisionError:
                pass
        except IndexError:
            pass

    def wheelEvent(self, event):
        self.current_picture -= event.angleDelta().y() // 120
        if self.current_picture < 0: self.current_picture = 0
        if self.current_picture > len(self.pictures) - 1:
            self.current_picture = len(self.pictures) - 1
        self.show_current_picture()



if __name__ == "__main__":
    pass