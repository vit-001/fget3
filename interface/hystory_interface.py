# -*- coding: utf-8 -*-
__author__ = 'Vit'

class HistoryFromViewInterface:
    def get_history(self)->list:
        return []


class HistoryFromModelInterface:
    def add(self, data):
        pass


if __name__ == "__main__":
    pass