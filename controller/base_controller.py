# -*- coding: utf-8 -*-
__author__ = 'Vit'

from common.url import URL

class ControllerFromViewInterface:
    def goto_url(self, url:URL, **options):
        pass

    def on_cycle_handler(self):
        pass

    def on_exit(self):
        pass

class ControllerFromModelInterface:
    pass

if __name__ == "__main__":
    pass