# -*- coding: utf-8 -*-
__author__ = 'Vit'
import os

from PyQt6.QtWidgets import QWidget

from data_format.url import URL

from interface.hystory_interface import HistoryFromViewInterface
from interface.view_manager_interface import ViewManagerFromViewInterface

from view_qt6.qt_ui.ui_history_view import Ui_HistoryView


class HistoryView(QWidget):
    def __init__(self, parent:QWidget, view_manager:ViewManagerFromViewInterface):
        super().__init__(parent)

        self.view_manager=view_manager

        self.history_items=list()
        self.current_url=URL()
        self.history=None

        self.ui=Ui_HistoryView()
        savecwd = os.getcwd()
        os.chdir('view_qt5/qt_ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)

        self.ui.combo_history.addItem(self.current_url.get())
        self.binding()

    def binding(self):
        self.ui.bn_go.clicked.connect(self.on_go_clicked)
        self.ui.bn_back.clicked.connect(self.on_back_clicked)

    def update_history(self, history:HistoryFromViewInterface):
        self.history=history
        self.ui.combo_history.clear()
        self.history_items.clear()
        self.ui.combo_history.addItem(self.current_url.get())
        for item in reversed(history.get_history()):
            self.ui.combo_history.addItem(item.url.get())
            self.history_items.append(item)

    def set_current_url(self, url:URL):
        self.current_url=url
        self.ui.combo_history.setItemText(0,self.current_url.get())

    def on_go_clicked(self):
        index=self.ui.combo_history.currentIndex()
        text=self.ui.combo_history.currentText()
        if index==0:
            if text.strip() == self.current_url.get():
                self.view_manager.goto_url(self.current_url)
            else:
                self.view_manager.goto_url(URL(text))
        else:
            if text.strip() == self.history_items[index - 1].url.get():
                item = self.history_items[index - 1]
                self.view_manager.goto_url(item.url, {'context':item.context})
            else:
                self.view_manager.goto_url(URL(text))

    def on_back_clicked(self):
        if self.history:
            item=self.history.back()
            if item:
                self.view_manager.goto_url(item.url,{'context':item.context,'no_history':True})


if __name__ == "__main__":
    pass