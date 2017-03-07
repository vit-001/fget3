# -*- coding: utf-8 -*-
__author__ = 'Vit'

class LoaderError(RuntimeError):
    def __init__(self, description):
        self.txt = description

    def __str__(self):
        return self.txt


if __name__ == "__main__":
    pass