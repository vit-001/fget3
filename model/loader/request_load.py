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
            headers=dict()
            headers['user-agent']=url.user_agent
            if url.referer:
                headers['Referer']=url.referer.get()

            if url.method == 'GET':
                response = requests.get(url.get(), cookies=url.coockies, proxies=self.proxies,headers=headers)
            elif url.method == 'POST':
                # print('Loading POST')
                # print(url.get(), url.post_data)
                response = requests.post(url.get(), data=url.post_data, proxies=self.proxies,headers=headers)
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

    def get_redirect_location(self, url: URL) -> URL:
        try:
            headers=dict()
            headers['user-agent']=url.user_agent

            if url.method == 'GET':
                response = requests.get(url.get(), cookies=url.coockies, proxies=self.proxies,headers=headers,
                                        stream=True, allow_redirects=False)
            elif url.method == 'POST':
                response = requests.post(url.get(), data=url.post_data, proxies=self.proxies,headers=headers,
                                         stream=True, allow_redirects=False)
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
            location=response.headers.get('Location', None)
            if location:
                return URL(location)
            else:
                return None


if __name__ == "__main__":
    l = RequestLoad()
    url = URL('http://scs.spb.ru')
    print(l.open(url).decode(errors='ignore'))
