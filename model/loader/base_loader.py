# -*- coding: utf-8 -*-
__author__ = 'Vit'

import io
import os
import urllib.parse as up

from common.url import URL

class FLData:
    def __init__(self, url: URL, filename: str, overwrite=True):
        self._url = url
        self._filename = filename
        self.overwrite = overwrite
        self.text=''

    def get_url(self):
        return self._url

    def set_url(self, url:URL):
        self._url=url

    def get_filename(self):
        return self._filename

class LoaderError(RuntimeError):
    def __init__(self, description):
        self.txt = description

    def __str__(self):
        return self.txt


class BaseLoadProcedure:
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
        if file.overwrite or (not os.path.exists(file.get_filename())):
            result = self.open(file.get_url())

            if file.get_filename() is None or file.get_filename() is '':
                file.text = result.decode()
                return file

            path = os.path.dirname(file.get_filename())

            if not os.path.exists(path):
                os.makedirs(path)

            buf = io.BytesIO(result)
            with open(file.get_filename(), 'wb') as fd:
                chunk = buf.read(256)
                while len(chunk) > 0:
                    fd.write(chunk)
                    chunk = buf.read(256)
        return file


class BaseLoadProcess:
    def load_list(self, fldata_list: list):
        pass

    def abort(self):
        pass

    def update(self):
        pass


class BaseLoader:
    def get_new_load_process(self, on_load_handler=lambda x: None, on_end_handler=lambda: None) -> BaseLoadProcess:
        pass

    def start_load_file(self, filedata: FLData, on_result=lambda filedata: None):
        pass

    def on_update(self):
        pass

    def on_exit(self):
        pass


if __name__ == "__main__":
    raise LoaderError('test')
