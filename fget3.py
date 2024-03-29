# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()

    #     print('Todo:')
    #     # print('www.tgpdog.com', '  - VeroniccaComSite ')
    #     print('http://www.shameless.com/', 'verifyed, script')
    #     # print('http://www.phicatube.net/videos', 'verifyed, plus file; "var cnf ="')
    #     # print('https://www.pornfreeze.com/','verifyed, simple')
    #     print('https://www.ebalovo.com/', 'simple')
    #     print('http://www.txxx.com/  script')
    #     # print('https://faapy.com/', 'jwplayer script')
    #     print('https://kinovau.tv/','verifyed, simple')
    #     # print('http://www.girlstop.info/','photo')
    #     # print('https://www.coedcherry.com/models/danica-mpl-studios')
    #
    #     # print('Исправить TUBE8')
    #     print('Thats all')
    
    print("Let's go..")
    print('')

    import sys, os

    print("Python version {}.{}.".format(sys.version_info.major, sys.version_info.minor))

    qt = 'pyqt6'

    for item in sys.argv[1:]:
        if item.startswith('-pyqt5'):
            qt = 'pyqt5'

    if qt == 'pyqt5':
        print('Starting with PyQt5')

        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import qVersion

        print('PyQt version: ' + qVersion())

        from common.setting import Setting
        from controller.controller import Controller
        from model.model import Model
        from view_qt5.view_manager import ViewManager

        for item in sys.argv[1:]:
            if item.startswith('-compile'):
                print('Compile Qt interfaces')
                from xutil.compile_qt_interfaces import InterfaceCompiler

                ic = InterfaceCompiler(sys.argv[0].rpartition('/')[0])
                ic.compile_interfaces()
            if item.startswith('-small_window'):
                print('Run in small window mode')
                Setting.main_window_x0_in_percents = 25
                Setting.main_window_h_in_percents = 45
                Setting.full_window_h_in_percents = 45
                Setting.full_window_w_gap_in_percents = 2

        app = QApplication(sys.argv)

        view = ViewManager()
        model = Model(view)
        controller = Controller(view, model)
        Setting.log = view.get_log()

        sys.exit(app.exec_())

    if qt == 'pyqt6':
        print('Run with PyQt6')
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import qVersion

        from common.setting import Setting
        from controller.controller import Controller
        from model.model import Model
        from view_qt6.view_manager import ViewManager

        for item in sys.argv[1:]:
            # if item.startswith('-compile'):
            #     print('Compile Qt interfaces')
            #     from xutil.compile_qt_interfaces import InterfaceCompiler
            #
            #     ic = InterfaceCompiler(sys.argv[0].rpartition('/')[0])
            #     ic.compile_interfaces()
            if item.startswith('-small_window'):
                print('Run in small window mode')
                Setting.main_window_x0_in_percents = 25
                Setting.main_window_h_in_percents = 45
                Setting.full_window_h_in_percents = 45
                Setting.full_window_w_gap_in_percents = 2

        app = QApplication(sys.argv)

        view = ViewManager()
        model = Model(view)
        controller = Controller(view, model)
        Setting.log = view.get_log()

        sys.exit(app.exec())
