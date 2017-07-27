# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes, psp, sp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class Tube8Site(BaseSiteParser): #todo исправить TUBE8
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('tube8.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Newest=URL('http://www.tube8.com/newest.html*'),
                        Newest_long=URL('http://www.tube8.com/newest.html?filter_duration=long*'),
                        Newest_medium=URL('http://www.tube8.com/newest.html?filter_duration=medium*'),
                        Newest_short=URL('http://www.tube8.com/newest.html?filter_duration=short*'),
                        Featured=URL('http://www.tube8.com/latest.html*'),
                        Featured_long=URL('http://www.tube8.com/latest.html?filter_duration=long*'),
                        Featured_medium=URL('http://www.tube8.com/latest.html?filter_duration=medium*'),
                        Featured_short=URL('http://www.tube8.com/latest.html?filter_duration=short*'))

        view.add_start_button(picture_filename='model/site/resource/tube8.png',
                              menu_items=menu_items,
                              url=URL("http://www.tube8.com/newest.html*"))

    def get_shrink_name(self):
        return 'T8'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': ['video_box','thumb-wrapper']})):
            href = URL(thumbnail.a.attrs['href'], base_url=url)
            thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)
            label=thumbnail.img.attrs.get('alt','')

            duration = thumbnail.find('div', {'class': 'video_duration'})
            dur_time = '' if duration is None else str(duration.string)

            hd_span = thumbnail.find('span', {'class': 'hdIcon'})
            hd = 'HD' if hd_span else ''

            self.add_thumb(thumb_url=thumb_url, href=href, popup=label,
                           labels=[{'text':dur_time, 'align':'top right'},
                                   {'text':label, 'align':'bottom center'},
                                   {'text': hd, 'align': 'top left'}])

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('ul',{'id':'pagination'})

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        menu=soup.find('div',{'class':'menu-box'})

        categories=menu.find('div',{'id':'categories-subnav-box'})
        for tag in _iter(categories.find_all('a')):
            self.add_tag(collect_string(tag),URL(tag.attrs['href']))

    def parse_video(self, soup: BeautifulSoup, url: URL):
        player_container = soup.find('div', {'id':'playerContainer'})
        if player_container:
            script=player_container.find('script', text=lambda x: 'flashvars' in str(x))
            flashvars=quotes(script.string.replace('\\', '').replace(' ',''),'flashvars={','};')
            print(flashvars)
            while '"quality_' in flashvars:
                nxt = flashvars.partition('"quality_')[2]

                t = nxt.partition('":"')
                label = t[0]
                file = t[2].partition('",')[0]
                if file.startswith('http://') or file.startswith('https://'):
                    self.add_video(label,URL(file+'*'))
                flashvars = nxt
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        info_box=soup.find('div',{'class':'infoBox'})
        if info_box:
            user_span=info_box.find('span',{'id':'videoUsername'})
            if user_span and user_span.a:
                username=user_span.find('span',{'class':'username'}).string.strip()
                href=URL(user_span.a.attrs['href'].replace('/user/','/user-videos/'))
                self.add_tag(username,href,style=dict(color='blue'))

            category=info_box.find('li',{'class':'video-category'})
            if category and category.a:
                self.add_tag(category.a.string.strip(),URL(category.a.attrs['href']))

            tag_list=info_box.find('li',{'class':'tag-list'})
            if tag_list:
                for tag in _iter(tag_list.find_all('a')):
                    self.add_tag(tag.string.strip(), URL(tag.attrs['href']))


if __name__ == "__main__":
    pass
