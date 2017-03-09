# -*- coding: utf-8 -*-
__author__ = 'Vit'
from bs4 import BeautifulSoup

from data_format.url import URL
from data_format.fl_data import FLData
from common.util import _iter, quotes

from interface.view_manager_interface import ViewManagerFromModelInterface

from model.site.parser import BaseSiteParser


class RealGfSite(BaseSiteParser):
    @staticmethod
    def can_accept_url(url: URL) -> bool:
        return url.contain('realgfporn.com/')

    @staticmethod
    def create_start_button(view:ViewManagerFromModelInterface):
        menu_items=dict(Most_Recent=URL('http://www.realgfporn.com/most-recent/'),
                    Categories=URL('http://www.realgfporn.com/channels/'),
                    Longest=URL('http://www.realgfporn.com/longest/'),
                    Most_Viewed=URL('http://www.realgfporn.com/most-viewed/'),
                    Top_Rated=URL('http://www.realgfporn.com/top-rated/')
                    )

        view.add_start_button(name='Realgf',
                              picture_filename='model/site/resource/realgf.png',
                              menu_items=menu_items,
                              url=URL("http://www.realgfporn.com/most-recent/", test_string='Real GF Porn'))

    def parse_thumbs(self, soup: BeautifulSoup, url: URL):
        for thumbnail in _iter(soup.find_all('div', {'class': 'post'})):
            href = URL(thumbnail.a.attrs['href'], base_url=url)
            description = thumbnail.a.img.attrs['alt']
            thumb_url = URL(thumbnail.img.attrs['src'], base_url=url)

            duration = thumbnail.find('b', {'class': 'post-duration'})
            dur_time = '' if duration is None else str(duration.string)
            print(dur_time,href)

            if dur_time != 'Link':
                self.add_thumb(thumb_url=thumb_url, href=href, popup=description,
                               labels=[{'text': dur_time, 'align': 'top right'},
                                       {'text': description, 'align': 'bottom center'}])

    def parse_thumb_title(self, soup: BeautifulSoup, url: URL) -> str:
        return 'RGF '+ url.get().partition('realgfporn.com/')[2].strip('/')

    def parse_thumbs_tags(self, soup: BeautifulSoup, url: URL):
        tags_container = soup.find('div', {'class': 'site-cats'})
        if tags_container is not None:
            for tag in _iter(tags_container.find_all('a')):
                self.add_tag(str(tag.string), URL(tag.attrs['href'], base_url=url))

    def get_pagination_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find('div', {'class': 'pagination'})

    def parse_video(self, soup: BeautifulSoup, url: URL):
        content = soup.find('div', {'id': 'mediaspace'})
        if content is not None:
            script = content.find('script', text=lambda x: 'jwplayer(' in x)
            if script is not None:
                data = str(script.string).replace(' ', '')
                file = quotes(data, 'file:"', '"')
                self.add_video('DEFAULT', URL(file, base_url=url))

    def parse_video_title(self, soup: BeautifulSoup, url: URL) -> str:
        return url.get().rpartition('/')[2].rpartition('.')[0].rpartition('-')[0]

    def parse_video_tags(self, soup: BeautifulSoup, url: URL):
        tags = list()
        for item in _iter(soup.find_all('div', {'class': 'more-content'})):
            for href in _iter(item.find_all('a')):
                if href.string is not None:
                    if '/user/' in href.attrs['href']:
                        self.add_tag(str(href.string), URL(href.attrs['href'], base_url=url),
                                        style={'color':'blue'})
                    else:
                        tags.append({'text':str(href.string), 'href':URL(href.attrs['href'], base_url=url)})

        for item in tags:
            self.add_tag(item['text'],item['href'])
#

if __name__ == "__main__":
    pass
