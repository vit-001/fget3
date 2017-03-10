# -*- coding: utf-8 -*-
__author__ = 'Vit'
import json, os

from common.setting import Setting
from data_format.url import URL

from interface.favorites_interface import FavoritesInterface
from interface.site_interface import SiteInterface

class Favorites(FavoritesInterface):
    def __init__(self, favorites_filename:str):
        self.filename=favorites_filename
        self.data=[]
        self.read_datafile(self.filename)

    def add(self, label:str, url: URL):
        for i,(fav_label,fav_url) in enumerate(self.data):
            if fav_url==url:
                self.data[i]=tuple([label,url])
                return
        print('Add', url.get(), 'to favorites as', label)
        self.data.append(tuple([label,url]))

    def remove(self, url: URL):
        for i,(fav_label,fav_url) in enumerate(self.data):
            if fav_url==url:
                self.data.pop(i)
                return

    def get_favorite_items(self, site: SiteInterface) -> list:
        fav_list=list()
        for (label,url) in self.data:
            if site.can_accept_url(url):
                fav_list.append(dict(label=label, url=url))
        return fav_list

    def read_datafile(self, filename:str):
        print('Load favorites from', filename)
        try:
            with open(filename) as config:
                data = json.load(config)
                for (label,url_ser) in data:
                    self.data.append(tuple([label,URL.from_dict(url_ser)]))
        except EnvironmentError as err:
            print('Read ' + filename + ' error: ', err)
        except (TypeError, ValueError):
            print('Favorites savefile error, using default')

    def write_datafile(self, filename:str):
        print('Writing',len(self.data),'favorites records to',filename)
        data=[]
        for (label,url) in self.data:
            data.append(tuple([label,url.to_dict_serialize()]))
        try:
            os.replace(filename, filename + '.old')
        except EnvironmentError as err:
            print('Writing ' + filename + ' error: ', err)

        try:
            with open(filename, 'w') as fav_file:
                json.dump(data, fav_file)
        except EnvironmentError as err:
            print('Writing ' + filename + ' error: ', err)

    def on_exit(self):
        self.write_datafile(self.filename)

if __name__ == "__main__":
    f=Favorites(Setting.global_data_path+'favorites.json')
    # f.add('aaa', URL('aaa'))

    print(f.data)

    f.on_exit()

