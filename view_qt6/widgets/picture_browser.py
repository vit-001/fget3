# -*- coding: utf-8 -*-
__author__ = 'Vit'

from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QEventLoop

class PictureBrowser(QLabel):
    def __init__(self, parent:QWidget, on_current_change:lambda index:None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.pictures=list()
        self.current_picture=0
        self.on_current_change=on_current_change

    def re_init(self):
        self.pictures = list()
        self.current_picture = 0

    def add_picture(self, filename):
        print('Add picture',filename)
        self.pictures.append(QPixmap(filename))
        self.show_current_picture()
        QEventLoop().processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
        self.update()

    @property
    def count(self):
        return len(self.pictures)

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
        self.on_current_change(self.current_picture)

    def wheelEvent(self, event):
        self.current_picture -= event.angleDelta().y() // 120
        if self.current_picture < 0: self.current_picture = 0
        if self.current_picture > len(self.pictures) - 1:
            self.current_picture = len(self.pictures) - 1
        self.show_current_picture()




if __name__ == "__main__":
    pass