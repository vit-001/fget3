# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
import sys
from multiprocessing import freeze_support

from PyQt5.QtWidgets import QApplication

from common.url import URL

from model.model import Model
from view.view_manager import ViewManager
from controller.controller import Controller

if __name__ == '__main__':
    # freeze_support()

    app = QApplication(sys.argv)

    view=ViewManager()
    model=Model(view)
    controller=Controller(view,model)

    model.goto_url(URL("http://collectionofbestporn.com/most-recent*", test_string='Collection'))

    sys.exit(app.exec_())




