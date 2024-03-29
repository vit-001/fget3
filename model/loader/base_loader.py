# -*- coding: utf-8 -*-
__author__ = 'Vit'

import io
import os

from data_format.fl_data import FLData
from data_format.url import URL

from data_format.loader_error import LoaderError
from interface.loader_interface import LoadProcedureInterface


class BaseLoadProcedure(LoadProcedureInterface):
    def open(self, url: URL) -> bytes:
        'Open a network object denoted by a URL and return his bytes representstive.'
        pass

    def get_redirect_location(self, url:URL)->URL:
        'Open only response header and return redirect URL if its present, else return None'
        return None

    def load_to_file(self, file: FLData) -> FLData:
        if file.find_redirect_location:
            file.redirect_location = self.get_redirect_location(file.url)
            return file

        if file.overwrite or (not os.path.exists(file.filename)):
            result = self.open(file.url)

            if file.filename == None or file.filename == '':
                file.text = result.decode(errors='ignore')
                return file

            path = os.path.dirname(file.filename)

            if not os.path.exists(path):
                os.makedirs(path)

            buf = io.BytesIO(result)
            try:
                # print(file.filename)
                with open(file.filename, 'wb') as fd:
                    chunk = buf.read(256)
                    while len(chunk) > 0:
                        fd.write(chunk)
                        chunk = buf.read(256)
            except FileNotFoundError as err:
                print(err)
            except OSError as err:
                print(err)

        return file


if __name__ == "__main__":
    raise LoaderError('test')
