# -*- coding: utf-8 -*-
__author__ = 'Vit'


import os
import sys

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

from data_format.url import URL
from data_format.loader_error import LoaderError

from model.loader.base_loader import BaseLoadProcedure


class SeleniumServerLoad(BaseLoadProcedure):


    def __init__(self, proxies=None):
        self.proxies = proxies
        self.driver = None

    def open(self, url: URL) -> bytes:
        # print(self.driver)
        if not self.driver:
            os.environ['MOZ_HEADLESS'] = '1'
            binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe', log_file=sys.stdout)
            self.driver = driver = webdriver.Firefox(firefox_binary=binary)
            # self.driver.minimize_window()

        try:
            if url.method == 'GET':
                self.driver.get(url.get())
            #
            # elif url.method == 'POST':
            #     # print('Loading POST')
            #     # print(url.get(), url.post_data)
            #     response = requests.post(url.get(), data=url.post_data, proxies=self.proxies,headers=headers)
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
    l = SeleniumServerLoad()
    url = URL('https://www.porntube.com/videos/via-lasciva-dp-trio-painters_7282989')
    print(l.open(url).decode(errors='ignore'))
