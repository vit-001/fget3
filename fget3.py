# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
import sys
from multiprocessing import freeze_support

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from common.url import URL

from model.model import Model
from view.base_view import AbstractViewFromModelInterface
from view.view_manager import ViewManager
from model.loader.multiprocess_az_loader import MultiprocessAZloader


if __name__ == '__main__':

    freeze_support()
    # loader=MultiprocessAZloader()



    # import time
    # time.sleep(2)

    # loader.on_exit()


    app = QApplication(sys.argv)

    view=ViewManager()
    model=Model(view)

    timer = QTimer()
    timer.timeout.connect(model.on_cycle_handler)
    timer.start(100)



    model.goto_url(URL("http://collectionofbestporn.com/most-recent*", test_string='Collection'))




    sys.exit(app.exec_())




