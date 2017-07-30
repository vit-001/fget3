# -*- coding: utf-8 -*-
__author__ = 'Vit'

from data_format.history_data import HistoryData
from interface.hystory_interface import HistoryFromViewInterface, HistoryFromModelInterface


class HistoryModel(HistoryFromViewInterface, HistoryFromModelInterface):
    def __init__(self, history_name:str, on_changed_handlr: lambda history_from_view_interface:None):
        self.name=history_name
        self.back_data=list()
        self.handler=on_changed_handlr

    def add(self, data:HistoryData):
        # print('=======add to history==',data)
        self.back_data.append(data)
        self.handler(self)

    def get_history(self, qty=20) -> list:
        return self.back_data

    def forward(self) -> HistoryData:
        return super().forward()

    def back(self) -> HistoryData:
        # print('=======go back=========')
        if self.back_data:
            item=self.back_data.pop()
            self.handler(self)
            return item
        return None

if __name__ == "__main__":
    pass