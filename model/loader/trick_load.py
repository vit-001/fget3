# -*- coding: utf-8 -*-
__author__ = 'Vit'

import socket
import urllib.parse

from common.url import URL
from model.loader.base_loader import BaseLoadProcedure, LoaderError


class TrickLoad(BaseLoadProcedure):
    def __init__(self):
        self.trick_headers = {
            'sp_method': "GET  {0} HTTP/1.0\r\nHost: {1}\r\nConnection: close\r\n\r\n",
            'cr_method': "\nGET {0} HTTP/1.0\r\nHost: {1}\r\nConnection: close\r\n\r\n",
            'tab_method': "GET {0} HTTP/1.0\r\nHost: {1}\t\r\nConnection: close\r\n\r\n",
            'point_method': "GET {0} HTTP/1.0\r\nHost: {1}.\r\nConnection: close\r\n\r\n",
            'host_method': "GET {0} HTTP/1.0\r\nhost: {1}\r\nConnection: close\r\n\r\n",
            'unix_method': "GET {0} HTTP/1.0\nHost: {1}\nConnection: close\n\n",
            'order_method': "GET {0} HTTP/1.0\r\nConnection: close\r\nHost: {1}\r\n\r\n",
        }
        self.default_trick = None

    def open(self, url: URL, trick=None) -> bytes:

        trick = self.default_trick if trick is None else trick
        if trick is None:
            return b''

        us = urllib.parse.urlsplit(url.get())
        hostname = us[1]
        addr = socket.gethostbyname(hostname)

        if us[2] is not '':
            uri = us[2]
        else:
            uri = '/'

        if us[3] is not '':
            uri += '?' + us[3]

        try:
            result = self._send(addr, 80, self.trick_headers[trick].format(uri, hostname))

        except Exception as e:
            raise LoaderError(e.__repr__())

        (head, sp, body) = result.partition(b'\r\n\r\n')
        # print(head.decode())

        return body

    def _send(self, host, port, data) -> bytes:
        recv = ''
        sock = socket.create_connection((host, port), 10)
        try:
            sock.sendall(data.encode())
            recvdata = sock.recv(8192)
            recv = recvdata
            while recvdata:
                recvdata = sock.recv(8192)
                recv += recvdata
        finally:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            sock.close()
        return recv


if __name__ == "__main__":
    pass
