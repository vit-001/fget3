# -*- coding: utf-8 -*-
__author__ = 'Vit'
import os
from PyQt5.QtWidgets import QWidget

from common.url import URL

from view.qt_ui.ui_history_view import Ui_HistoryView

from view.view_manager_interface import ViewManagerFromViewInterface
from model.history_model.hystory_interface import HistoryFromViewInterface

class HistoryView(QWidget):
    def __init__(self, parent:QWidget, view_manager:ViewManagerFromViewInterface):
        super().__init__(parent)

        self.view_manager=view_manager

        self.history_items=list()

        self.ui=Ui_HistoryView()
        savecwd = os.getcwd()
        os.chdir('view/qt_ui')
        self.ui.setupUi(self)
        os.chdir(savecwd)

        self.binding()

    def binding(self):
        self.ui.bn_go.clicked.connect(self.on_go_clicked)
        self.ui.bn_back.clicked.connect(self.on_back_clicked)

    def update_history(self, history:HistoryFromViewInterface):
        print('updating history')
        self.ui.combo_history.clear()
        self.history_items.clear()
        self.ui.combo_history.addItem('---')
        for item in reversed(history.get_history()):
            print(item)
            self.ui.combo_history.addItem(item['url'].get())
            self.history_items.append(item)

    def on_go_clicked(self):
        print('go')
        index=self.ui.combo_history.currentIndex()
        text=self.ui.combo_history.currentText()
        if index==0:
            pass # todo подумать что здесь
        else:
            print(index, text, self.history_items[index-1])
            if text.strip() == self.history_items[index - 1]['url'].get():
                self.go_to_index(index)
            else:
                self.view_manager.goto_url(URL(text))

    def go_to_index(self, index):
        item = self.history_items[index - 1]
        self.view_manager.goto_url(item['url'], item['context'])

    def on_back_clicked(self):
        print('back')
        self.go_to_index(1) #todo много чего


if __name__ == "__main__":
    pass