# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
import sys, os
from multiprocessing import freeze_support

from PyQt5.QtWidgets import QApplication

from common.setting import Setting

from controller.controller import Controller
from model.model import Model
from view.view_manager import ViewManager


if __name__ == '__main__':
    freeze_support()

    for item in sys.argv[1:]:
        if item.startswith('-compile'):
            print('Compile Qt interfaces')
            from xutil.compile_qt_interfaces import InterfaceCompiler
            ic = InterfaceCompiler(sys.argv[0].rpartition('/')[0])
            ic.compile_interfaces()
        if item.startswith('-small_window'):
            print('Run in small window mode')
            Setting.main_window_h_in_percents = 45
            Setting.full_window_h_in_percents = 45
            Setting.full_window_w_gap_in_percents = 25

    app = QApplication(sys.argv)

    view=ViewManager()
    model=Model(view)
    controller=Controller(view,model)

    sys.exit(app.exec_())






