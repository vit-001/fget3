# -*- coding: utf-8 -*-
__author__ = 'Vit'

from data_format.url import URL

class HistoryData:
    def __init__(self, url:URL, context=None):
        self.url=url
        self.context=context

    def __eq__(self, other):
        if self.url == other.url:
            return True
        return False

    def __str__(self):
        return '<HistoryData:'+self.url.get()+' at:'+str(self.context)+'>'

if __name__ == "__main__":
    pass