# -*- coding: utf-8 -*-
__author__ = 'Vit'

from model.history_model.hystory_interface import HistoryFromViewInterface

class HistoryModel(HistoryFromViewInterface):
    def __init__(self, history_name:str):
        self.name=history_name
        self.data=list()

    def add(self, data):
        print('add to history',self.name, data)
        self.data.append(data)


if __name__ == "__main__":
    pass