# -*- coding: utf-8 -*-
__author__ = 'Vit'



from multiprocessing import Process
import os
import sys

from socket import socket, AF_INET, SOCK_STREAM

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException
from selenium import webdriver

class SeleniumLoadServer(Process):
    def __init__(self, port = 50008, hidden=True):
        self.port=port
        self.driver=None
        self.hidden=hidden
        super().__init__()

    def run(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(('', self.port))
        sock.listen(10)

        print('SeleniumLoadServer: started')

        while True:
            conn, addr = sock.accept()

            recvdata = conn.recv(8192)
            recv = recvdata
            commands=recv.rstrip(b'\r\n').split(b'\r\n\r\n')
            # print(commands)

            for command in commands:
                data = command.decode(errors='ignore')
                print('SeleniumLoadServer: data:',data)

                terminate=self._decode_command(data, conn)
                if terminate: return

            self.driver.get('about:blank')
            conn.close()

    def _prepare_driver(self):
        if not self.driver:
            if self.hidden:
                print('SeleniumLoadServer: Creating Firefox headless driver')
                os.environ['MOZ_HEADLESS'] = '1'
                binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe', log_file=sys.stdout)
                self.driver = webdriver.Firefox(firefox_binary=binary)
            else:
                print('SeleniumLoadServer: Creating Chrome driver')
                self.driver=webdriver.Chrome()


    def _decode_command(self, command:str, conn)->bool:

        if command.startswith('TERMINATE'):
            print('SeleniumLoadServer: Terminate')
            if self.driver:
                self.driver.quit()
                self.driver = None
            return True

        self._prepare_driver()

        if command.startswith('OPEN:'):
            data=command.partition('OPEN:')[2]
            print('SeleniumLoadServer: Loading', data)
            self.driver.get(data)

        elif command.startswith('CLICK_CLASS:'):
            data = command.partition('CLICK_CLASS:')[2]
            try:
                element = self.driver.find_element_by_class_name(data)
                actions = ActionChains(self.driver)
                actions.click(element)
                actions.perform()
            except NoSuchElementException:
                print('NoSuchElementException', data)
            except MoveTargetOutOfBoundsException:
                print('MoveTargetOutOfBoundsException', data)


        elif command.startswith('SOURCE'):
            data=self.driver.page_source
            print('SeleniumLoadServer: ', len(data), 'bytes load')
            conn.send(data.encode(encoding='utf-8', errors='strict'))

        elif command.startswith('CLOSE_POPUP'):
            print('SeleniumLoadServer: clear popup')
            current = self.driver.current_window_handle
            for handle in self.driver.window_handles:
                if handle != current:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
            self.driver.switch_to.window(current)

        elif command.startswith('CLEAR'):
            self.driver.get('about:blank')

        elif command.startswith('http'):
            try:
                print('SeleniumLoadServer: Loading', command)
                self.driver.get(command)

            except None:
                pass
            else:
                data=self.driver.page_source
                print('SeleniumLoadServer: ', len(data), 'bytes load')
                conn.send(data.encode(encoding='utf-8', errors='strict'))

        return False

    def abort(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(('localhost', self.port))
        sock.send('TERMINATE'.encode())
        sock.close()

class SeleniumLoadClient:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(('localhost', 50008))

        self.data=b''

    def command(self, data:str):
        self.data+=data.encode()+b'\r\n\r\n'

    def send(self):
        self.sock.send(self.data)


    def recv(self)->bytes:
        recvdata = self.sock.recv(8192)
        r = recvdata
        while recvdata:
            recvdata = self.sock.recv(8192)
            r += recvdata

        return r

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    pass
