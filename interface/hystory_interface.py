# -*- coding: utf-8 -*-
__author__ = 'Vit'

from data_format.history_data import HistoryData


class HistoryFromViewInterface:
    def get_history(self)->list:
        return []

    def back(self)->HistoryData:
        pass

    def forward(self)->HistoryData:
        pass

class HistoryFromModelInterface:
    def add(self, data:HistoryData):
        pass


if __name__ == "__main__":
    pass