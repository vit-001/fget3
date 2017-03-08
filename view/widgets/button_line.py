__author__ = 'Vit'

from PyQt5.Qt import QFont
from PyQt5.QtCore import QPoint, QRect, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *

class ActionButton(QToolButton):
    def __init__(self,tooltip:str, action:lambda:None):
        super().__init__(None)
        self.clicked.connect(action)
        self.setToolTip(tooltip)
        self.setAutoRaise(True)

    def set_button_style(self, attr_value_dict: dict):
        """
        :param attr_value_dict:
                Available styles:
                    'color' - text color
                    'background'
                    'font' - font family
                    'font_size'
                    'bold'
                    'italic'
                    'underline'
                    'autoraise' - autoraise button

            Example: button.set_button_style({'color':'magenta' , 'font_size': 18})
        """
        if not attr_value_dict:
            return
        style=''
        if 'color' in attr_value_dict and attr_value_dict['color']:
            style+='color: '+ attr_value_dict['color'] +';'
        if 'background' in attr_value_dict:
            style+='background-color: '+ attr_value_dict['background'] +';'

        if style is not '':
            self.setStyleSheet('QToolButton {'+ style +'}')

        font = QFont()
        if 'font' in attr_value_dict:
            font.setFamily(attr_value_dict['font'])
        if 'font_size' in attr_value_dict:
            font.setPointSize(attr_value_dict['font_size'])
        font.setBold(attr_value_dict.get('bold',False))
        font.setItalic(attr_value_dict.get('italic',False))
        font.setUnderline(attr_value_dict.get('underline',False))
        self.setFont(font)

        self.setAutoRaise(attr_value_dict.get('autoraise',True))

    def set_menu(self, menu):
        if menu:
            self.setMenu(menu)
            self.setPopupMode(QToolButton.MenuButtonPopup)

class TextButton(ActionButton):
    def __init__(self, text:str, tooltip:str='', action=lambda:None):
        super().__init__(tooltip, action)
        self.setText(text)


class ImageButton(ActionButton):
    def __init__(self, picture_filename:str, tooltip:str, action=lambda:None):
        super().__init__(tooltip, action)
        self.setText(tooltip)
        if picture_filename:
            pixmap = QPixmap(picture_filename)
            icon = QIcon()
            icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
            self.setIcon(icon)
            self.setIconSize(QSize(100, 100))


class ButtonLine(QWidget):
    def __init__(self, parent=None, height=25, space=2, speed=40):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.space = space
        self.height = height
        self.buttons = list()
        self.buttons_width = self.space * 2
        self.curr_scroll = 0
        self.speed = speed

    def add_button(self,button:QToolButton):
        button.setParent(self)
        button.setFixedHeight(self.height)
        self.buttons.append(button)
        self._place()
        self.show()

    def _add_button(self, text='', action=lambda: None, menu=None, tooltip='', bold=False, underline=False,
                   autoraise=False, text_color:str=None):

        button = QToolButton(self)

        if text_color is not None:
            button.setStyleSheet('QToolButton {color: '+text_color+';}')

        button.setText(text)
        font = QFont()
        font.setBold(bold)
        font.setUnderline(underline)
        button.setFont(font)
        button.setAutoRaise(autoraise)
        button.clicked.connect(action)
        button.setFixedHeight(self.height)
        button.setToolTip(tooltip)

        if menu is not None:
            button.setMenu(menu)
            button.setPopupMode(QToolButton.MenuButtonPopup)

        self.buttons.append(button)
        self._place()
        self.show()

    def clear(self):
        for item in self.buttons:
            item.setParent(None)
            item.clicked.disconnect()
            item.close()
        self.buttons = list()
        self.curr_scroll = 0
        self.hide()

    def minimumSizeHint(self):
        return QSize(0, self.height + 2 * self.space)

    def sizeHint(self):
        return QSize(0, self.height + 2 * self.space)

    def _place(self):
        x = self.space + self.curr_scroll * self.speed
        y = self.space
        for item in self.buttons:
            item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x += item.sizeHint().width() + self.space
            item.show()
        self.buttons_width = x

    def wheelEvent(self, event):
        delta = event.angleDelta().y() // 120
        if self.buttons_width < self.geometry().width():
            if delta < 0: return
        self.curr_scroll += delta
        if self.curr_scroll > 0: self.curr_scroll = 0
        self._place()
