# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

import os


class InterfaceCompiler():
    def __init__(self, base_dir:str, test_compile=False):

        # self.test_compile = test_compile

        self.interfaces = ['main_window','scroll_bar_widget', 'full_view_window']

        # self.test_interfaces = ['tst_qpixmap', 'tst', 'video_player']

        # if self.test_compile:
        #     self.interfaces.extend(self.test_interfaces)

        self.base_dir = base_dir                                     #'E:/repo/fget3'
        self.source_dir = self.base_dir + '/view/qt_design/'
        self.dest_dir = self.base_dir + '/view/qt_ui/'

        self.pyuic5 = 'C:/Python34/Lib/site-packages/PyQt5/pyuic5.bat '

    def compile_interfaces(self):

        for fname in self.interfaces:
            source = self.source_dir + fname + '.ui'
            dest = self.dest_dir + fname + '.py'
            command = self.pyuic5 + source + ' -o ' + dest
            print(command)
            os.system(command)

    def run_all(self):
        for fname in self.interfaces:
            os.system('C:/Python34/pythonw ' + self.dest_dir + 'tests/' + fname + '_tst.py')


if __name__ == "__main__":
    ic = InterfaceCompiler()
    ic.compile_interfaces()
    ic.run_all()