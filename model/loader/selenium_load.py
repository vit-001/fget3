# -*- coding: utf-8 -*-
__author__ = 'Vit'


from selenium import webdriver
# import requests

from data_format.url import URL
from data_format.loader_error import LoaderError

from model.loader.base_loader import BaseLoadProcedure


class SeleniumLoad(BaseLoadProcedure):
    driver=None

    def __init__(self, proxies=None):
        # self.proxies = proxies
        self.driver = None


    def open(self, url: URL) -> bytes:
        if not self.driver:
            self.driver=webdriver.Ie()
            self.driver.minimize_window()

        try:
            if url.method == 'GET':
                self.driver.get(url.get())
            else:
                raise LoaderError('Unknown method:' + url.method)

            data=self.driver.page_source.encode(encoding='utf-8', errors='strict')
            self.driver.close()

        except None:
            raise LoaderError('Unknown error in loader')
        else:
            return data

    def get_redirect_location(self, url: URL) -> URL:
        return url


if __name__ == "__main__":
    l = SeleniumLoad()
    url = URL('https://www.porntube.com/videos/via-lasciva-dp-trio-painters_7282989')
    print(l.open(url).decode(errors='ignore'))
