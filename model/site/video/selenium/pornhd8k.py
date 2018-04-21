# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from common.util import _iter, pretty, collect_string,psp,quotes
from data_format.fl_data import FLData
from data_format.url import URL
from interface.view_manager_interface import ViewManagerFromModelInterface
from model.site.parser import BaseSiteParser


class Pornhd8kSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('pornhd8k.me/')

    @staticmethod
    def create_start_button(view: ViewManagerFromModelInterface):
        # menu_items = dict(HD=URL('http://collectionofbestporn.com/tag/hd-porn*'),
        #                   Latest=URL('http://collectionofbestporn.com/most-recent*'),
        #                   TopRated=URL('http://collectionofbestporn.com/top-rated*'),
        #                   MostViewed=URL('http://collectionofbestporn.com/most-viewed*'),
        #                   Categories=URL('http://collectionofbestporn.com/channels/'),
        #                   Longest=URL('http://collectionofbestporn.com/longest*'))

        view.add_start_button(picture_filename='model/site/resource/pornhd8k.png',
                              # menu_items=menu_items,
                              url=URL("http://pornhd8k.me/porn-hd-videos*", test_string='Porn'))

    def get_shrink_name(self):
        return 'P8'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for containrer in _iter(soup.find_all('div', {'class': ['movies-list']})):
            # pretty(containrer)
            for thumbnail in _iter(containrer.find_all('div', {'class': 'ml-item'})):
                # pretty(thumbnail)
                href = URL(thumbnail.a.attrs['href'], base_url=url, load_method='SELENIUM')
                description = thumbnail.a.attrs['title']
                thumb_url = URL(thumbnail.a.img.attrs['data-original'], base_url=url)

                duration = thumbnail.find('em', {'class': "time_thumb"})
                dur_time = collect_string(duration)

                quality = thumbnail.find('span', {'class': "mli-quality"})
                qual = collect_string(quality) if quality else ''

                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       {'text': description, 'align': 'bottom center'},
                                       {'text': qual, 'align': 'top left', 'bold': True}])

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        menu = soup.find('div', {'id': 'menu'})
        if menu:
            # pretty(menu)
            for tag in menu.find_all('a'):
                # pretty(tag)
                href=tag.attrs['href']
                if '/' in href:
                    self.add_tag(str(tag.string).strip(), URL(href, base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('ul', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        container=soup.find('div',{'id':'media-player'})
        if container:
            self._result_type = 'video'
            # pretty(container)
            video=container.find('video')
            if video:
                video_id=video.attrs['src'].rpartition('/')[2].partition('.')[0]
                video_base=video.attrs['src'].rpartition('/')[0]
                n=int(video_id,base=16)

                def _add(name, base, n):
                    addr = base + '/' + hex(n).partition('x')[2] + '.mp4'
                    self.add_video(name, URL(addr))

                _add('-1 (720)',video_base,n-1)
                _add(' 0 (480)', video_base, n)
                _add('-2 (360)', video_base, n-2)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        category_container=soup.find('div',{'class':'mvic-info'})
        if category_container:
            for href in _iter(category_container.find_all('a')):
                if href.string:
                    self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url), style={'color': 'blue'})

        tag_container=soup.find('div', {'id': 'mv-keywords'})
        if tag_container:
            # pretty(tag_container)
            for href in _iter(tag_container.find_all('a')):
                self.add_tag(str(href.attrs['title']), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass