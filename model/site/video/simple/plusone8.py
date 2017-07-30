# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from common.util import _iter, quotes, psp, collect_string

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class PlusoneSite(BaseSiteParser):

    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('plusone8.com/')
    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Popular=URL('http://plusone8.com/?filter=rate*'),
                        Latest=URL('http://plusone8.com/?filter=date*'),
                        Random=URL('http://plusone8.com/?filter=random*'),
                        MostViewed=URL('http://plusone8.com/?filter=views*'),
                        Categories=URL('http://plusone8.com/categories/'),
                        Longest=URL('http://plusone8.com/?filter=duration*'))

        view.add_start_button(picture_filename='model/site/resource/plusone8.png',
                              menu_items=menu_items,
                              url=URL("http://plusone8.com/?filter=date*", test_string='Porn'))

    def get_shrink_name(self):
        return 'PO8'

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        container = soup.find('main',{'id':'main'})
        if container:
            for thumbnail in _iter(container.find_all('div', {'class': 'column'})):
                # psp(thumbnail.prettify())
                xref=thumbnail.find('a')
                if xref:
                    href = URL(xref.attrs['href'], base_url=url)
                    description = xref.attrs['title']
                    thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

                    duration = thumbnail.find('span', {'class': "length"})
                    dur_time = '' if duration is None else collect_string(duration)

                    quality = thumbnail.find('span', {'class': "quality"})
                    qual = '' if quality is None else str(quality.string)

                    self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                                   labels=[{'text': dur_time, 'align': 'top right'},
                                           {'text': description, 'align': 'bottom center'},
                                           {'text': qual, 'align': 'top left', 'bold': True}])

    def get_pagination_container(self, soup: BeautifulSoup):
        return soup.find('div', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        video = soup.find('div',{'class':'video-player'})
        if video is not None:
            # psp(video.prettify())
            for source in _iter(video.find_all('source')):
                psp(source)
                self.add_video('DEFAULT', URL(source.attrs['src'], base_url=url))
            self.set_default_video(-1)

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        for actor_container in _iter(soup.find_all('div', {'id': 'video-actors'})):
            for href in _iter(actor_container.find_all('a')):
                psp(href)
                self.add_tag(str(href.attrs['title']), URL(href.attrs['href'], base_url=url), style={'color': 'blue'})

        for tag_container in _iter(soup.find_all('div', {'id': 'cat-list'})):
            for href in _iter(tag_container.find_all('a')):
                psp(href)
                self.add_tag(str(href.attrs['title']), URL(href.attrs['href'], base_url=url))


if __name__ == "__main__":
    pass