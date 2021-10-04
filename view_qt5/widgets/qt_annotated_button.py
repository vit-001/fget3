# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon,QFont
from PyQt5.QtWidgets import QToolButton,QWidget,QPushButton,QLayout,QSizePolicy,QApplication,QVBoxLayout,QLabel

def get_align(align_string='top'):
    s=align_string.upper().split(' ')
    align=Qt.AlignAbsolute
    for item in s:
        if item == 'LEFT': align |=Qt.AlignLeft
        if item == 'RIGHT': align |= Qt.AlignRight
        if item == 'CENTER': align |= Qt.AlignHCenter
        if item == 'JUSTIFY': align |= Qt.AlignJustify
        if item == 'TOP': align |= Qt.AlignTop
        if item == 'BOTTOM': align |= Qt.AlignBottom
    return align

class QAnnotatedButton(QToolButton):

    def __init__(self, QWidget_parent=None, labels:list=tuple()):
        super().__init__(QWidget_parent)

        self.labels=list()

        for item in labels:
            label=QLabel(self)
            text=item.get('text','')
            lenght=item.get('lenght',29)
            if len(text)>lenght-3:
                text=text[:lenght-3]+'...'
            label.setText(text)
            label.setAlignment(get_align(item.get('align','bottom')) )
            label.setMargin(5)
            self.labels.append(label)
            if item.get('bold',False):
                font=QFont()
                font.setBold(True)
                label.setFont(font)
            # label.setFont(QFont("Times", 8, QFont.Bold))

    def setFixedSize(self, *__args):
        super().setFixedSize(*__args)
        for item in self.labels:
            item.setFixedSize(*__args)

if __name__ == "__main__":

    class Window(QWidget):
        def __init__(self):

            super(Window, self).__init__()
            self.thumb_size=150

            layout = QVBoxLayout()

            button1 = QAnnotatedButton()
            button1.setAutoRaise(True)
            button1.setText('testtesttest')
            button1.setTextBottom('bottom')
            button1.setTextTop('top')
            button1.setFixedSize(self.thumb_size, self.thumb_size) #E:\repo\fget\view_qt5\qt_ui\files\picture
            button1.setToolTip('popup')

            pixmap = QPixmap('E:/repo/fget/view_qt5/qt_ui/files/picture/logo.png')
            icon = QIcon()
            icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
            button1.setIcon(icon)
            button1.setIconSize(QSize(self.thumb_size, self.thumb_size))


            button2 = QAnnotatedButton()
            button2.setAutoRaise(True)
            button2.setText('testtesttest')
            button2.setFixedSize(self.thumb_size, self.thumb_size)
            button2.setToolTip('popup')


            layout.addWidget(button1)
            layout.addWidget(button2)

            self.setLayout(layout)

            self.setWindowTitle("Test")


    import sys

    app = QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())
