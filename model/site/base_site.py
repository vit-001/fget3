# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta

__author__ = 'Vit'

from bs4 import BeautifulSoup

from common.url import URL
from common.setting import Setting
from model.loader.base_loader import FLData
from model.base_model import ModelFromSiteInterface
from view.base_view import ViewManagerFromModelInterface, ThumbViewFromModelInterface

class ThumbData(FLData):
    def __init__(self, thumb_url: URL, thumb_filename: str, href:URL, popup:str='', labels:list=list()):
        super().__init__(thumb_url, filename=thumb_filename, overwrite=False)
        self.href=href
        self.popup=popup
        self.labels=labels

class SiteInterface:
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        pass

    @staticmethod
    def can_accept_url(url:URL)->bool:
        return False

    def goto_url(self, url:URL, **options):
        pass

class ParseResult:
    def __init__(self):
        self._result_type= 'none'
        self.title='Title'
        self.thumbs=[]
        self.video = None
        self.controls_top = []
        self.controls_bottom = []
        self.controls_mid = []

    def add_thumb(self,thumb_url:URL, href:URL, popup:str='', labels:list=list()):
        self._result_type= 'thumbs'
        thumb={'url':thumb_url,'href':href,'popup':popup,'labels':labels}
        self.thumbs.append(thumb)

    def add_page(self,text: str, href: URL, menu=None, style: dict = None):
        control={'text':text,'href':href,'menu':menu,'style':style}
        self.controls_bottom.append(control)

    def add_tag(self,text: str, href: URL, menu=None, style: dict = None):
        control={'text':text,'href':href,'menu':menu,'style':style}
        self.controls_mid.append(control)

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
        print('Goto url:', url, end='')
        self.start_options=options
        print(options)

        loader=self.model.loader
        filedata=FLData(url,'')

        loader.start_load_file(filedata, self.on_load_url)

    def on_load_url(self, filedata:FLData):
        # print(filedata.url, 'loaded')
        soup=BeautifulSoup(filedata.text,'html.parser')
        self.parse_soup(soup, filedata.url)
        if self.is_no_result:
            print('Parsing has no result')

    def parse_soup(self, soup: BeautifulSoup, url: URL) -> bool:
        return False

    def generate_thumb_view(self):
        view=self.start_options.get('current_thumb_view', None)
        if not view:
            view=self.model.view.prepare_thumb_view(self.title)
        else:
            view.re_init(self.title)
        loader=self.model.loader.get_new_load_process(
            on_load_handler=lambda tumbdata:view.add_thumb(tumbdata.filename,tumbdata.href,tumbdata.popup,tumbdata.labels))

        thumb_list=list()
        for thumb in self.thumbs:
            filename=thumb['url'].get_short_filename(base=Setting.cache_path)
            thumb_list.append(ThumbData(thumb['url'],filename,thumb['href'],thumb['popup'], thumb['labels']))
        loader.load_list(thumb_list)

        for item in self.controls_bottom:
            view.add_bottom_line(item['text'], item['href'],item['href'].get(),item['menu'],item['style'])

        for item in self.controls_mid:
            view.add_mid_line(item['text'], item['href'],item['href'].get(),item['menu'],item['style'])

        for item in self.controls_top:
            view.add_top_line(item['text'], item['href'],item['href'].get(),item['menu'],item['style'])

class BaseSiteParser(BaseSite):
    def parse_soup(self, soup:BeautifulSoup, url:URL):
        self.parse_video(soup, url)
        if self.is_video:
            self.parse_video_tags(soup, url)
            return
        self.parse_pictures(soup, url)
        if self.is_pictures:
            self.parse_pictures_tags(soup, url)
            return
        self.parse_thumbs(soup, url)
        if self.is_no_result:
            self.parse_others(soup, url)
        if self.is_thumbs:
            self.parse_thumbs_tags(soup, url)
            self.parse_pagination(soup, url)
            self.title=self.parse_thumb_title(soup,url)
            self.generate_thumb_view()

    def parse_thumbs(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_video(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_pictures(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_others(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_pagination(self, soup: BeautifulSoup, url: URL):
        container = self.get_pagination_container(soup)
        if container is not None:
            for page in container.find_all('a', {'href': True}):
                if page.string is not None and page.string.isdigit():
                    self.add_page(page.string, URL(page.attrs['href'], base_url=url))
                    # print('Add page',page.string, URL(page.attrs['href'], base_url=url), page.attrs['href'])

    def get_pagination_container(self, soup:BeautifulSoup)->BeautifulSoup:
        return None

    def parse_thumbs_tags(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_video_tags(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_pictures_tags(self, soup:BeautifulSoup, url:URL):
        pass

    def parse_thumb_title(self, soup:BeautifulSoup, url:URL)->str:
        return 'Title'

if __name__ == "__main__":
    pass