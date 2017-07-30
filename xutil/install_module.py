# -*- coding: utf-8 -*-
__author__ = 'Vit'

import pip, importlib, sys

def test_module(module:str, load_name:str=None):
    try:
        importlib.import_module(module)
    except ImportError:
        print('You need to install',module)
        print('Trying...')
        if load_name is None:
            load_name=module
        result=pip.main(['install', load_name])
        if result:
            print('Error in pip. Trying to upgrade')
            pip.main(['install', '--upgrade', 'pip'])
            print('Please restart program')
            sys.exit(44)

if __name__ == "__main__":
    test_module('PyQt5')
