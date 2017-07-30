__author__ = 'Vit'

from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import (QPainter)
from PyQt5.QtWidgets import (QWidget)


class ProgressHLine(QWidget):
    def __init__(self, parent=None, height=6):
        QWidget.__init__(self, parent)

        self.height = height
        self.margin = 3

        self.names = list()
        self.values = dict()
        self.colors = dict()
        self.max_value = 1
        self.autohide_bar_name=None

    def add_progress(self, name:str, color=Qt.red):
        self.names.append(name)
        self.values[name] = 0
        self.colors[name] = color

    def set_value(self, name:str, value:int):
        self.values[name] = value
        if self.autohide_bar_name:
            if self.values.get(self.autohide_bar_name,-1) >= self.max_value:
                self.hide()
        self.update()

    def set_max_value(self, value:int):
        self.max_value = value
        if self.max_value == 0:
            self.hide()
        else:
            self.show()

    def set_autohide_bar_name(self, name:str):
        self.autohide_bar_name = name

    def reset(self):
        for name in self.names:
            self.values[name] = 0
        self.set_max_value(0)
        self.update()

    def minimumSizeHint(self):
        return QSize(10, self.height + 2 * self.margin)

    def sizeHint(self):
        return QSize(10, self.height + 2 * self.margin)

    def paintEvent(self, event):
        geometry = self.geometry()
        painter = QPainter(self)

        border = QRect(self.margin, self.margin, geometry.width() - 2 * self.margin, self.height )
        painter.setPen(Qt.darkGray)
        painter.drawRect(border)

        if self.max_value == 0:
            return

        line_width = geometry.width() - 1 - 2 * self.margin
        for name in self.names:
            rect = QRect(self.margin, self.margin, self.values[name] * line_width / self.max_value, self.height - 1)
            painter.setBrush(self.colors[name])
            painter.setPen(self.colors[name])
            painter.drawRect(rect)

