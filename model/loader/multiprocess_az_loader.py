# -*- coding: utf-8 -*-
__author__ = 'Vit'

import datetime
import json
import os
import re
import requests
from multiprocessing import Manager, Queue, Process, Lock

from common.setting import Setting

from data_format.fl_data import FLData
from data_format.url import URL
from data_format.loader_error import LoaderError

from interface.loader_interface import LoadProcessInterface, LoaderInterface

from model.loader.base_loader import BaseLoadProcedure
from model.loader.request_load import RequestLoad
from model.loader.trick_load import TrickLoad
from model.loader.selenium_load import SeleniumLoad
from model.loader.selenium_hidden_firefox_load import SeleniumHiddenFirefoxLoad

class DataServer:
    def __init__(self):
        self.manager = Manager()
        self.data = self.manager.dict()
        self.last_load_proxy_pack = None
        self.init_data()
        # print('Proxy pack', len(self.data['proxy_domains']))

    def get_data(self):
        return self.data

    def stop(self):
        self.write_config(Setting.data_server_config_path+'az.json')
        self.manager.shutdown()

    def init_data(self):
        print('Requests version: ' + requests.__version__)
        self.read_config(Setting.data_server_config_path+'az.json')
        self.read_proxy_pac(URL("http://antizapret.prostovpn.org/proxy.pac*"))
        self.data['domain_cash'] = dict()

    def read_proxy_pac(self, pac_url):
        if self.last_load_proxy_pack:
            if datetime.datetime.now() - self.last_load_proxy_pack < datetime.timedelta(hours=2):
                return
        try:
            print('Loading', pac_url)
            pac = RequestLoad().open(pac_url).decode(errors='ignore')

            r = re.search('\"PROXY (.*); DIRECT', pac)
            if r:
                self.data['free_http_proxy'] = r.group(1)
                # p = re.findall("\"(.*?)\",", pac)
                #
                # proxy_domains = list()
                # for item in p:
                #     proxy_domains.append(item)
                # self.data['proxy_domains']=proxy_domains
        except LoaderError:
            print('AZLoader error:', pac_url, 'not loaded. Lets try to load later...')

        self.last_load_proxy_pack=datetime.datetime.now()

    def read_config(self, config_filename):
        try:
            with open(config_filename) as config:
                data = json.load(config)
                self.data['free_http_proxy'] = data.get('free_http_proxy', None)
                self.data['proxy_domains'] = data.get('proxy_domains', list())
                self.last_load_proxy_pack = datetime.datetime.fromtimestamp(data.get('last_loaded'), None)

                print('Load DataServer config')

        except EnvironmentError as err:
            print('Read ' + config_filename + ' error: ', err)
        except (TypeError, ValueError):
            print('DataServer config error, using default')
            self.last_load_proxy_pack = None

    def write_config(self, config_filename):
        try:
            os.replace(config_filename, config_filename + '.old')
        except EnvironmentError as err:
            print('Writing ' + config_filename + ' error: ', err)

        try:
            with open(config_filename, 'w') as config:
                print('Writing DataServer config to ' + config_filename)

                data = dict()
                data['free_http_proxy'] = self.data['free_http_proxy']
                data['last_loaded'] = self.last_load_proxy_pack.timestamp()
                data['proxy_domains'] = self.data.get('proxy_domains', list())

                json.dump(data, config)
        except EnvironmentError as err:
            print('Writing ' + config_filename + ' error: ', err)


class AZloaderMP(BaseLoadProcedure):
    def __init__(self, data, lock:Lock):
        self.data = data
        self.lock = lock
        self.request_load = RequestLoad()
        self.trick_load = TrickLoad()
        self.selenium_load=SeleniumLoad()
        self.selenium_hidden_load=SeleniumHiddenFirefoxLoad()

    def open(self, url: URL) -> bytes:
        self.lock.acquire()
        method = self.get_load_method(url)
        self.lock.release()

        if method == 'none':
            raise LoaderError('No way to open, connection not established or content filtered.')

        if method == 'plain':
            self.request_load.proxies = None
            return self.request_load.open(url)
        elif method == 'proxy':
            self.request_load.proxies = {'http': self.data.get('free_http_proxy', '')}
            return self.request_load.open(url)
        elif method == 'selenium_ie':
            return self.selenium_load.open(url)
        elif method == 'selenium':
            return self.selenium_hidden_load.open(url)

        else:
            return self.trick_load.open(url,method)

    def get_redirect_location(self, url: URL) -> URL:
        return self.request_load.get_redirect_location(url)

    def get_load_method(self, url: URL) -> str:

        if url.load_method=='SELENIUM':
            return 'selenium'

        if url.load_method == 'SELENIUM_IE':
            return 'selenium_ie'

        domain_cash = self.data.get('domain_cash', dict())
        domain = url.domain()
        for item in domain_cash:
            if '.' + item in domain or item == domain:
                return domain_cash[item]

        if url.test_string is None:
            return 'plain'

        if Setting.debug_loader:
            print('Testing domain:', domain, '... ')
        method = self._inspect_availability(url)
        if Setting.debug_loader:
            print('            ...', method)

        # self.lock.acquire()
        domain_cash = self.data.get('domain_cash', dict())
        if domain.startswith('www.'):
            domain=domain.partition('.')[2]
        domain_cash[domain] = method
        self.data['domain_cash'] = domain_cash
        # print(domain_cash)
        # self.lock.release()

        return method

    def _inspect_availability(self, url: URL) -> str:
        self.request_load.proxies = None
        try:
            string = self.request_load.open(url).decode(errors='ignore')

            if url.test_string in string:
                return 'plain'
        except LoaderError:
            pass

        try:
            self.request_load.proxies = {'http': self.data.get('free_http_proxy', '')}
            string = self.request_load.open(url).decode(errors='ignore')

            if url.test_string in string:
                return 'proxy'
        except LoaderError:
            pass

        for method_name in self.trick_load.trick_headers:
            # print(method_name)
            string = self.trick_load.open(url,trick=method_name).decode(errors='ignore')
            # print(string)
            if url.test_string in string:
                return method_name

        return 'none'


class LoadProcessEvent():
    def __init__(self, type: str, data=None):
        self.type = type
        self.data = data

class LoadServer(Process):
    def __init__(self,
                 fldata_list: list,
                 events_queue: Queue,
                 data_server: DataServer,
                 lock: Lock):
        self.filelist = fldata_list
        self.events = events_queue
        self.data = data_server.get_data()
        self.lock = lock
        Process.__init__(self)

    def run(self):
        self.events.put(LoadProcessEvent('start'))
        loader = AZloaderMP(self.data, self.lock)

        for filedata in self.filelist:
            try:
                result=loader.load_to_file(filedata)
                self.events.put(LoadProcessEvent('load', result))
            except (ValueError, LoaderError) as Error:
                self.events.put(LoadProcessEvent('error', filedata))
                print(filedata.url.get() + ' not loaded: ', Error)
        self.events.put(LoadProcessEvent('done'))


class LoadProcess(LoadProcessInterface):
    def __init__(self, data_server: DataServer, lock: Lock):
        self.loader = None
        self.events_queue = Queue()
        self.data_server = data_server
        self.lock = lock

    def set_handlers(self,on_load_handler, on_end_handler):
        self.on_load = on_load_handler
        self.on_end = on_end_handler

    def load_list(self, fldata_list: list):
        self.loader = LoadServer(fldata_list, self.events_queue, self.data_server, self.lock)
        self.loader.start()

    def update(self):
        if self.events_queue:
            while not self.events_queue.empty():
                event = self.events_queue.get()

                if event.type == 'load':
                    self.on_load(event.data)

                if event.type == 'done':
                    self.on_end()

    def abort(self):
        if self.loader is not None:
            self.loader.terminate()
            self.update()

class MultiprocessAZloader(LoaderInterface):
    def __init__(self):
        self.data = DataServer()
        self.lock = Lock()
        self.list_of_load_process = list()
        self.single_file_loader = None

    def get_new_load_process(self, on_load_handler=lambda filedata: None,
                             on_end_handler=lambda: None) -> LoadProcessInterface:

        new_process = LoadProcess(data_server=self.data,
                                  lock=self.lock)
        new_process.set_handlers(on_load_handler=on_load_handler,
                                  on_end_handler=lambda :self.on_end_of_process_handler(new_process,on_end_handler))
        self.list_of_load_process.append(new_process)
        return new_process

    def on_end_of_process_handler(self, process:LoadProcess, handler=lambda:None):
        self.list_of_load_process.remove(process)
        handler()

    def on_update(self):
        if self.single_file_loader:
            self.single_file_loader.update()
        for load_process in self.list_of_load_process:
            load_process.update()

    def start_load_file(self, filedata: FLData, on_result=lambda filedata: None):
        self.single_file_loader = self.get_new_load_process(on_load_handler=on_result,
                                                            on_end_handler=lambda: None)

        self.single_file_loader.load_list([filedata])

    def on_exit(self):
        self.data.stop()
        for load_process in self.list_of_load_process:
            load_process.abort()


if __name__ == "__main__":
    import time
    l=MultiprocessAZloader()
    time.sleep(2)

    l.on_exit()

