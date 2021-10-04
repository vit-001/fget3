# -*- coding: utf-8 -*-
__author__ = 'Vit'

from bs4 import BeautifulSoup

def _iter(source):
    if source is None:
        return []
    else:
        return source

def get_menu_handler(function,*args,**options):
    return lambda:function(*args,**options)

def quotes(text:str, from_lex:str, to_lex:str):
    return text.partition(from_lex)[2].partition(to_lex)[0]

def collect_string(soup:BeautifulSoup)->str:
    result=''
    for s in soup.stripped_strings:
        result += s

    return result

def collect_string_to_array(soup:BeautifulSoup):
    result=list()
    for s in soup.stripped_strings:
        result.append(s)

    return result


def sp():
    print('=========================================')

def psp(*arguments, **keywords):
    print(*arguments, **keywords)
    sp()

def pretty(soup:BeautifulSoup):
    psp(soup.prettify())

if __name__ == "__main__":
    pass