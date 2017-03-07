# -*- coding: utf-8 -*-
__author__ = 'Vit'

from data_format.url import URL

class FLData:
    def __init__(self, url: URL, filename: str, overwrite=True):
        self._url = url
        self._filename = filename
        self.overwrite = overwrite
        self.text=''

    @property
    def url(self):
        return self._url

    @property
    def filename(self):
        return self._filename


if __name__ == "__main__":
    pass