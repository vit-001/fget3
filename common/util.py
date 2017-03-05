# -*- coding: utf-8 -*-
__author__ = 'Vit'

def _iter(source):
    if source is None:
        return []
    else:
        return source

def get_menu_handler(function,*args,**options):
    return lambda:function(*args,**options)

def quotes(text:str, from_lex:str, to_lex:str):
    return text.partition(from_lex)[2].partition(to_lex)[0]

def sp():
    print('=========================================')

def psp(*arguments, **keywords):
    print(*arguments, **keywords)
    sp()

if __name__ == "__main__":
    pass