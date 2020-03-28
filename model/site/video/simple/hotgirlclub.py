# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, pretty, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class HotgirlclubSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('hotgirlclub.com/')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Newest=URL('http://www.hotgirlclub.com/videos/newest/'),
                        TopRatedMounth=URL('http://www.hotgirlclub.com/videos/top-rated/month/'),
                        TopRatedAll=URL('http://www.hotgirlclub.com/videos/top-rated/all-time/'),
                        MostViewedAll=URL('http://www.hotgirlclub.com/videos/most-viewed/all-time/'),
                        MostViewedMounth=URL('http://www.hotgirlclub.com/videos/most-viewed/month/'),
                        Longest=URL('http://www.hotgirlclub.com/videos/longest/'))

        view.add_start_button(picture_filename='model/site/resource/hotgirlclub.png',
                              menu_items=menu_items,
                              url=URL("http://www.hotgirlclub.com/videos/newest/", test_string='Porn'))

    def get_shrink_name(self):
        return 'HG'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('li', {'class': 'thumb thumb-video'})):
            img=thumbnail.find('img')
            href = URL(thumbnail.a.attrs['href'], base_url=url)
            description = img.attrs['alt']
            thumb_url = URL(img.attrs.get('data-src', thumbnail.img.attrs.get('src')), base_url=url)

            duration = thumbnail.find('span', {'class': "duration"})
            dur_time = '' if duration is None else str(duration.string)

            quality = thumbnail.find('span', {'class': "quality"})
            qual = '' if quality is None else str(quality.string)

            self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                           labels=[{'text': dur_time, 'align': 'top right'},
                                   {'text': description, 'align': 'bottom center'},
                                   {'text': qual, 'align': 'top left', 'bold': True}])

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('ul', {'class': 'pagination-list'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('video')
        if video:
            for source in _iter(video.find_all('source')):
                self.add_video(source.attrs['type'], URL(source.attrs['src'], base_url=url))
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        # adding "star" to video
        for metadata in _iter(soup.find_all('div', {'class': 'info-col'})):
            for href in _iter(metadata.find_all('a', href=lambda x: '/pornstars/' in str(x))):
                self.add_tag(collect_string(href), URL(href.attrs['href'] + '', base_url=url), style=dict(color='red'))

        # adding "categories" to video
        for metadata in _iter(soup.find_all('div', {'class': 'info-col'})):
            for href in _iter(metadata.find_all('a', href=lambda x: '/categories/' in str(x))):
                self.add_tag(collect_string(href), URL(href.attrs['href'] + '', base_url=url), style=dict(color='green'))

        # adding "tags" to video
        for metadata in _iter(soup.find_all('div', {'class': 'info-col'})):
            for href in _iter(metadata.find_all('a', href=lambda x: '/tags/' in str(x))):
                self.add_tag(collect_string(href), URL(href.attrs['href'] + '', base_url=url))



if __name__ == "__main__":
    pass