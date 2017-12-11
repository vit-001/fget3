# -*- coding: utf-8 -*-
__author__ = 'Vit'



from multiprocessing import Process
import os
import sys

from socket import socket, AF_INET, SOCK_STREAM

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

class SeleniumLoadServer(Process):
    def __init__(self, port = 50008):
        self.port=port
        self.driver=None
        super().__init__()

    def run(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(('', self.port))
        sock.listen(10)
        while True:
            conn, addr = sock.accept()
            data = conn.recv(1024).decode(errors='ignore')

            print('SeleniumLoadServer: data:',data)

            if data.startswith('TERMINATE'):
                # print('SeleniumLoadServer: Terminate')
                if self.driver:
                    self.driver.quit()
                    self.driver=None
                break

            if not self.driver:
                print('SeleniumLoadServer: Creating Firefox headless driver')
                os.environ['MOZ_HEADLESS'] = '1'
                binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe', log_file=sys.stdout)
                self.driver = webdriver.Firefox(firefox_binary=binary)

            try:
                print('SeleniumLoadServer: Loading', data)
                self.driver.get(data)

            except None:
                pass
            else:
                data=self.driver.page_source
                print('SeleniumLoadServer: ', len(data), 'bytes load')
                conn.send(data.encode(encoding='utf-8', errors='strict'))
                # self.driver.get('about:blank')
                conn.close()

    def abort(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(('localhost', self.port))
        sock.send('TERMINATE'.encode())
        sock.close()


if __name__ == "__main__":
    server=SeleniumLoadServer()
    server.start()

    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 50008))

    addr='http://www.drtuber.com/video/4065629/hot-sexy-teen-deep-throat-blowjob'

    sock.send(addr.encode())

    recvdata = sock.recv(1024)
    recv = recvdata
    while recvdata:
        recvdata = sock.recv(1024)
        recv += recvdata

    # print(recv.decode())


    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 50008))

    addr='http://www.drtuber.com/video/4065629/hot-sexy-teen-deep-throat-blowjob'

    sock.send(addr.encode())
    reply = sock.recv(1024)
    sock.close()
    # print(reply.decode())

    server.abort()
