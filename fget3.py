# -*- coding: utf-8 -*-
__author__ = 'Nikitin'
from multiprocessing import freeze_support
if __name__ == '__main__':
    freeze_support()

    # from xutil.install_module import test_module
    #
    # test_module('bs4', 'beautifulsoup4')
    # test_module('PyQt5')
    # test_module('requests')
    # test_module('lxml')

    import sys, os

    from PyQt5.QtWidgets import QApplication

    from common.setting import Setting
    from controller.controller import Controller
    from model.model import Model
    from view.view_manager import ViewManager

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



    print('Todo:')
    print('www.tgpdog.com', '  - VeroniccaComSite ')
    print('http://www.shameless.com/', 'verifyed, script')
    print('http://www.phicatube.net/videos', 'verifyed, plus file; "var cnf ="')
    print('https://www.pornfreeze.com/','verifyed, simple')
    # print('https://www.tnaflix.com/', 'simple but ajax')
    print('http://www.txxx.com/  script')
    print('https://faapy.com/', 'jwplayer script')
    print('')
    print('http://www.girlstop.info/','photo')
    print('https://www.coedcherry.com/models/danica-mpl-studios')

    # print('Исправить TUBE8')
    print('Thats all')
    print("Let's go..")
    print('')


    app = QApplication(sys.argv)

    view=ViewManager()
    model=Model(view)
    controller=Controller(view,model)
    Setting.log=view.get_log()

    sys.exit(app.exec_())






