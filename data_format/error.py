# -*- coding: utf-8 -*-
__author__ = 'Nikitin'

class BaseFgetError(RuntimeError):
    def __init__(self, caption:str):
        self.caption=caption

    def __str__(self):
        return self.caption

class AbstractMethodError(BaseFgetError):
    def __init__(self):
        super().__init__('This method must be redefining')


if __name__ == "__main__":
    pass