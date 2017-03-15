# -*- coding: utf-8 -*-
__author__ = 'Vit'

import requests

from data_format.url import URL
from data_format.loader_error import LoaderError

from model.loader.base_loader import BaseLoadProcedure


class RequestLoad(BaseLoadProcedure):
    def __init__(self, proxies=None):
        self.proxies = proxies

    def open(self, url: URL) -> bytes:
        try:
            if url.method == 'GET':
                response = requests.get(url.get(), cookies=url.coockies, proxies=self.proxies)
            elif url.method == 'POST':
                print('Loading POST')
                print(url.get(), url.post_data)
                response = requests.post(url.get(), data=url.post_data, proxies=self.proxies)
            else:
                raise LoaderError('Unknown method:' + url.method)

            response.raise_for_status()

        except requests.exceptions.HTTPError as err:
            raise LoaderError('HTTP error: {0}'.format(err.response.status_code))

        except requests.exceptions.ConnectTimeout:
            raise LoaderError('Connection timeout')

        except requests.exceptions.ReadTimeout:
            raise LoaderError('Read timeout')

        except requests.exceptions.ConnectionError:
            raise LoaderError('Connection error')

        except:
            raise LoaderError('Unknown error in loader')
        else:
            return response.content


if __name__ == "__main__":
    l = RequestLoad()
    url = URL('http://scs.spb.ru')
    print(l.open(url).decode(errors='ignore'))
