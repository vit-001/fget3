# -*- coding: utf-8 -*-
__author__ = 'Vit'

from model.loader.selenium_load_server import SeleniumLoadServer, SeleniumLoadClient
from bs4 import BeautifulSoup


if __name__ == "__main__":
    # freeze_support()

    server = SeleniumLoadServer(hidden=False)
    server.start()


    sock1=SeleniumLoadClient()

    sock1.command('http://datoporn.co/embed-5w4yfk3qm2f6.html')
    # # sock1.command('SOURCE')
    # sock1.command('CLICK_CLASS:modal_btn')
    # sock1.command('CLICK_CLASS:drt-button-play')
    # sock1.command('CLICK_CLASS:drt-button-quality')
    #
    # sock1.command('CLOSE_POPUP')
    # sock1.command('SOURCE')

    sock1.send()

    data = sock1.recv().decode()
    print(data)

    # soup=BeautifulSoup(data, "lxml")
    # container = soup.find('div', {'id': 'player'})
    # if container:
    #     for source in container.find_all('source'):
    #         print(source.attrs['data-quality'], source.attrs['src'])
    #         # self.set_default_video(-1)
    #
    #
    # sock1.close()
    #
    #
    # sock2=SeleniumLoadClient()
    #
    # sock2.command('OPEN:http://www.drtuber.com/video/4082638/teen-tied-and-made-to-cum-big-booty-amateur-fuck')
    # # sock1.command('SOURCE')
    # sock2.command('CLICK_CLASS:modal_btn')
    # sock2.command('CLICK_CLASS:drt-button-play')
    # sock2.command('CLICK_CLASS:drt-button-quality')
    #
    # sock2.command('SOURCE')
    #
    # sock2.send()
    #
    # data = sock2.recv().decode()
    # # print(data)
    #
    # soup=BeautifulSoup(data, "lxml")
    # container = soup.find('div', {'id': 'player'})
    # if container:
    #     for source in container.find_all('source'):
    #         print(source.attrs['data-quality'], source.attrs['src'])
    #         # self.set_default_video(-1)
    #
    #
    # sock2.close()
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    server.abort()
