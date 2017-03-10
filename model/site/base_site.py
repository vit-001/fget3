# -*- coding: utf-8 -*-
__author__ = 'Vit'

from bs4 import BeautifulSoup

from common.setting import Setting
from common.util import get_menu_handler
from data_format.fl_data import FLData
from data_format.url import URL
from interface.model_interface import ModelFromSiteInterface
from interface.site_interface import SiteInterface


class ThumbData(FLData):
    def __init__(self, thumb_url: URL, thumb_filename: str, href:URL, popup:str='', labels:list=list()):
        super().__init__(thumb_url, filename=thumb_filename, overwrite=False)
        self.href=href
        self.popup=popup
        self.labels=labels

class ParseResult:
    def __init__(self):
        self.url=URL()

        self._result_type= 'none'
        self.title='No title'

        self.waiting_data=False

        self.thumbs=[]

        self.video_data = []
        self.video_default_index=0

        self.pictures=[]

        self.controls_top = []
        self.controls_bottom = []
        self.controls_mid = []

    def add_thumb(self,thumb_url:URL, href:URL, popup:str='', labels:list=list()):
        self._result_type= 'thumbs'
        thumb={'url':thumb_url,'href':href,'popup':popup,'labels':labels}
        self.thumbs.append(thumb)

    def add_fav(self,text: str, href: URL, menu=None, style: dict = None):
        control={'text':text,'href':href,'menu':menu,'style':style}
        self.controls_top.append(control)

    def add_page(self,text: str, href: URL, menu=None, style: dict = None):
        control={'text':text,'href':href,'menu':menu,'style':style}
        self.controls_bottom.append(control)

    def add_tag(self,text: str, href: URL, menu=None, style: dict = None):
        control={'text':text,'href':href,'menu':menu,'style':style}
        self.controls_mid.append(control)

    def add_video(self, caption:str, url:URL):
        self._result_type='video'
        self.video_data.append(dict(text=caption, url=url))

    def add_picture(self, filename:str, url:URL):
        self._result_type='pictures'
        self.pictures.append(dict(file=filename, url=url))

    def sort_video(self):
        self.video_data.sort(key=lambda x:int(x['text']))

    def set_default_video(self, default=0):
        self.video_default_index=default

    @property
    def is_video(self)->bool:
        return self._result_type == 'video'

    @property
    def is_pictures(self)->bool:
        return self._result_type == 'pictures'

    @property
    def is_thumbs(self)->bool:
        return self._result_type == 'thumbs'

    @property
    def is_no_result(self) -> bool:
        return self._result_type == 'none'


class BaseSite(SiteInterface, ParseResult):
    def __init__(self, model:ModelFromSiteInterface):
        ParseResult.__init__(self)
        self.model=model
        self.start_options=dict()

    def goto_url(self, url: URL, **options):
        print() #todo отладочный вывод
        print('Goto url:', url)

        self.url=url
        self.start_options=options
        # print(options)

        loader=self.model.loader
        filedata=FLData(url,'')

        loader.start_load_file(filedata, self.on_load_url)

    def on_load_url(self, filedata:FLData):
        # print(filedata.url, 'loaded')
        soup=BeautifulSoup(filedata.text,'html.parser')
        self.parse_soup(soup, filedata.url)

        if self.is_no_result and not self.waiting_data:
            print('Parsing has no result')

    def parse_soup(self, soup: BeautifulSoup, url: URL) -> bool:
        return False

    def generate_thumb_view(self):
        if self.waiting_data:
            return

        view=self.start_options.get('current_thumb_view', None)
        if not view:
            view=self.model.view_manager.new_thumb_view()
            view.subscribe_to_history_event(self.model.thumb_history.add)

        flags=self.start_options.get('flags')
        loader=self.model.loader.get_new_load_process(
            on_load_handler=lambda tumbdata:view.add_thumb(tumbdata.filename,tumbdata.href,tumbdata.popup,tumbdata.labels))

        thumb_list=list()
        statistic=dict()
        accepted=0
        rejected=0
        for thumb in self.thumbs:
            domain=thumb['href'].domain()
            statistic[domain]=statistic.get(domain,0)+1
            if self.model.can_accept_url(thumb['href']):
                accepted+=1
                filename=thumb['url'].get_short_filename(base=Setting.thumbs_cache_path)
                thumb_list.append(ThumbData(thumb['url'],filename,thumb['href'],thumb['popup'], thumb['labels']))
            else:
                rejected+=1

        view.prepare(url=self.url, title=self.title, tooltip=self.url.get(),on_stop=loader.abort, flags=flags,max_progress=len(thumb_list))

        # print statistic for url
        print()#todo отладочный вывод
        print('Statistic for',self.url)
        for domain in statistic:
            print('  {0:5d} in {1}'.format(statistic[domain], domain))
        print('Total {0}, accepted {1}, rejected {2}'.format(accepted+rejected,accepted,rejected))

        loader.load_list(thumb_list)

        for item in self.model.get_favorite_items(self):
            self.add_fav(item['label'], item['url'], style=dict(on_remove=get_menu_handler(self.model.remove_favorite,item['url'])))

        self.add_controls_to_view(view)

    def generate_video_view(self):
        if self.waiting_data:
            return

        view = self.start_options.get('current_full_view', None)
        if not view:
            view = self.model.view_manager.new_full_view()
            view.subscribe_to_history_event(self.model.full_history.add)

        flags = self.start_options.get('flags')
        view.prepare(url=self.url,title=self.title, tooltip=self.url.get(),flags=flags)

        view.set_video_list(self.video_data, self.video_default_index)

        self.add_controls_to_view(view)

        print()
        print('Now playback', self.url) # todo сделать отладочный вывод
        for item in self.video_data:
            print(item['text'], item['url'])
        print('Default:', self.video_data[self.video_default_index]['text'])

    def generate_pictures_view(self):
        if self.waiting_data:
            return

        view = self.start_options.get('current_full_view', None)
        if not view:
            view = self.model.view_manager.new_full_view()
            view.subscribe_to_history_event(self.model.full_history.add)

        flags = self.start_options.get('flags')
        loader=self.model.loader.get_new_load_process(
            on_load_handler=lambda fl_data:view.add_picture(fl_data.filename))
        view.prepare(url=self.url, title=self.title, tooltip=self.url.get(),on_stop=loader.abort, flags=flags,max_progress=len(self.pictures))

        pictures_list=list()
        for picture in self.pictures:
            filename=Setting.pictures_path+picture['file'].strip('/')
            pictures_list.append(FLData(picture['url'],filename,overwrite=False))

        loader.load_list(pictures_list)

        self.add_controls_to_view(view)

        # print('Now playback', self.url) # todo сделать отладочный вывод

    def add_controls_to_view(self, view):
        for item in self.controls_bottom:
            view.add_to_bottom_line(item['text'], item['href'], item['href'].get(), item['menu'], item['style'])

        for item in self.controls_mid:
            view.add_to_mid_line(item['text'], item['href'], item['href'].get(), item['menu'], item['style'])

        for item in self.controls_top:
            view.add_to_top_line(item['text'], item['href'], item['href'].get(), item['menu'], item['style'])


if __name__ == "__main__":
    pass