# -*- coding: utf-8 -*-
__author__ = 'Vit'
from socket import socket, AF_INET, SOCK_STREAM

from data_format.url import URL
from data_format.loader_error import LoaderError

from model.loader.base_loader import BaseLoadProcedure

from model.loader.selenium_load_server import SeleniumLoadClient

class SeleniumHiddenFirefoxLoad(BaseLoadProcedure):
    def __init__(self, proxies=None):
        self.proxies = proxies

    def open(self, url: URL) -> bytes:
        try:
            if url.method == 'GET':
                sock = SeleniumLoadClient()

                sock.command(url.get())
                sock.send()
                recv = sock.recv()
                sock.close()

            elif url.method == 'SCRIPT':
                sock = SeleniumLoadClient()
                script=url.any_data
                for item in script.splitlines():
                    sock.command(item)
                sock.send()
                recv = sock.recv()
                sock.close()

            else:
                raise LoaderError('Unknown method:' + url.method)

        except None:
            raise LoaderError('Unknown error in loader')
        else:
            return recv

    def get_redirect_location(self, url: URL) -> URL:
        return url

    def abort(self):
        print('Aborted')


if __name__ == "__main__":
    l = SeleniumHiddenFirefoxLoad()
    url = URL('https://www.porntube.com/videos/via-lasciva-dp-trio-painters_7282989')
    print(l.open(url).decode(errors='ignore'))
