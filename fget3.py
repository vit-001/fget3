# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
import sys, time
from multiprocessing import freeze_support

from PyQt5.QtWidgets import QApplication

from common.url import URL

from model.model import Model
from view.view_manager.view_manager import ViewManager
from controller.controller import Controller

if __name__ == '__main__':
    freeze_support()

    print(sys.argv)

    from xutil.conpile_interfaces import InterfaceCompiler
    ic = InterfaceCompiler(sys.argv[0].rpartition('/')[0])
    ic.compile_interfaces()


    app = QApplication(sys.argv)

    view=ViewManager()
    model=Model(view)
    controller=Controller(view,model)

    # model.goto_url(URL("https://www.veronicca.com/videos?o=mr*", test_string='Veronicca'))
    # time.sleep(1)
    # model.goto_url(URL("https://www.veronicca.com/videos?o=mr&page=2*", test_string='Veronicca'))
    # time.sleep(1)
    # model.goto_url(URL("https://www.veronicca.com/videos?o=mr&page=3*", test_string='Veronicca'))
    # time.sleep(1)
    # model.goto_url(URL("https://www.veronicca.com/videos?o=mr&page=4*", test_string='Veronicca'))
    # time.sleep(1)
    # model.goto_url(URL("https://www.veronicca.com/videos?o=mr&page=5*", test_string='Veronicca'))
    # time.sleep(1)
    # model.goto_url(URL("https://www.veronicca.com/videos?o=mr&page=6*", test_string='Veronicca'))

    sys.exit(app.exec_())






