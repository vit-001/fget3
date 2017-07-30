# -*- coding: utf-8 -*-
__author__ = 'Vit'

from data_format.fl_data import FLData
from data_format.url import URL


class LoadProcedureInterface:
    def open(self, url: URL) -> bytes:
        'Open a network object denoted by a URL and return his bytes representstive.'
        pass

    def load_to_file(self, file: FLData) -> FLData:
        """
        Load a network object denoted by a URL to a local file.
        :param file - url and local file name:
        :return same object, but if file.get_filendme() is '' or None file don't write and
                in file.text will returned decoded neteork object:
        """
        pass


class LoadProcessInterface:
    def load_list(self, fldata_list: list):
        pass

    def abort(self):
        pass

    def update(self):
        pass


class LoaderInterface:
    def get_new_load_process(self, on_load_handler=lambda x: None, on_end_handler=lambda: None) -> LoadProcessInterface:
        pass

    def start_load_file(self, filedata: FLData, on_result=lambda filedata: None):
        pass

    def on_update(self):
        pass

    def on_exit(self):
        pass


if __name__ == "__main__":
    pass