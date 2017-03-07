# -*- coding: utf-8 -*-
__author__ = 'Vit'

from interface.hystory_interface import HistoryFromViewInterface, HistoryFromModelInterface


class HistoryModel(HistoryFromViewInterface, HistoryFromModelInterface):
    def __init__(self, history_name:str, on_changed_handlr: lambda history_from_view_interface:None):
        self.name=history_name
        self.data=list()
        self.handler=on_changed_handlr

    def add(self, data):
        print('add to history',self.name, data)
        self.data.append(data)
        self.handler(self)

    def get_history(self) -> list:
        return self.data



if __name__ == "__main__":
    pass